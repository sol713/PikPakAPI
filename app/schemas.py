from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    session_id: str
    user_id: Optional[str] = None
    encoded_token: str


class FileItem(BaseModel):
    id: str
    name: str
    kind: str


class FileListResponse(BaseModel):
    files: List[FileItem] = Field(default_factory=list)
    next_page_token: Optional[str] = None
    path_trail: List[FileItem] = Field(default_factory=list)


class DownloadLinksRequest(BaseModel):
    file_ids: List[str]


class DownloadLink(BaseModel):
    file_id: str
    web_content_link: Optional[str] = None
    medias: Optional[list] = None


class DownloadLinksResponse(BaseModel):
    links: List[DownloadLink]


class ShareLinksRequest(BaseModel):
    share_links: List[str]
    pass_code: Optional[str] = None


class ShareInfo(BaseModel):
    share_link: str
    data: dict
    error: Optional[str] = None


class ShareLinksResponse(BaseModel):
    results: List[ShareInfo]


class ShareSaveResult(BaseModel):
    share_link: str
    saved_ids: List[str] = Field(default_factory=list)
    error: Optional[str] = None


class ShareSaveRequest(BaseModel):
    share_links: List[str]
    pass_code: Optional[str] = None


class ShareSaveResponse(BaseModel):
    results: List[ShareSaveResult]


class MoveCopyRequest(BaseModel):
    from_paths: List[str]
    to_path: str
    move: bool = False
    create: bool = False


class MoveCopyResponse(BaseModel):
    result: Dict[str, Any]


class OfflineTaskCreateRequest(BaseModel):
    url: str
    parent_id: Optional[str] = None
    name: Optional[str] = None


class OfflineTaskActionRequest(BaseModel):
    task_id: str


class OfflineTaskDeleteRequest(BaseModel):
    task_ids: List[str]
    delete_files: bool = False


class OfflineTask(BaseModel):
    id: str
    name: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None


class OfflineTaskListResponse(BaseModel):
    tasks: List[OfflineTask] = Field(default_factory=list)
    next_page_token: Optional[str] = None


class VipInfoResponse(BaseModel):
    data: Dict[str, Any]
