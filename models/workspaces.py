from typing import Optional

from models.base_model import BaseModelDB


class WorkspacesModel(BaseModelDB):
    _collection_name = 'workspaces'
    workspace_name: str
    description: Optional[str] = None
    workspace_image: str = "url"