import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://profiles.utdallas.edu"
BROWSE_URL = f"{BASE_URL}/browse?page="
HEADERS = {"User-Agent": "Mozilla/5.0"}

professors = []

for page in range(1, 54):  # All 53 pages
    print(f"Scraping page {page}...")
    response = requests.get(f"{BROWSE_URL}{page}", headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to load page {page}")
        continue
    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.select(".card.profile-card")

    for card in cards:
        name_tag = card.select_one("a")
        title_tag = card.select_one(".card-body")
        img_tag = card.select_one("img")

        name = name_tag.get_text(strip=True) if name_tag else "N/A"
        title = title_tag.get_text(strip=True) if title_tag else "N/A"
        profile_url = BASE_URL + name_tag.get("href", "") if name_tag else "N/A"
        image_url = BASE_URL + img_tag.get("src", "") if img_tag else "N/A"

        professors.append({
            "name": name,
            "title": title,
            "profileUrl": profile_url,
            "image": image_url,
            "tags": []
        })

# Save data
with open("professors.json", "w") as f:
    json.dump(professors, f, indent=2)

print(f"✅ Saved {len(professors)} professor profiles to professors.json")
