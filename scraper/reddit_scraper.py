import requests
import json
import time

HEADERS = {"User-Agent": "comptia-hub-scraper/1.0"}

SUBREDDITS = [
    "CompTIA",
    "cybersecurity",
    "ITCareerQuestions"
]

KEYWORDS = [
    "cysa", "security+", "sec+", "network+",
    "comptia", "study guide", "free resources",
    "practice questions", "notes", "passed"
]

def is_relevant(post):
    text = (post["title"] + " " + post.get("selftext", "")).lower()
    return any(kw in text for kw in KEYWORDS)

def scrape_subreddit(subreddit_name, limit=50):
    url = f"https://www.reddit.com/r/{subreddit_name}/top.json?t=year&limit={limit}"
    results = []

    try:
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        posts = data["data"]["children"]

        for post in posts:
            p = post["data"]
            if not is_relevant(p):
                continue

            links = []
            for word in p.get("selftext", "").split():
                if word.startswith("http"):
                    links.append(word)

            results.append({
                "title": p["title"],
                "url": f"https://reddit.com{p['permalink']}",
                "score": p["score"],
                "external_links": links[:5],
                "subreddit": subreddit_name
            })

    except Exception as e:
        print(f"  Error scraping r/{subreddit_name}: {e}")

    return results

def run():
    all_results = []

    for sub in SUBREDDITS:
        print(f"Scraping r/{sub}...")
        results = scrape_subreddit(sub)
        all_results.extend(results)
        print(f"  Found {len(results)} relevant posts")
        time.sleep(2)  # be polite, avoid rate limiting

    output_path = "../data/reddit_resources.json"
    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\nDone! Saved {len(all_results)} posts to {output_path}")

if __name__ == "__main__":
    run()
