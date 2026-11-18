import asyncio
from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, status
from fastapi.responses import StreamingResponse

from app.api.dependencies import LLMServiceDep, PdfServiceDep
from app.schema.qa_model import QAModel
from app.services.pdf_service import PdfService

router = APIRouter(prefix="/document", tags=["Document"])

CHUNK_SIZE = 1024 * 1024  # 1 MB chunk size
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB max size


@router.post("/upload-pdf", response_class=StreamingResponse)
async def upload_pdf(
    qa_data: Annotated[QAModel, Form(media_type="multipart/form-data")],
    llm_service: LLMServiceDep,
    pdf_service: PdfServiceDep,
):
    pdf_bytes = None
    while True:
        content_bytes = await qa_data.file.read(CHUNK_SIZE)
        if not content_bytes:
            break
        if pdf_bytes and len(pdf_bytes) >= MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_CONTENT_TOO_LARGE,
                detail=f"File size should be less than {MAX_FILE_SIZE} bytes",
            )
        pdf_bytes = content_bytes if not pdf_bytes else pdf_bytes + content_bytes

    if pdf_bytes:
        pdf_content = pdf_service.read(pdf_bytes)
        async for chunk in llm_service.chat(
            query=qa_data.question, pdf_content=pdf_content
        ):
            yield chunk
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="PDF file is empty"
        )
