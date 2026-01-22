import requests
import json
import os
import re
import time

# ================= CONFIG =================

JSON_FILE = "GetAuthorNameWithLiks.json"
DOWNLOAD_DIR = "tamilvu_books"
METADATA_FILE = os.path.join(DOWNLOAD_DIR, "metadata.json")

TIMEOUT = 30
RETRIES = 3
CHUNK_SIZE = 1024 * 64  # 64 KB

# ================= HELPERS =================

def safe_name(name: str) -> str:
    """Sanitize folder names (author names only)"""
    name = name.strip()
    name = re.sub(r'[\\/:*?"<>|]', "", name)
    name = re.sub(r"\s+", " ", name)
    return name


def load_metadata():
    """Load metadata safely"""
    if not os.path.exists(METADATA_FILE):
        return {}

    try:
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        print("⚠️ Corrupted metadata.json detected. Resetting it.")
        return {}


def save_metadata(metadata: dict):
    """Save metadata correctly (overwrite, NOT append)"""
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)


def download_pdf(url, file_path):
    """Download PDF with progress and retry support"""

    if os.path.exists(file_path):
        print(f"⏭️ Already exists: {os.path.basename(file_path)}")
        return "skipped"

    for attempt in range(1, RETRIES + 1):
        try:
            with requests.get(url, stream=True, timeout=TIMEOUT) as r:
                r.raise_for_status()

                total_size = int(r.headers.get("content-length", 0))
                downloaded = 0
                start_time = time.time()

                with open(file_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
                        if not chunk:
                            continue

                        f.write(chunk)
                        downloaded += len(chunk)

                        if total_size:
                            percent = downloaded * 100 / total_size
                            speed = downloaded / (time.time() - start_time + 0.01)

                            print(
                                f"\r⬇️ {percent:6.2f}% | "
                                f"{downloaded // 1024} KB | "
                                f"{speed / 1024:.1f} KB/s",
                                end="",
                                flush=True
                            )

                print(f"\n✅ Downloaded: {os.path.basename(file_path)}")
                return "downloaded"

        except requests.exceptions.RequestException as e:
            print(f"\n⚠️ Attempt {attempt}/{RETRIES} failed: {e}")
            time.sleep(2)

    print(f"❌ Failed: {os.path.basename(file_path)}")
    return "failed"

# ================= MAIN =================

def main():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # Load book list JSON
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ Book JSON file not found")
        return
    except json.JSONDecodeError:
        print("❌ Invalid book JSON format")
        return

    start = input("Start downloading books? (y/N): ").strip().lower()
    if start not in ("y", "yes"):
        print("🚫 Program exited")
        return

    metadata = load_metadata()
    stats = {"downloaded": 0, "skipped": 0, "failed": 0}

    # Continue numbering
    book_counter = len(metadata) + 1

    try:
        for author, books in data.items():
            if str(author).endswith("-link"):
                continue

            if not books:
                print(f"⚠️ No books for author: {author}")
                continue

            author_name = safe_name(author)
            author_dir = os.path.join(DOWNLOAD_DIR, author_name)
            os.makedirs(author_dir, exist_ok=True)

            choice = input(
                f"\n👤 Author: {author_name}\n"
                "Download this author's books? (y = yes / n = skip / q = quit): "
            ).strip().lower()

            if choice in ("q", "quit", "exit"):
                print("🚫 Download cancelled")
                break

            if choice not in ("y", "yes"):
                print(f"⏭️ Skipped author: {author_name}")
                continue

            for book in books:
                title = book.get("book_name", "").strip()
                pdf_link = book.get("pdf_link", "").strip()

                if not title or not pdf_link:
                    print("⚠️ Missing book title or PDF link")
                    continue

                book_id = f"book_{book_counter:04d}"
                file_path = os.path.join(author_dir, f"{book_id}.pdf")

                print(f"\n📘 {title}")

                result = download_pdf(pdf_link, file_path)
                stats[result] += 1

                if result == "downloaded":
                    metadata[book_id] = {
                        "title": title,       # FULL TAMIL TITLE
                        "author": author,
                        "file": file_path,
                        "pdf_link": pdf_link
                    }
                    save_metadata(metadata)
                    book_counter += 1

    except KeyboardInterrupt:
        print("\n⛔ Download interrupted by user")

    print("\n📊 Download Summary")
    print("────────────────────")
    print(f"✅ Downloaded : {stats['downloaded']}")
    print(f"⏭️ Skipped     : {stats['skipped']}")
    print(f"❌ Failed      : {stats['failed']}")
    print("🎉 Done!")


if __name__ == "__main__":
    main()
