from core.errors import NotAvailableError
from models.responde_model import LocationError
from models.workspaces import WorkspacesModel
from repositories.base_repository import BaseRepository


class WorkspacesRepository(BaseRepository[WorkspacesModel]):
    _entity_model = WorkspacesModel

    async def workspace_available(self, workspace_name: str, raise_exception: bool = True) -> None:
        self.api_response.logger.info("Checking availability")
        workspace = await self.collection.find_one({"workspace_name": workspace_name})
        if workspace and raise_exception:
            raise NotAvailableError(message=f"The workspace {workspace} is not available, it already exists",
                                    location=LocationError.Body)
