from pydantic import BaseModel


class UwaziEntity(BaseModel):
    identifier: str
    text: str = None
    pdf_path: str = None