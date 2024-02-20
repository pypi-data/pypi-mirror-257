import importlib
from typing import List, Union, Dict, Any


from langchain.embeddings.base import Embeddings

from langchain.llms.base import BaseLLM, LLM
from coagent.llm_models.llm_config import EmbedConfig, LLMConfig
from coagent.connector.phase import BasePhase
from coagent.connector.agents import BaseAgent
from coagent.connector.chains import BaseChain
from coagent.connector.schema import Message, Role, PromptField, ChainConfig
from coagent.tools import toLangchainTools, TOOL_DICT, TOOL_SETS


class AgentFlow:
    def __init__(
        self, 
        role_type: str,
        role_name: str,
        agent_type: str,
        role_prompt: str,
        prompt_config: List[Dict[str, Any]],
        prompt_manager_type: str = "PromptManager",
        chat_turn: int = 3,
        focus_agents: List[str] = [],
        focus_messages: List[str] = [],
        embeddings: Embeddings = None,
        llm: BaseLLM = None,
        **kwargs
    ):
        self.role_type = role_type
        self.role_name = role_name
        self.agent_type = agent_type
        self.role_prompt = role_prompt

        self.prompt_config = prompt_config
        self.prompt_manager_type = prompt_manager_type

        self.chat_turn = chat_turn
        self.focus_agents = focus_agents
        self.focus_messages = focus_messages

        self.embeddings = embeddings
        self.llm = llm
        self.build_config()
        self.build_agent()

    def build_config(self,):
        self.llm_config = LLMConfig(model_name="test", llm=self.llm)
        self.embed_config = EmbedConfig(embed_model="test", langchain_embeddings=self.embeddings)

    def build_agent(self, ):
        # 可注册个性化的agent，仅通过start_action和end_action来注册
        # class ExtraAgent(BaseAgent):
        #     def start_action_step(self, message: Message) -> Message:
        #         pass

        #     def end_action_step(self, message: Message) -> Message:
        #         pass
        # agent_module = importlib.import_module("coagent.connector.agents")
        # setattr(agent_module, 'extraAgent', ExtraAgent)

        # 可注册个性化的prompt组装方式，
        # class CodeRetrievalPM(PromptManager):
        #     def handle_code_packages(self, **kwargs) -> str:
        #         if 'previous_agent_message' not in kwargs:
        #             return ""
        #         previous_agent_message: Message = kwargs['previous_agent_message']
        #         # 由于两个agent共用了同一个manager，所以临时性处理
        #         vertices = previous_agent_message.customed_kargs.get("RelatedVerticesRetrivalRes", {}).get("vertices", [])
        #         return ", ".join([str(v) for v in vertices])

        # prompt_manager_module = importlib.import_module("coagent.connector.prompt_manager")
        # setattr(prompt_manager_module, 'CodeRetrievalPM', CodeRetrievalPM)
        
        # agent实例化
        agent_module = importlib.import_module("coagent.connector.agents")
        baseAgent: BaseAgent = getattr(agent_module, self.agent_type)
        role = Role(
            role_type=self.agent_type, role_name=self.role_name, 
            agent_type=self.agent_type, role_prompt=self.role_prompt,
        )

        self.agent = baseAgent(
                    role=role, 
                    prompt_config = [PromptField(**config) for config in self.prompt_config],
                    prompt_manager_type=self.prompt_manager_type,
                    chat_turn=self.chat_turn,
                    focus_agents=self.focus_agents,
                    focus_message_keys=self.focus_messages,
                    llm_config=self.llm_config,
                    embed_config=self.embed_config,
                )
        







class ChainFlow:
    def __init__(
        self, 
        chain_name: str,
        agent_flow1: AgentFlow,
        agent_flow2: AgentFlow = None,
        agent_flow3: AgentFlow = None,
        chat_turn: int = 5,
        do_checker: bool = False,
        embeddings: Embeddings = None,
        llm: BaseLLM = None,

        # chain_type: str = "BaseChain",
        **kwargs
    ):
        self.agent_flows = [agent_flow1, agent_flow2, agent_flow3]
        self.agent_flows = [agent_flow for agent_flow in self.agent_flows if agent_flow]
        self.chat_turn = chat_turn
        self.do_checker = do_checker
        self.chain_name = chain_name
        self.chain_type = "BaseChain"

        self.embeddings = embeddings
        self.llm = llm
        self.build_config()
        self.build_chain()

    def build_config(self,):
        self.llm_config = LLMConfig(model_name="test", llm=self.llm)
        self.embed_config = EmbedConfig(embed_model="test", langchain_embeddings=self.embeddings)
    
    def build_chain(self, ):
        # chain 实例化
        chain_module = importlib.import_module("coagent.connector.chains")
        baseChain: BaseChain = getattr(chain_module, self.chain_type)

        agent_names = [agent_flow.role_name for agent_flow in self.agent_flows]
        chain_config = ChainConfig(chain_name=self.chain_name, agents=agent_names, do_checker=self.do_checker, chat_turn=self.chat_turn)
        self.chain = baseChain(
                chain_config,
                [agent_flow.agent for agent_flow in self.agent_flows], 
                embed_config=self.embed_config,
                llm_config=self.llm_config,
                )
        



class PhaseFlow:
    def __init__(
        self, 
        phase_name: str,
        chain_flow1: ChainFlow,
        chain_flow2: ChainFlow = None,
        chain_flow3: ChainFlow = None,
        embeddings: Embeddings = None,
        llm: BaseLLM = None,
        **kwargs
    ):
        self.phase_name = phase_name
        self.chain_flows = [chain_flow1, chain_flow2, chain_flow3]
        self.chain_flows = [chain_flow for chain_flow in self.chain_flows if chain_flow]
        self.phase_type = "BasePhase"

        self.embeddings = embeddings
        self.llm = llm
        self.build_config()
        self.build_phase()
    
    def __call__(self, params: dict) -> str:

        tools = toLangchainTools([TOOL_DICT[i] for i in TOOL_SETS if i in TOOL_DICT])
        query_content = "帮我确认下127.0.0.1这个服务器的在10点是否存在异常，请帮我判断一下"
        query = Message(
            role_name="human", role_type="user", tools=tools,
            role_content=query_content, input_query=query_content, origin_query=query_content
            )
        # phase.pre_print(query)
        output_message, output_memory = self.phase.step(query)
        return output_memory.to_str_messages(return_all=True, content_key="parsed_output_list")

    def build_config(self,):
        self.llm_config = LLMConfig(model_name="test", llm=self.llm)
        self.embed_config = EmbedConfig(embed_model="test", langchain_embeddings=self.embeddings)

    def build_phase(self, ):
        # phase 实例化
        phase_module = importlib.import_module("coagent.connector.phase")
        basePhase: BasePhase = getattr(phase_module, self.phase_type)

        self.phase = basePhase(
                phase_name=self.phase_name,
                chains=[chain_flow.chain for chain_flow in self.chain_flows],
                embed_config=self.embed_config,
                llm_config=self.llm_config,
                )
