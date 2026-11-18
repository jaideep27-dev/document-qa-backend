from typing import Annotated

from fastapi import Depends
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import llm_settings
from app.services.llm_service import LLMService
from app.services.pdf_service import PdfService


def get_google_chat_model():
    return ChatGoogleGenerativeAI(
        model=llm_settings.GOOGLE_MODEL, api_key=llm_settings.GOOGLE_API_KEY
    )


LLMDependency = Annotated[BaseChatModel, Depends(get_google_chat_model)]


def get_system_prompt():
    from pathlib import Path
    path = Path(__file__).parent.parent / "core" / "system_prompt.txt"
    with open(path, "r") as f:
        return f.read()


def get_llm_service(llm_dependency: LLMDependency):
    return LLMService(llm=llm_dependency, system_prompt=get_system_prompt())


LLMServiceDep = Annotated[LLMService, Depends(get_llm_service)]


def get_pdf_service():
    return PdfService()


PdfServiceDep = Annotated[PdfService, Depends(get_pdf_service)]
