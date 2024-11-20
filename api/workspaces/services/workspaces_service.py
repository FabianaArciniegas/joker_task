from typing import List

from motor.motor_asyncio import AsyncIOMotorDatabase

from api.workspaces.schemas.inputs import WorkspaceCreation, WorkspaceUpdate
from api.workspaces.schemas.outputs import WorkspaceResponse
from repositories.workspaces import WorkspacesRepository
from schemas.api_response import ApiResponse


class WorkspaceService:
    def __init__(self, db: AsyncIOMotorDatabase, api_response: ApiResponse):
        self.db = db
        self.api_response = api_response
        self.workspace_repository = WorkspacesRepository(self.db, self.api_response)

    async def create_workspace(self, workspace_data: WorkspaceCreation) -> WorkspaceResponse:
        self.api_response.logger.info("Check if the workspace already exists")
        await self.workspace_repository.workspace_available(workspace_data.workspace_name)
        self.api_response.logger.info('Creating workspace')
        created_workspace = await self.workspace_repository.create(workspace_data.model_dump())
        workspace = WorkspaceResponse(**created_workspace.model_dump())
        return workspace

    async def get_workspace_by_id(self, workspace_id: str) -> WorkspaceResponse:
        self.api_response.logger.info("Get workspace")
        found_workspace = await self.workspace_repository.get_by_id(workspace_id)
        workspace = WorkspaceResponse(**found_workspace.model_dump())
        return workspace

    async def get_all_workspaces(self) -> List[WorkspaceResponse]:
        self.api_response.logger.info("Get all workspaces")
        found_workspaces = await self.workspace_repository.get_all()
        workspaces = []
        for workspace in found_workspaces:
            workspaces.append(WorkspaceResponse(**workspace.model_dump()))
        return workspaces

    async def update_workspace(self, workspace_id: str, workspace_data: WorkspaceUpdate) -> WorkspaceResponse:
        self.api_response.logger.info("Check if data is available")
        await self.workspace_repository.workspace_available(workspace_data.workspace_name)
        self.api_response.logger.info("Received data to update workspace")
        updated_workspace = await self.workspace_repository.patch(workspace_id, workspace_data)
        workspace = WorkspaceResponse(**updated_workspace.model_dump())
        return workspace

    async def delete_workspace(self, workspace_id: str) -> None:
        self.api_response.logger.info("Delete workspace")
        await self.workspace_repository.delete(workspace_id)
