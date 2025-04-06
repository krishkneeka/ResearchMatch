import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://profiles.utdallas.edu"
BROWSE_URL = f"{BASE_URL}/browse"
HEADERS = {"User-Agent": "Mozilla/5.0"}

all_professors = []

for page in range(1, 54):  # 53 total
    print(f"Scraping page {page}")
    res = requests.get(f"{BROWSE_URL}?page={page}", headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    cards = soup.select(".card.profile-card")

    for card in cards:
        try:
            name_tag = card.select_one(".profile-name a")
            title_tag = card.select_one(".profile-title")
            img_tag = card.select_one("img.card-img-top")

            if not name_tag or not title_tag:
                continue

            name = name_tag.get_text(strip=True)
            relative_url = name_tag.get("href", "")
            profile_url = relative_url if relative_url.startswith("http") else BASE_URL + relative_url

            title = title_tag.get_text(strip=True)
            image_url = img_tag["src"].strip()
            if not image_url.startswith("http"):
                image_url = BASE_URL + image_url

            # Now visit the individual profile page for tags
            tags = []
            try:
                profile_res = requests.get(profile_url, headers=HEADERS)
                profile_soup = BeautifulSoup(profile_res.text, "html.parser")

                tag_elements = profile_soup.select(".field-of-study a, .tag")
                tags = [t.get_text(strip=True) for t in tag_elements]

            except Exception as inner_err:
                print(f"⚠️ Couldn’t fetch tags from profile {profile_url}: {inner_err}")

            all_professors.append({
                "name": name,
                "title": title,
                "profileUrl": profile_url,
                "image": image_url,
                "tags": tags
            })

            time.sleep(0.3)  # Be nice to their server

        except Exception as outer_err:
            print(f"❌ Error on page {page}: {outer_err}")

# Save to file
with open("professors_full.json", "w", encoding="utf-8") as f:
    json.dump(all_professors, f, indent=2, ensure_ascii=False)

print("✅ Done scraping. Data saved to professors_full.json")
