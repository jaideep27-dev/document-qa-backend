from fastapi import UploadFile
from pydantic import BaseModel, Field


class QAModel(BaseModel):
    question: str = Field(
        description="A question required to be answered using the given PDF file",
        min_length=5,
        max_length=100,
    )
    file: UploadFile = Field(description="PDF file uploaded by user")
