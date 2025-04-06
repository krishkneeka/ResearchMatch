import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://profiles.utdallas.edu"
BROWSE_URL = f"{BASE_URL}/browse"
HEADERS = {"User-Agent": "Mozilla/5.0"}

all_professors = []

for page in range(1, 54):  # all 53 pages
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

            name = name_tag.text.strip()
            profile_path = name_tag["href"].strip()
            profile_url = profile_path if profile_path.startswith("http") else BASE_URL + profile_path
            title = title_tag.text.strip()
            image_url = img_tag["src"].strip()
            if not image_url.startswith("http"):
                image_url = BASE_URL + image_url

            # Visit profile page for email + tags
            profile_res = requests.get(profile_url, headers=HEADERS)
            profile_soup = BeautifulSoup(profile_res.text, "html.parser")

            # ✨ Extract email
            email_tag = profile_soup.select_one('a[href^="mailto:"]')
            email = ""
            if email_tag:
                href = email_tag.get("href", "")
            if href.startswith("mailto:"):
                email = href.replace("mailto:", "").strip()


            # ✨ Extract tags (if still needed)
            tag_elements = profile_soup.select(".tag, .field-of-study a")
            tags = [tag.text.strip() for tag in tag_elements]

            # Build final professor dict
            all_professors.append({
                "name": name,
                "title": title,
                "profileUrl": profile_url,
                "image": image_url,
                "tags": tags,
                "email": email
            })

            time.sleep(0.3)  # be kind to the server

        except Exception as e:
            print(f"❌ Error: {e}")

# Save to JSON
with open("professors_with_emails.json", "w", encoding="utf-8") as f:
    json.dump(all_professors, f, indent=2, ensure_ascii=False)

print("✅ Done! Data saved to professors_with_emails.json")
