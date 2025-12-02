from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .deps import get_client
from .routers import auth as auth_router
from .routers import account as account_router
from .routers import files as files_router
from .routers import tasks as tasks_router


def create_app() -> FastAPI:
    app = FastAPI(title="PikPakAPI Web", version="0.1.0")

    templates = Jinja2Templates(directory="app/templates")

    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"]
        ,
        allow_headers=["*"],
    )

    app.include_router(auth_router.router)
    app.include_router(account_router.router, dependencies=[Depends(get_client)])
    app.include_router(files_router.router, dependencies=[Depends(get_client)])
    app.include_router(tasks_router.router, dependencies=[Depends(get_client)])

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    @app.get("/login", response_class=HTMLResponse)
    async def login_page(request: Request):
        return templates.TemplateResponse("login.html", {"request": request})

    @app.get("/files", response_class=HTMLResponse)
    async def files_page(request: Request):
        return templates.TemplateResponse("files.html", {"request": request})

    return app


app = create_app()
