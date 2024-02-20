from json import JSONDecodeError
from typing import Any
import arklog
import invoke
from fastapi import APIRouter, Query, Request, Response
from fastapi.responses import JSONResponse
from starlette.responses import HTMLResponse


class ShellRouter(APIRouter):
    """"""

    def __init__(self, *args: Any, title: str, description: str, version: str, configuration, templates, **kwargs: Any):
        self.title = title
        self.description = description
        self.version = version
        self.configuration = configuration
        self.templates = templates
        super().__init__(*args, **kwargs)

        @self.get("/", response_class=HTMLResponse)
        async def root_shell(request: Request, query: str | None = Query(None)) -> Response:
            """"""
            return self.templates.TemplateResponse(
                request=request, name="shell.html", context={"id": id}
            )


        @self.post("/")
        async def root_post_shell(request: Request, query: str | None = Query(None)) -> Response:
            try:
                body = await request.json()
                arklog.debug(body)
            except JSONDecodeError:
                return JSONResponse(status_code=500, content={"status": "error", "debug": "Could not parse json input."})
            command = body.get("command")
            result = invoke.run(command)
            arklog.debug(command)
            return JSONResponse(status_code=200, content={
                "status": "ok",
                "output": {
                    "command": str(command),
                    "result": str(result)
                }
            })
