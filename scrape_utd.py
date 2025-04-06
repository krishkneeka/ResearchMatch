import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://profiles.utdallas.edu"
BROWSE_URL = f"{BASE_URL}/browse"
HEADERS = {"User-Agent": "Mozilla/5.0"}

all_professors = []

# Loop through the first N pages
for page in range(1, 53):  # Increase range as needed
    print(f"Scraping page {page}")
    response = requests.get(f"{BROWSE_URL}?page={page}", headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    people = soup.select('div.media-body')  # Container holding each profile

    for person in people:
        try:
            link_tag = person.find('a', href=True)
            if not link_tag:
                continue

            name = link_tag.text.strip()
            profile_path = link_tag['href'].strip()
            profile_url = BASE_URL + profile_path

            title = person.find('p').text.strip()

            # Now get profile image and tags from profile page
            profile_response = requests.get(profile_url, headers=HEADERS)
            profile_soup = BeautifulSoup(profile_response.text, 'html.parser')

            img_tag = profile_soup.find('img', class_='profile-image')
            image_url = BASE_URL + img_tag['src'] if img_tag else BASE_URL + "/img/default.png"

            # Try to grab tags from profile page
            tags = []
            tag_elements = profile_soup.select('.tag, .field-of-study a')
            for tag in tag_elements:
                tags.append(tag.text.strip())

            professor_data = {
                "name": name,
                "title": title,
                "profileUrl": profile_url,
                "image": image_url,
                "tags": tags
            }

            all_professors.append(professor_data)
        
        except Exception as e:
            print(f"Error scraping a profile: {e}")

# Save to JSON
with open("professors.json", "w", encoding='utf-8') as f:
    json.dump(all_professors, f, indent=2)
