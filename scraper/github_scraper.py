from github import Github
import json
import os

# We'll add your API key here shortly — for now, unauthenticated works (rate limited)
g = Github()

# CompTIA exam search terms
SEARCH_TERMS = [
    "cysa+ study",
    "cysa practice questions",
    "comptia security+ questions",
    "sec+ study guide",
    "network+ notes",
    "comptia a+ practice",
    "casp+ study"
]

def search_github(query):
    results = []
    repos = g.search_repositories(query=query, sort="stars", order="desc")
    
    for repo in repos[:10]:  # top 10 per search term
        results.append({
            "name": repo.full_name,
            "url": repo.html_url,
            "description": repo.description,
            "stars": repo.stargazers_count,
            "updated": str(repo.updated_at),
            "topic": query
        })
    return results

def run():
    all_results = []
    
    for term in SEARCH_TERMS:
        print(f"Searching: {term}")
        results = search_github(term)
        all_results.extend(results)
        print(f"  Found {len(results)} repos")
    
    # Save to a JSON file in the data folder
    output_path = "../data/github_resources.json"
    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\nDone! Saved {len(all_results)} resources to {output_path}")

if __name__ == "__main__":
    run()
