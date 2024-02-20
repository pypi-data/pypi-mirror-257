from pathlib import Path
from typing import Any
import arklog
from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse, FileResponse


class FileRouter(APIRouter):
    """"""

    def __init__(self, *args: Any, title: str, description: str, version: str, configuration, templates, **kwargs: Any):
        self.title = title
        self.description = description
        self.version = version
        self.configuration = configuration
        super().__init__(*args, **kwargs)

        @self.get("/{file_path:path}")
        async def file_access(file_path: str) -> Response:
            """"""
            looking_for = Path(file_path)
            if looking_for.exists():
                arklog.debug(f"Retuning file '{looking_for.name}'.")
                return FileResponse(looking_for)
            arklog.warning(f"File {looking_for.name} not found.")
            return JSONResponse(status_code=404, content={"error": f"File {looking_for.name} not found."})
