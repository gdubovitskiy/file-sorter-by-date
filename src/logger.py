from datetime import datetime
from pathlib import Path


def init_logger(log_file: Path) -> None:
    """Инициализация логгера с созданием родительских директорий"""
    log_file.parent.mkdir(parents=True, exist_ok=True)
    if log_file.exists():
        log_file.unlink()


def log_message(message: str, log_file: Path) -> None:
    """Запись сообщения в лог"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
