from typing import Any, Iterator, List, Optional

import openai
from langchain.agents.agent import AgentExecutor
from langchain.agents.agent_toolkits import create_conversational_retrieval_agent
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models.base import BaseChatModel
from langchain.memory import ConversationBufferMemory
from langchain_openai import AzureChatOpenAI, ChatOpenAI

from mmon.config import load_config
from mmon.langchain_callback import LangChainCallbackHandler
from mmon.tools import load_tools


def get_llm() -> ChatOpenAI:
    config = load_config()
    common_openai_params = {
        "temperature": 0,
        "api_key": config.llm.openai_api_key,
        "api_version": config.llm.openai_api_version,
    }
    if len(config.llm.deployment_id) > 0:
        llm = AzureChatOpenAI(azure_endpoint=config.llm.openai_api_base, deployment_name=config.llm.deployment_id, **common_openai_params)  # type: ignore[arg-type,call-arg]
    else:
        llm = ChatOpenAI(base_url=config.llm.openai_api_base, model=config.llm.model, **common_openai_params)  # type: ignore[arg-type]
    return llm


class Engine:
    executor: AgentExecutor
    callbacks: List[BaseCallbackHandler]

    def __init__(self, llm: Optional[BaseChatModel] = None, verbose_level: int = 0):
        if llm is None:
            llm = get_llm()
        tools = load_tools(llm, verbose_level)
        if verbose_level >= 3:
            openai.log = "debug"  # type: ignore[assignment]

        self.executor = create_conversational_retrieval_agent(
            llm=llm,
            tools=tools,
            max_token_limit=2000,
            remember_intermediate_steps=False,
            verbose=verbose_level > 1,
        )
        self.callbacks = [LangChainCallbackHandler()]

    def run(self, prompt: str) -> str:
        response: str = self.executor.invoke(prompt, callbacks=self.callbacks)
        return response

    def stream(self, prompt: str) -> Iterator[dict[str, Any]]:
        # just input prompt without prep_inputs is work, but can't pass type check
        inputs = self.executor.prep_inputs(prompt)
        response = self.executor.stream(inputs, callbacks=self.callbacks)
        return response
