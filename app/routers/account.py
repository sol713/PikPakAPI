from fastapi import APIRouter, Depends, HTTPException, status

from pikpakapi import PikPakApi, PikpakException

from ..deps import get_client


router = APIRouter(prefix="/api/account", tags=["account"])


@router.get("/info")
async def account_info(client: PikPakApi = Depends(get_client)):
    return client.get_user_info()


@router.get("/quota")
async def quota_info(client: PikPakApi = Depends(get_client)):
    try:
        return await client.get_quota_info()
    except PikpakException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get("/vip")
async def vip_info(client: PikPakApi = Depends(get_client)):
    try:
        return await client.vip_info()
    except PikpakException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get("/invite-code")
async def invite_code(client: PikPakApi = Depends(get_client)):
    try:
        code = await client.get_invite_code()
        return {"code": code}
    except PikpakException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get("/transfer-quota")
async def transfer_quota(client: PikPakApi = Depends(get_client)):
    try:
        return await client.get_transfer_quota()
    except PikpakException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc
