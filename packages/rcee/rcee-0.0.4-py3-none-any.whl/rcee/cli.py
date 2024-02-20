"""
Handles parsing arguments and passing them to the correct places when launching the application.
"""
import arklog
import click
import logging
import sys
import uvicorn

from rcee import __version__
from pathlib import Path
from signal import SIGINT, SIGTERM, signal
from dataclasses import dataclass
from rcee.endpoint import RemoteCodeExecutionEndpoint


@dataclass(init=True, repr=True, order=False, frozen=True)
class Configuration:
    cwd: Path
    root_directory: Path


def handler(signal_code, _) -> None:
    """Signal handler."""
    logger = logging.getLogger(__name__)
    logger.debug(f"Shutting down because signal {signal_code} was received.")
    sys.exit(1)


@click.option("--host", "-h", default="0.0.0.0", type=str, help="Address on which to listen")
@click.option("--port", "-p", default=7999, type=int, help="Port on which to listen")
def launch(host: str, port: int) -> int:
    """"""
    cwd = Path.cwd()
    root_project_directory = Path(__file__).resolve().parent.parent
    configuration = Configuration(cwd, root_project_directory)
    app = RemoteCodeExecutionEndpoint(
        version=__version__,
        title="RCEE",
        description="Remote Code Execution Endpoint",
        configuration=configuration
    )
    uvicorn.run(app, host=host, port=port)
    return 0


def entry_point():
    """"""
    signal(SIGINT, handler)
    signal(SIGTERM, handler)
    arklog.set_config_logging()
    logging.info(f"Remote code execution endpoint {__version__}.")
    sys.exit(launch("0.0.0.0", 7999))


if __name__ == "__main__":
    entry_point()
