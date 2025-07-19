from pathlib import Path

import typer

from .core import process_files
from .logger import init_logger
from .utils import validate_directories

app = typer.Typer()


def validate_path(ctx: typer.Context, value: Path) -> Path:
    if not value.exists() and ctx.params.get("source") is None:
        raise typer.BadParameter(f"Path {value} does not exist")
    return value


@app.command()
def main(
    source: Path = typer.Argument(
        ...,
        help="Source directory with files",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        callback=validate_path,
    ),
    destination: Path = typer.Argument(
        ...,
        help="Target directory for organized files",
        file_okay=False,
        dir_okay=True,
        writable=True,
        resolve_path=True,
        callback=validate_path,
    ),
    workers: int = typer.Option(
        8, "--workers", "-w", help="Number of parallel threads", min=1, max=32
    ),
    log_file: Path = typer.Option("log.txt", "--log", "-l", help="Path to log file"),
    copy: bool = typer.Option(
        False, "--copy", help="Copy files instead of moving them"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Simulate without moving files"
    ),
):
    """Sort files from SOURCE to DESTINATION based on dates in filenames (YYYYMMDD_*)."""
    log_file_path = destination / log_file

    destination.mkdir(parents=True, exist_ok=True)

    init_logger(log_file_path)

    validate_directories(source, destination)

    files = [f.name for f in source.iterdir() if f.is_file()]

    process_files(
        files,
        source,
        destination,
        workers,
        log_file_path,
        copy,
        dry_run,
    )
    typer.echo(f"\n✅ Done! Check logs in {log_file_path}")


if __name__ == "__main__":
    app()
