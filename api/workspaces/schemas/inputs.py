from typing import Optional

from pydantic import BaseModel


class WorkspaceCreation(BaseModel):
    workspace_name: str
    description: Optional[str] = None
    workspace_image: str = "url"


class WorkspaceUpdate(BaseModel):
    workspace_name: Optional[str] = None
    description: Optional[str] = None
    workspace_image: Optional[str] = None
