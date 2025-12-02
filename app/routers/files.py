import re
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query, status

from pikpakapi import PikPakApi, PikpakException

from .. import schemas
from ..deps import get_client


router = APIRouter(prefix="/api/files", tags=["files"])


@router.get("", response_model=schemas.FileListResponse)
async def list_files(
    client: PikPakApi = Depends(get_client),
    parent_id: Optional[str] = Query(default=None),
    path: Optional[str] = Query(default=None),
    create_missing: bool = Query(default=False),
    limit: int = Query(default=100, ge=1, le=1000),
    page_token: Optional[str] = Query(default=None, alias="page_token"),
):
    resolved_parent = parent_id
    path_trail: List[schemas.FileItem] = []

    if path:
        normalized_path = "/" + "/".join([p for p in path.split("/") if p])
        try:
            trail = await client.path_to_id(normalized_path, create=create_missing)
        except PikpakException as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
            ) from exc
        path_trail = [
            schemas.FileItem(
                id=entry.get("id", ""),
                name=entry.get("name", ""),
                kind=entry.get("file_type", ""),
            )
            for entry in trail
        ]
        if trail:
            resolved_parent = trail[-1].get("id")
        else:
            resolved_parent = None

    try:
        data = await client.file_list(
            size=limit, parent_id=resolved_parent, next_page_token=page_token
        )
    except PikpakException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    files = [
        schemas.FileItem(id=f.get("id", ""), name=f.get("name", ""), kind=f.get("kind", ""))
        for f in data.get("files", [])
    ]
    return schemas.FileListResponse(
        files=files,
        next_page_token=data.get("next_page_token"),
        path_trail=path_trail,
    )


@router.post("/download-links", response_model=schemas.DownloadLinksResponse)
async def batch_download_links(
    payload: schemas.DownloadLinksRequest, client: PikPakApi = Depends(get_client)
):
    links = []
    for file_id in payload.file_ids:
        try:
            info = await client.get_download_url(file_id)
        except PikpakException as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
        links.append(
            schemas.DownloadLink(
                file_id=file_id,
                web_content_link=info.get("web_content_link"),
                medias=info.get("medias"),
            )
        )
    return schemas.DownloadLinksResponse(links=links)


@router.post("/share-info", response_model=schemas.ShareLinksResponse)
async def batch_share_info(
    payload: schemas.ShareLinksRequest, client: PikPakApi = Depends(get_client)
):
    results: List[schemas.ShareInfo] = []
    for link in payload.share_links:
        try:
            data = await client.get_share_info(share_link=link, pass_code=payload.pass_code)
            if isinstance(data, ValueError):
                results.append(schemas.ShareInfo(share_link=link, data={}, error=str(data)))
            else:
                results.append(schemas.ShareInfo(share_link=link, data=data))
        except PikpakException as exc:
            results.append(schemas.ShareInfo(share_link=link, data={}, error=str(exc)))
    return schemas.ShareLinksResponse(results=results)


@router.post("/share-save", response_model=schemas.ShareSaveResponse)
async def batch_share_save(
    payload: schemas.ShareSaveRequest, client: PikPakApi = Depends(get_client)
):
    results: List[schemas.ShareSaveResult] = []
    pattern = re.compile(r"/s/([^/]+)(?:.*/([^/]+))?$")

    for link in payload.share_links:
        match = pattern.search(link)
        if not match:
            results.append(
                schemas.ShareSaveResult(share_link=link, error="Share link is invalid")
            )
            continue
        share_id = match.group(1)
        try:
            data = await client.get_share_info(share_link=link, pass_code=payload.pass_code)
            if isinstance(data, ValueError):
                results.append(
                    schemas.ShareSaveResult(share_link=link, error=str(data))
                )
                continue
            pass_code_token = data.get("pass_code_token")
            files = data.get("files", [])
            file_ids = [f.get("id") for f in files if f.get("id")]
            if not file_ids:
                results.append(
                    schemas.ShareSaveResult(share_link=link, error="No files found in share")
                )
                continue
            restore_result = await client.restore(
                share_id=share_id, pass_code_token=pass_code_token, file_ids=file_ids
            )
            saved_ids = restore_result.get("file_ids", file_ids)
            results.append(
                schemas.ShareSaveResult(share_link=link, saved_ids=saved_ids)
            )
        except PikpakException as exc:
            results.append(
                schemas.ShareSaveResult(share_link=link, error=str(exc))
            )
    return schemas.ShareSaveResponse(results=results)


@router.post("/move-copy", response_model=schemas.MoveCopyResponse)
async def move_or_copy(
    payload: schemas.MoveCopyRequest, client: PikPakApi = Depends(get_client)
):
    try:
        result = await client.file_move_or_copy_by_path(
            from_path=payload.from_paths,
            to_path=payload.to_path,
            move=payload.move,
            create=payload.create,
        )
    except PikpakException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc
    return schemas.MoveCopyResponse(result=result)
