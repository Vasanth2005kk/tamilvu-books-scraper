# 📚 TamilVu Books Scraper

A Python-based tool to scrape and download Tamil books from [TamilVu.org](https://www.tamilvu.org), a digital library of Tamil literature.

## 🎯 What Does This Project Do?

This project helps you:
1. **Scrape** author names and book links from TamilVu.org
2. **Download** Tamil books (PDFs) organized by author
3. **Track** download progress with metadata

## 📋 Prerequisites

Before running this project, make sure you have:

- **Python 3.7+** installed
- **pip** (Python package manager)
- Internet connection

## 🚀 Quick Start

### Step 1: Clone This Repository

```bash
# Clone the repository
git clone https://github.com/Vasanth2005kk/tamilvu-books-scraper.git

# Navigate to the project directory
cd tamilvu-books-scraper
```

### Step 2: Set Up Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # On Linux/Mac
# OR
.venv\Scripts\activate  # On Windows
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Scraper

First, scrape the author names and book links:

```bash
python get-authornames.py
```

This will create a file called `GetAuthorNameWithLiks.json` containing all authors and their books.

### Step 5: Download Books

Now download the books:

```bash
python main.py
```

The script will:
- Ask for confirmation before starting
- Let you choose which authors to download
- Show download progress with speed and percentage
- Save books in the `tamilvu_books/` folder organized by author

## 📁 Project Structure

```
download-books/
├── get-authornames.py          # Scrapes author names and book links
├── main.py                     # Downloads books from the scraped data
├── GetAuthorNameWithLiks.json  # Generated: Author and book data
├── example.json                # Sample data structure
├── tamilvu_books/              # Downloaded books folder
│   ├── metadata.json           # Tracks downloaded books
│   ├── Author Name 1/
│   │   ├── book_0001.pdf
│   │   └── book_0002.pdf
│   └── Author Name 2/
│       └── book_0003.pdf
└── README.md                   # This file
```

## 🛠️ How It Works

### 1. **get-authornames.py**
- Visits the TamilVu library page
- Extracts all author names and their profile links
- For each author, scrapes their book titles and PDF links
- Saves everything to `GetAuthorNameWithLiks.json`

### 2. **main.py**
- Reads `GetAuthorNameWithLiks.json`
- Creates organized folders for each author
- Downloads PDFs with:
  - ✅ Progress tracking (percentage, speed)
  - ✅ Retry mechanism (3 attempts)
  - ✅ Resume capability (skips existing files)
  - ✅ Metadata tracking
- Saves metadata in `tamilvu_books/metadata.json`

## 📊 Features

- ✅ **Interactive Download**: Choose which authors to download
- ✅ **Progress Tracking**: Real-time download speed and percentage
- ✅ **Resume Support**: Automatically skips already downloaded books
- ✅ **Error Handling**: Retries failed downloads up to 3 times
- ✅ **Organized Storage**: Books sorted by author in separate folders
- ✅ **Metadata Tracking**: JSON file tracks all downloaded books with titles and links
- ✅ **Safe File Naming**: Automatically sanitizes author names for folder creation

## ⚙️ Configuration

You can modify these settings in `main.py`:

```python
JSON_FILE = "GetAuthorNameWithLiks.json"  # Source data file
DOWNLOAD_DIR = "tamilvu_books"             # Download folder
TIMEOUT = 30                               # Request timeout (seconds)
RETRIES = 3                                # Download retry attempts
CHUNK_SIZE = 1024 * 64                     # Download chunk size (64 KB)
```

## 📝 Example Usage

```bash
# Step 1: Scrape authors and books
$ python get-authornames.py
✅ Processed author: கண்ணதாசன்
✅ Processed author: பாரதியார்
✅ Data successfully written to GetAuthorNameWithLiks.json

# Step 2: Download books
$ python main.py
Start downloading books? (y/N): y

👤 Author: கண்ணதாசன்
Download this author's books? (y = yes / n = skip / q = quit): y

📘 கவிதைகள் தொகுப்பு
⬇️  45.23% | 1024 KB | 128.5 KB/s
✅ Downloaded: book_0001.pdf

📊 Download Summary
────────────────────
✅ Downloaded : 15
⏭️ Skipped     : 3
❌ Failed      : 0
🎉 Done!
```

## 🐛 Troubleshooting

### Problem: "Module not found" error
**Solution**: Install dependencies
```bash
pip install requests beautifulsoup4
```

### Problem: Download fails repeatedly
**Solution**: 
- Check your internet connection
- The TamilVu server might be slow or down
- Try increasing `TIMEOUT` in `main.py`

### Problem: "Corrupted metadata.json detected"
**Solution**: The script will automatically reset it. Your existing PDFs are safe.

## 📜 License

This project is for educational purposes. Please respect TamilVu.org's terms of service and use responsibly.

## 🤝 Contributing

Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## ⚠️ Disclaimer

This tool is for personal use and educational purposes only. Please:
- Respect the source website's bandwidth
- Don't use for commercial purposes
- Follow TamilVu.org's terms of service

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Review the error messages carefully
3. Make sure all dependencies are installed

---

**Happy Reading! 📖✨**
