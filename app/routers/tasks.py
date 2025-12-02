from typing import Optional, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, Query, status

from pikpakapi import PikPakApi, PikpakException

from .. import schemas
from ..deps import get_client


router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("/offline", response_model=schemas.OfflineTaskListResponse)
async def list_offline_tasks(
    client: PikPakApi = Depends(get_client),
    limit: int = Query(default=50, ge=1, le=500),
    page_token: Optional[str] = Query(default=None, alias="page_token"),
):
    try:
        data = await client.offline_list(size=limit, next_page_token=page_token)
    except PikpakException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    tasks = []
    for t in data.get("tasks", []):
        tasks.append(
            schemas.OfflineTask(
                id=t.get("id", ""),
                name=t.get("name", ""),
                status=t.get("phase"),
                created_at=t.get("created_time"),
            )
        )
    return schemas.OfflineTaskListResponse(
        tasks=tasks, next_page_token=data.get("next_page_token")
    )


@router.post("/offline", response_model=Dict[str, Any])
async def create_offline_task(
    payload: schemas.OfflineTaskCreateRequest, client: PikPakApi = Depends(get_client)
):
    try:
        return await client.offline_download(
            file_url=payload.url, parent_id=payload.parent_id, name=payload.name
        )
    except PikpakException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/offline/retry")
async def retry_offline_task(
    payload: schemas.OfflineTaskActionRequest, client: PikPakApi = Depends(get_client)
):
    try:
        return await client.offline_task_retry(task_id=payload.task_id)
    except PikpakException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/offline")
async def delete_offline_task(
    payload: schemas.OfflineTaskDeleteRequest, client: PikPakApi = Depends(get_client)
):
    try:
        await client.delete_tasks(task_ids=payload.task_ids, delete_files=payload.delete_files)
        return {"deleted": payload.task_ids}
    except PikpakException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
