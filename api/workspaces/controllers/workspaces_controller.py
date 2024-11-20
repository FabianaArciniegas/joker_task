from typing import Annotated, List

from fastapi import Request, Response, Depends
from fastapi.routing import APIRouter

from api.workspaces.schemas.inputs import WorkspaceCreation, WorkspaceUpdate
from api.workspaces.schemas.outputs import WorkspaceResponse
from api.workspaces.services.workspaces_service import WorkspaceService
from models.responde_model import ResponseModel
from schemas import api_response
from schemas.api_response import ApiResponse
from utils.reponse_handler import response_handler

workspaces_router: APIRouter = APIRouter(prefix="/workspaces")


@workspaces_router.post(
    path="",
    tags=["workspaces"],
    description="Create a new Workspace",
)
@response_handler()
async def create_workspace(
        request: Request,
        response: Response,
        workspace_data: WorkspaceCreation,
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> ResponseModel[WorkspaceResponse]:
    api_response.logger.info("Received data to create workspace")
    workspace_service = WorkspaceService(request.app.database, api_response)
    workspace = await workspace_service.create_workspace(workspace_data)
    return workspace


@workspaces_router.get(
    path="/id={workspace_id}",
    tags=["workspaces"],
    description="Get a specific Workspace",
)
@response_handler()
async def get_workspace_by_id(
        request: Request,
        response: Response,
        workspace_id: str,
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> ResponseModel[WorkspaceResponse]:
    api_response.logger.info("Received data to get workspace")
    workspace_service = WorkspaceService(request.app.database, api_response)
    workspace = await workspace_service.get_workspace_by_id(workspace_id)
    return workspace


@workspaces_router.get(
    path="",
    tags=["workspaces"],
    description="Get all Workspaces",
)
@response_handler()
async def get_all_workspaces(
        request: Request,
        response: Response,
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> ResponseModel[List[WorkspaceResponse]]:
    api_response.logger.info("Received data to get all workspaces")
    workspace_service = WorkspaceService(request.app.database, api_response)
    workspaces = await workspace_service.get_all_workspaces()
    return workspaces

@workspaces_router.patch(
    path="/id={workspace_id}",
    tags=["workspaces"],
    description="Update a Workspace",
)
@response_handler()
async def update_workspace(
        request: Request,
        response: Response,
        workspace_id: str,
        workspace_data:WorkspaceUpdate,
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
)->ResponseModel[WorkspaceResponse]:
    api_response.logger.info("Received data to update workspace")
    workspace_service = WorkspaceService(request.app.database, api_response)
    workspace = await workspace_service.update_workspace(workspace_id, workspace_data)
    return workspace

@workspaces_router.delete(
    path="/id={workspace_id}",
    tags=["workspaces"],
    description="Delete a Workspace",
)
@response_handler()
async def delete_workspace(
        request: Request,
        response: Response,
        workspace_id: str,
)->ResponseModel:
    api_response.logger.info("Received data to delete workspace")
    workspace_service = WorkspaceService(request.app.database, api_response)
    await workspace_service.delete_workspace(workspace_id)
    return