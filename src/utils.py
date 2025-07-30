from pathlib import Path
from typing import Any, Optional

import typer


def validate_directories(source: Path, destination: Path) -> None:
    """Проверка директорий."""
    if not source.exists():
        raise FileNotFoundError(f"Директория не найдена: {source}")
    destination.mkdir(parents=True, exist_ok=True)


def print_param(label: str, value: Any, icon: Optional[str] = None, color: Optional[str] = None):
    """Печатает параметр с иконкой и стилем."""
    formatted_label = typer.style(f"{label}:", bold=True)
    formatted_value = typer.style(str(value), fg=color) if color else str(value)
    icon_part = f"{icon}  " if icon else ""
    typer.echo(f"{icon_part}{formatted_label} {formatted_value}")


def validate_path(ctx: typer.Context, value: Path) -> Path:
    if not value.exists() and ctx.params.get("source") is None:
        raise typer.BadParameter(f"🚨 Path {value} does not exist")
    return value
