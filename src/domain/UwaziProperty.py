from pathlib import Path

from pydantic import BaseModel, model_validator


class UwaziProperty(BaseModel):
    identifier: str = None
    shared_id: str = None
    content_hash: str = None
    language: str = None
    property_name: str = None
    text: str = None
    pdf_path: Path = None

    @model_validator(mode='after')
    def set_identifier(self):
        if not self.identifier and self.shared_id and self.language and self.property_name and self.content_hash:
            self.identifier = f"{self.shared_id}____{self.language}____{self.property_name}____{self.content_hash}"
        return self

    def remove_pdf(self):
        if self.pdf_path and self.pdf_path.exists():
            self.pdf_path.unlink()
