from bs4 import BeautifulSoup
import requests
import json
from urllib.parse import urljoin
from requests.exceptions import RequestException

BASE_URL = "https://www.tamilvu.org"
URL = "https://www.tamilvu.org/ta/library-libcontnt-273141"
JSON_FILE = "GetAuthorNameWithLiks.json"

final_data = {}

try:
    response = requests.get(URL, timeout=15)
    response.raise_for_status()
except RequestException as e:
    print(f"❌ Failed to load main page: {e}")
    exit()

try:
    soup = BeautifulSoup(response.text, "html.parser")
    unorder_list = soup.find('ul', {"class": "treeview", "id": "tree2"})
except Exception as e:
    print(f"❌ HTML parsing failed: {e}")
    exit()

if not unorder_list:
    print("❌ Author list not found")
    exit()

for li in unorder_list.find_all('li'):
    try:
        a_tag = li.find('a')
        if not a_tag or not a_tag.get('href'):
            continue

        author_name = a_tag.text.strip()
        author_link = urljoin(BASE_URL, a_tag['href'])

        try:
            author_page = requests.get(author_link, timeout=15)
            author_page.raise_for_status()
        except RequestException:
            print(f"⚠️ Skipping author (page error): {author_link}")
            continue

        author_soup = BeautifulSoup(author_page.text, "html.parser")
        book_div = author_soup.find('div', id="AutoNumber1")

        if not book_div:
            print(f"⚠️ No books found for {author_name}")
            continue

        books = []
        for book in book_div.find_all('a', href=True):
            try:
                book_name = book.text.strip()
                book_link = urljoin(BASE_URL, book['href'])

                books.append({
                    "book_name": book_name,
                    "pdf_link": book_link
                })
            except Exception:
                continue

        if books:
            final_data[f"{author_name}-link"] = author_link
            final_data[author_name] = books

        print(f"✅ Processed author: {author_name}")

    except Exception as e:
        print(f"❌ Unexpected error for author block: {e}")
        continue

try:
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    print(f"\n✅ Data successfully written to {JSON_FILE}")
except IOError as e:
    print(f"❌ Failed to write JSON file: {e}")
