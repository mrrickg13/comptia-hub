import json
import os

def load_json(path):
    if not os.path.exists(path):
        print(f"  Warning: {path} not found, skipping")
        return []
    with open(path) as f:
        return json.load(f)

def tag_exam(text):
    """Guess which exam a resource is for based on keywords"""
    text = text.lower()
    tags = []
    if any(k in text for k in ["cysa", "cs0", "cys+"]):
        tags.append("CySA+")
    if any(k in text for k in ["security+", "sec+", "sy0"]):
        tags.append("Security+")
    if any(k in text for k in ["network+", "net+", "n10"]):
        tags.append("Network+")
    if any(k in text for k in ["a+", "core 1", "core 2", "1101", "1102"]):
        tags.append("A+")
    if any(k in text for k in ["casp", "cas-"]):
        tags.append("CASP+")
    if any(k in text for k in ["pentest+", "pt0"]):
        tags.append("PenTest+")
    if not tags:
        tags.append("General")
    return tags

def normalize_github(resources):
    normalized = []
    for r in resources:
        text = f"{r.get('name', '')} {r.get('description', '') or ''} {r.get('topic', '')}"
        normalized.append({
            "title": r.get("name"),
            "url": r.get("url"),
            "description": r.get("description") or "No description provided",
            "source": "GitHub",
            "score": r.get("stars", 0),
            "exams": tag_exam(text),
            "external_links": []
        })
    return normalized

def normalize_reddit(resources):
    normalized = []
    for r in resources:
        text = f"{r.get('title', '')} {r.get('subreddit', '')}"
        normalized.append({
            "title": r.get("title"),
            "url": r.get("url"),
            "description": f"Reddit post from r/{r.get('subreddit')} — score: {r.get('score')}",
            "source": "Reddit",
            "score": r.get("score", 0),
            "exams": tag_exam(text),
            "external_links": r.get("external_links", [])
        })
    return normalized

def deduplicate(resources):
    seen = set()
    unique = []
    for r in resources:
        if r["url"] not in seen:
            seen.add(r["url"])
            unique.append(r)
    return unique

def run():
    print("Loading data...")
    github = load_json("../data/github_resources.json")
    reddit = load_json("../data/reddit_resources.json")
    youtube = load_json("../data/youtube_resources.json")
    examcompass = load_json("..data/examcompass_resources.json")

    print(f"  GitHub: {len(github)} resources")
    print(f"  Reddit: {len(reddit)} resources")

    def normalize_generic(resources):
      normalized = []
      for r in resources:
        text = f"{r.get('title', '')} {r.get('description', '')} {r.get('topic', '')}"
        if "exams" not in r:
            r["exams"] = tag_exam(text)
        normalized.append(r)
      return normalized

    normalized = normalize_github(github) + normalize_reddit(reddit) + normalize_generic(youtube) + normalize_generic(examcompass)
    unique = deduplicate(normalized)

    # Sort by score descending
    unique.sort(key=lambda x: x["score"], reverse=True)

    output_path = "../data/all_resources.json"
    with open(output_path, "w") as f:
        json.dump(unique, f, indent=2)

    print(f"\nDone! {len(unique)} unique resources saved to {output_path}")

    # Quick summary
    from collections import Counter
    exam_counts = Counter()
    source_counts = Counter()
    for r in unique:
        source_counts[r["source"]] += 1
        for exam in r.get("exams", ["General"]):
            exam_counts[exam] += 1

    print("\nBy source:")
    for source, count in source_counts.items():
        print(f"  {source}: {count}")

    print("\nBy exam:")
    for exam, count in exam_counts.most_common():
        print(f"  {exam}: {count}")

if __name__ == "__main__":
    run()
