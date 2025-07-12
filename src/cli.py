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
    log_file: Path = typer.Option(
        "log.txt", "--log", "-l", help="Path to log file"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Simulate without moving files"
    ),
):
    """Sort files from SOURCE to DESTINATION based on dates in filenames (YYYYMMDD_*)."""
    # Создаем полный путь к лог-файлу в целевой директории
    dest_log_path = destination / log_file

    # Явно создаем целевую директорию если её нет
    destination.mkdir(parents=True, exist_ok=True)

    # Инициализируем логгер с полным путем
    init_logger(dest_log_path)

    validate_directories(source, destination)

    files = [f.name for f in source.glob("*_*") if f.is_file()]
    if not files:
        typer.echo("❌ No files matching pattern 'YYYYMMDD_*' found!", err=True)
        raise typer.Exit(1)

    process_files(files, source, destination, workers, log_file, dry_run)
    typer.echo(f"\n✅ Done! Check logs in {log_file}")


if __name__ == "__main__":
    app()
