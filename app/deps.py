from typing import Optional

from fastapi import Cookie, Depends, HTTPException, status

from pikpakapi import PikPakApi

from .store import session_store


async def get_client(session_id: Optional[str] = Cookie(default=None)) -> PikPakApi:
    if not session_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in")
    encoded_token = session_store.get_token(session_id)
    if not encoded_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")
    try:
        client = PikPakApi(encoded_token=encoded_token)
        return client
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
