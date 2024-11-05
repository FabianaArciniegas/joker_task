import uuid
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class BaseModelDB(BaseModel):
    __collection_name: str
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted: bool = False
