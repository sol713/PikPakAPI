import secrets
from typing import Dict, Optional


class SessionStore:
    """
    Minimal in-memory session store for demo purposes.
    Stores encoded PikPak token keyed by generated session_id.
    """

    def __init__(self) -> None:
        self._sessions: Dict[str, str] = {}

    def create_session(self, encoded_token: str) -> str:
        session_id = secrets.token_urlsafe(32)
        self._sessions[session_id] = encoded_token
        return session_id

    def get_token(self, session_id: str) -> Optional[str]:
        return self._sessions.get(session_id)

    def delete_session(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)


session_store = SessionStore()
