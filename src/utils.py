from pathlib import Path


def validate_directories(source: Path, destination: Path) -> None:
    """Проверка директорий"""
    if not source.exists():
        raise FileNotFoundError(f"Директория не найдена: {source}")
    destination.mkdir(parents=True, exist_ok=True)
