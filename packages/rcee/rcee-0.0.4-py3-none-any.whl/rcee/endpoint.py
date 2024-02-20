import logging
import time
from pathlib import Path
from typing import Any
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from rcee.routers import FileRouter
from rcee.routers.shell import ShellRouter


class RemoteCodeExecutionEndpoint(FastAPI):
    """"""

    def __init__(self, *args: Any, title: str, description: str, version: str, configuration, **kwargs: Any):
        """"""
        self.title = title
        self.description = description
        self.version = version
        self.configuration = configuration
        super().__init__(*args, title=title, description=description, version=version, **kwargs)
        logging.debug(self.description)
        self.mount("/static", StaticFiles(directory=configuration.root_directory / Path("data/static")), name="static")
        templates = Jinja2Templates(directory=configuration.root_directory / Path("data/templates"))

        # self.include_router(TemplateRouter(title=title, description=description, version=version, configuration=configuration), prefix="/template")
        self.include_router(FileRouter(title=title, description=description, version=version, configuration=configuration, templates=templates), prefix="/files")
        self.include_router(ShellRouter(title=title, description=description, version=version, configuration=configuration, templates=templates), prefix="/shell")

        self.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @self.middleware("http")
        async def add_process_time_header(request: Request, call_next: Any) -> Response:
            start_time = time.time()
            response: Response = await call_next(request)
            duration = str(time.time() - start_time)
            response.headers["X-Process-Time"] = duration
            logging.debug(f"X-Process-Time = {duration}")
            return response
