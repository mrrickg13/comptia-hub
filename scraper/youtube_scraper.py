import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

SEARCH_TERMS = [
    "CySA+ study guide",
    "CySA+ practice questions",
    "CompTIA Security+ free course",
    "Security+ full course",
    "Network+ study guide",
    "CompTIA A+ course free",
    "CASP+ study",
    "PenTest+ course"
]

def search_youtube(query, max_results=10):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "relevanceLanguage": "en",
        "key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    results = []
    for item in data.get("items", []):
        video_id = item["id"]["videoId"]
        snippet = item["snippet"]
        results.append({
            "title": snippet["title"],
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "description": snippet["description"][:200],
            "source": "YouTube",
            "score": 0,
            "topic": query
        })

    return results

def run():
    all_results = []

    for term in SEARCH_TERMS:
        print(f"Searching: {term}")
        results = search_youtube(term)
        all_results.extend(results)
        print(f"  Found {len(results)} videos")

    # Deduplicate by URL
    seen = set()
    unique = []
    for r in all_results:
        if r["url"] not in seen:
            seen.add(r["url"])
            unique.append(r)

    output_path = "../data/youtube_resources.json"
    with open(output_path, "w") as f:
        json.dump(unique, f, indent=2)

    print(f"\nDone! Saved {len(unique)} videos to {output_path}")

if __name__ == "__main__":
    run()
