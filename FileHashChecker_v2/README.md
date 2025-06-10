# 🔐 FileHashChecker_v2

**FileHashChecker** is a Python-based command-line utility to calculate and verify file hash values using various algorithms (SHA-256, SHA-1, MD5, etc.). It supports batch processing, configurable output formats, and future plans include VirusTotal integration and a GUI.

---

## ✅ Features

### 🧩 Core Functions
- Calculate hash value of a single file (default: SHA-256)
- Supports multiple algorithms: SHA-256, SHA-1, MD5, etc.
- Compare calculated hash with a provided hash
- Graceful error handling for invalid paths or hash values
- List available hash algorithms

### 📁 Batch Processing & Output
- Batch verify multiple files by folder path
- Optionally include subdirectories
- Export results to CSV and/or JSON
- Output to both console and file simultaneously

### 📄 Hash List File Support
- Load hash list file (TXT/CSV format) [planned]
- Check for missing files or hashes [planned]

### 🧠 Security Utilities
- Detect different files with same hash (possible duplicate/malware)
- Warn about hash collisions [planned]
- Compare file size and modification time [planned]

### 🌐 VirusTotal Integration (Planned)
- Query VirusTotal using file hash
- Display detection count and threat info
- Manage API key via `.env` or config file

### ⚙️ Config Management (Planned)
- Set default algorithm, output format, and path in `.json` or `.ini`

### 🖥 GUI Mode (Optional)
- Build GUI using Tkinter or PyQt [planned]
- Drag-and-drop file input
- Highlight hash match/mismatch in color

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/FileHashChecker.git
cd FileHashChecker
pip install -r requirements.txt
```

🚀 Usage
Basic usage:
python FileHashChecker.py path/to/file

With options:
python FileHashChecker.py path/to/file -a sha1 -o result.json

Available options:
positional arguments:
  file_path             Path to the file to calculate hash

optional arguments:
  -h, --help            Show this help message and exit
  -a, --algorithm       Select hash algorithm (e.g., sha256, sha1, md5)
  -o, --output          Path to save output (CSV or JSON)
  --list-algorithms     Show available hash algorithms

📚 Example
python FileHashChecker.py example.exe -a sha256

Output:
File: example.exe
Algorithm: SHA-256
Hash: 6a7f3c6f75c...
Match: ✅ (Matched with input hash)

🔐 Future Plans
 VirusTotal API integration

 Full GUI support

 Save/load settings from config

 File integrity monitoring mode

 PyInstaller packaging for standalone .exe

🛡 License
This project is licensed under the MIT License.

📫 Contact
Feel free to open issues or contribute via pull requests.
Project maintained by hanenako