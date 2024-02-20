from json import JSONDecodeError
from typing import Any
from fastapi import APIRouter, Query, Request, Response
from fastapi.responses import JSONResponse


class TemplateRouter(APIRouter):
    """"""

    def __init__(self, *args: Any, title: str, description: str, version: str, configuration, **kwargs: Any):
        self.title = title
        self.description = description
        self.version = version
        self.configuration = configuration
        super().__init__(*args, **kwargs)

        @self.get("/")
        async def root_mock(request: Request, query: str | None = Query(None)) -> Response:
            """Template request response."""
            if query:
                match query.lower():
                    case "error":
                        return JSONResponse(status_code=400, content={"status": "error"})
                    case "get":
                        return JSONResponse(status_code=200, content={"status": "ok"})
            try:
                body = await request.json()
            except JSONDecodeError:
                return JSONResponse(status_code=500, content={"status": "error", "debug": "Could not parse json input."})
            data = body.get("data")
            return JSONResponse(status_code=200, content={
                "status": "ok",
                "output": {
                    "pong": data
                }
            })

        @self.put("/")
        async def root_put_mock(request: Request, query: str | None = Query(None)) -> Response:
            return await root_mock(request, query)

        @self.post("/")
        async def root_post_mock(request: Request, query: str | None = Query(None)) -> Response:
            return await root_mock(request, query)
