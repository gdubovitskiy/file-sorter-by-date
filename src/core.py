import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from tqdm import tqdm

from .logger import log_message


def process_single_file(
    filename: str,
    source_dir: Path,
    dest_dir: Path,
    log_file: Path,
    dry_run: bool = False,
) -> Optional[bool]:
    """
    Process a single file by:
    1. Extracting date from filename (YYYYMMDD_* format)
    2. Creating target directory structure (YYYY/MM)
    3. Moving file to destination

    Args:
        filename: Name of file to process
        source_dir: Source directory Path object
        dest_dir: Destination root directory Path
        log_file: Path to log file
        dry_run: If True, only simulate operation

    Returns:
        bool: True if success, False if error, None if skipped
    """
    try:
        if "_" not in filename:
            return None

        # Extract date from filename
        date_part = filename.split("_")[0]
        date = datetime.strptime(date_part, "%Y%m%d")
        year, month = date.year, f"{date.month:02d}"

        # Prepare destination path
        dest_path = dest_dir / str(year) / month / filename

        if not dry_run:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source_dir / filename), str(dest_path))

        log_message(
            f"{'DRY RUN' if dry_run else 'MOVED'}: {filename} -> {year}/{month}",
            log_file,
        )
        return True

    except ValueError as e:
        log_message(f"ERROR: Invalid date in filename {filename} - {str(e)}", log_file)
        return False
    except Exception as e:
        log_message(f"ERROR: Failed to process {filename} - {str(e)}", log_file)
        return False


def process_files(
    files: List[str],
    source_dir: Path,
    dest_dir: Path,
    workers: int = 8,
    log_file: Path = Path("log.txt"),
    dry_run: bool = False,
) -> None:
    """
    Process files in parallel using ThreadPoolExecutor

    Args:
        files: List of filenames to process
        source_dir: Source directory Path
        dest_dir: Destination directory Path
        workers: Number of worker threads
        log_file: Path to log file
        dry_run: Simulation mode flag
    """
    with tqdm(total=len(files), desc="Processing files") as progress_bar:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(
                    process_single_file,
                    filename,
                    source_dir,
                    dest_dir,
                    log_file,
                    dry_run,
                ): filename
                for filename in files
            }

            for future in as_completed(futures):
                future.result()
                progress_bar.update(1)
                progress_bar.set_postfix_str(f"Last: {futures[future]}", refresh=False)
