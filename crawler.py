# %%
!pip install requests beautifulsoup4
# %%
import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# %%
BASE = "https://www.bangla-kobita.com"

API = (
    "https://www.bangla-kobita.com/api/getpostbyauthor/"
    "?authorId=5&sectionId=1&skip=0&sortBy=ByViewDesc"
)

OUT = Path("bangla_kobita")
OUT.mkdir(exist_ok=True)

# %%

session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0"
data = session.get(API).json()

with open(OUT / "list.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# %%
# Crawl each poem
for item in data["data"]:
    url = BASE + item["Url"]

    print("Fetching:", url)

    html = session.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    post = soup.select_one(".post-content")
    text = post.get_text("\n", strip=True) if post else ""

    # Save text
    slug = item["Url"].strip("/").split("/")[-1]
    with open(OUT / f"{slug}.txt", "w", encoding="utf-8") as f:
        f.write(text)

print("Done.")
