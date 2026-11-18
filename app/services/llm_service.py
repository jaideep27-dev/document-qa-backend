from collections.abc import AsyncGenerator
from langchain.chat_models import BaseChatModel
from langchain.messages import HumanMessage, SystemMessage


class LLMService:
    def __init__(self, llm: BaseChatModel, system_prompt: str):
        self.llm = llm
        self.system_prompt = system_prompt

    async def chat(self, query: str, pdf_content: str):
        response = self.llm.astream(
            [
                SystemMessage(
                    content=self.system_prompt.format(pdf_content=pdf_content)
                ),
                HumanMessage(content=query),
            ]
        )
        async for chunk in response:
            if chunk:
                yield chunk.text
