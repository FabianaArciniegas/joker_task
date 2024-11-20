from pydantic import BaseModel


class WorkspaceResponse(BaseModel):
    workspace_name: str
    workspace_image: str = "url"

