import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from PIL import Image, UnidentifiedImageError
from PIL.ExifTags import TAGS
from tqdm import tqdm

from .logger import log_message


def get_image_date_exif(filepath: Path) -> Optional[datetime]:
    """Extract date from image EXIF DateTime tag"""
    try:
        with Image.open(filepath) as img:
            exif = img.getexif()
            if exif:
                for tag_id, value in exif.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == "DateTime" and value:
                        return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except (UnidentifiedImageError, AttributeError, ValueError):
        return None
    return None


def parse_filename_date(filename: str) -> Optional[datetime]:
    """Try multiple date formats from filename with enhanced pattern matching"""
    base_name = Path(filename).stem
    date_formats = [
        "%Y-%m-%d %H.%M.%S",  # 2014-07-09 21.46.17
        "%Y%m%d_%H%M%S",  # 20201231_235959
        "%Y%m%d",  # 20201231
        "%Y-%m-%d",  # 2020-12-31
        "%d.%m.%Y",  # 31.12.2020
        "%m%d%Y",  # 12312020 (US format)
        "%Y_%m_%d",  # 2020_12_31
        "%Y%m%d%H%M%S",  # 20201231235959
    ]

    clean_name = (
        base_name.replace(" ", "").replace("-", "").replace("_", "").replace(".", "")
    )
    for fmt in ["%Y%m%d%H%M%S", "%Y%m%d"]:
        try:
            return datetime.strptime(clean_name[: len(fmt)].ljust(len(fmt), "0"), fmt)
        except ValueError:
            continue

    for fmt in date_formats:
        try:
            return datetime.strptime(base_name[: len(fmt)], fmt)
        except ValueError:
            continue

    return None


def process_single_file(
    filename: str,
    source_dir: Path,
    dest_dir: Path,
    log_file: Path,
    copy: bool = False,
    dry_run: bool = False,
) -> Optional[bool]:
    """Process file by date from EXIF or filename with enhanced logging"""
    try:
        filepath = source_dir / filename

        date = get_image_date_exif(filepath)
        source = "EXIF"

        if date is None:
            date = parse_filename_date(filename)
            if date is None:
                log_message(f"SKIPPED: No date found in {filename}", log_file)
                return None
            source = "filename"

        year, month = date.year, f"{date.month:02d}"
        dest_path = dest_dir / str(year) / month / filename

        if not dry_run:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            if copy:
                shutil.copy(str(filepath), str(dest_path))  # Copy file
            else:
                shutil.move(str(filepath), str(dest_path))  # Move file

        status = 'DRY RUN' if dry_run else 'MOVED' if not copy else 'COPIED'
        log_message(f"{status:<10} ({source:^10}): {filename:<30} -> {year}/{month}", log_file, )
        return True

    except Exception as e:
        log_message(f"ERROR processing {filename}: {str(e)}", log_file)
        return False


def process_files(
    files: List[str],
    source_dir: Path,
    dest_dir: Path,
    workers: int = 8,
    log_file: Path = Path("log.txt"),
    copy: bool = False,
    dry_run: bool = False,
) -> None:
    """Process files in parallel with progress tracking"""
    with tqdm(total=len(files), desc="Processing files") as pbar:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(
                    process_single_file,
                    filename,
                    source_dir,
                    dest_dir,
                    log_file,
                    copy,
                    dry_run,
                ): filename
                for filename in files
            }

            for future in as_completed(futures):
                future.result()
                pbar.update(1)
                pbar.set_postfix_str(f"Last: {futures[future]}", refresh=False)
