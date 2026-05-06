import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://www.examcompass.com"

EXAM_PAGES = [
    "/comptia-cysa-plus-practice-tests",
    "/comptia-security-plus-practice-tests",
    "/comptia-network-plus-practice-tests",
    "/comptia-a-plus-practice-tests",
    "/comptia-casp-plus-practice-tests",
    "/comptia-pentest-plus-practice-tests"
]

EXAM_MAP = {
    "cysa": "CySA+",
    "security": "Security+",
    "network": "Network+",
    "a-plus": "A+",
    "casp": "CASP+",
    "pentest": "PenTest+"
}

def get_exam_tag(url):
    for key, tag in EXAM_MAP.items():
        if key in url:
            return tag
    return "General"

def scrape_page(path):
    url = BASE_URL + path
    results = []

    try:
        response = requests.get(url, headers={"User-Agent": "comptia-hub-scraper/1.0"})
        soup = BeautifulSoup(response.text, "html.parser")

        # Grab all practice test links on the page
        for link in soup.find_all("a", href=True):
            href = link["href"]
            text = link.get_text(strip=True)

            if "practice-test" in href and text:
                full_url = BASE_URL + href if href.startswith("/") else href
                results.append({
                    "title": f"ExamCompass: {text}",
                    "url": full_url,
                    "description": f"Free CompTIA practice test — {text}",
                    "source": "ExamCompass",
                    "score": 0,
                    "exams": [get_exam_tag(path)]
                })

    except Exception as e:
        print(f"  Error scraping {url}: {e}")

    return results

def run():
    all_results = []

    for page in EXAM_PAGES:
        print(f"Scraping {page}...")
        results = scrape_page(page)

        # Deduplicate within page
        seen = set()
        unique = []
        for r in results:
            if r["url"] not in seen:
                seen.add(r["url"])
                unique.append(r)

        all_results.extend(unique)
        print(f"  Found {len(unique)} practice tests")
        time.sleep(1)

    output_path = "../data/examcompass_resources.json"
    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\nDone! Saved {len(all_results)} resources to {output_path}")

if __name__ == "__main__":
    run()
