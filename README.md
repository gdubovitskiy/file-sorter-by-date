# 📂 File Sorter by Date

**Automatically organize files into `YYYY/MM` folders based on dates in filenames**  
*(Perfect for photos, documents, and any files with `YYYYMMDD_*` pattern)*

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Typer CLI](https://img.shields.io/badge/CLI-Typer-FF4785)](https://typer.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- 🚀 **Parallel processing** with configurable worker threads (4-32)
- 📅 **Smart date detection** from filenames (`YYYYMMDD_*` pattern)
- 📊 **Visual progress tracking** with tqdm
- 🧪 **Dry-run mode** for safe testing
- 📝 **Detailed logging** of all operations
- ✔️ **Automatic directory validation**
- 🛠️ **Error handling** with clear messages

## ⚡ Quick Start

### Prerequisites
- Python 3.10+
- Poetry 1.5+

### Installation
```bash
# Clone repository
git clone https://github.com/gdubovitskiy/file-sorter-by-date.git
cd file-sorter-by-date

# Install dependencies
poetry install
```

### Basic Usage
```bash
# Simple organization
poetry run file-sorter ~/source_folder ~/destination_folder

# With progress display and logging
poetry run file-sorter ~/Photos ~/Sorted --workers 4 --log migration.log
```

### Command Options
```bash
Options:
  --workers, -w INTEGER  Number of parallel threads [4-32] (default: 8)
  --log, -l TEXT         Name of log file (default: log.txt)
  --dry-run              Simulation mode (no actual file moves)
  --help                 Show this message and exit
```

## 🧠 How It Works

1. **Scans** source directory for files matching `YYYYMMDD_*` pattern
2. **Validates** directory permissions and existence
3. **Creates** folder structure `Destination/YYYY/MM/`
4. **Moves** files with parallel processing
5. **Logs** all actions with timestamps

## 🛠️ Project Structure

```
src/
├── cli.py          # Command-line interface (Typer)
├── core.py         # Main processing logic
├── logger.py       # Logging utilities
└── utils.py        # Directory validation
```

## 🐛 Troubleshooting

### Common Issues
1. **"TyperArgument.make_metavar()" error**:
   ```bash
   poetry lock --no-update
   poetry install
   ```

2. **No files found**:
   - Ensure filenames contain dates in `YYYYMMDD_*` format
   - Check source directory permissions

3. **Permission errors**:
   ```bash
   # On Linux/Mac:
   chmod +x src/cli.py
   ```

## 📧 Contact

Dubovitskiy George - [@gdubovitskiy](https://t.me/gdubovitskiy) - gdubovitskiy@ya.ru

---

### 🎯 Example Workflow

```bash
# 1. First do a dry-run
poetry run file-sorter ~/DCIM/Camera ~/Photos/Organized --dry-run

# 2. Check the log
cat sorting_log.txt

# 3. Run for real with 8 threads
poetry run file-sorter ~/DCIM/Camera ~/Photos/Organized --workers 8
```