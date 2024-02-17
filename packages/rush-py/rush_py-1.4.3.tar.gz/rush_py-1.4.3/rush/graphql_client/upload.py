# Generated by ariadne-codegen
# Source: combined.graphql

from typing import Any, Optional
from uuid import UUID

from .base_model import BaseModel


class Upload(BaseModel):
    upload: "UploadUpload"


class UploadUpload(BaseModel):
    id: UUID
    value: Optional[Any]


Upload.model_rebuild()
UploadUpload.model_rebuild()
