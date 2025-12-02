from fastapi import APIRouter, Depends, HTTPException, Response, status

from pikpakapi import PikPakApi, PikpakException

from .. import schemas
from ..deps import get_client
from ..store import session_store


router = APIRouter(prefix="/api", tags=["auth"])


@router.post("/login", response_model=schemas.LoginResponse)
async def login(payload: schemas.LoginRequest, response: Response):
    client = PikPakApi(username=payload.username, password=payload.password)
    try:
        await client.login()
        await client.refresh_access_token()
    except PikpakException as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    session_id = session_store.create_session(client.encoded_token)
    response.set_cookie("session_id", session_id, httponly=True)
    return schemas.LoginResponse(
        session_id=session_id,
        user_id=client.user_id,
        encoded_token=client.encoded_token,
    )


@router.get("/me")
async def me(client: PikPakApi = Depends(get_client)):
    return {"status": "ok", "user_id": client.user_id}
