import json
import sys
import urllib.request

REGISTRY_URL = "https://hub.docker.com/v2/repositories/library/nextcloud/tags/?page_size=100"

def fetch_tags(variant: str, prefixes: list[str]) -> list[dict]:
    data = []
    with urllib.request.urlopen(REGISTRY_URL) as response:
        data = json.loads(response.read())

    # Filter to matching tags
    matching = [
        result for result in data["results"]
        if result["name"].endswith(variant)
        and any(result["name"].startswith(f"{prefix}") for prefix in prefixes)
    ]

    # Group by digest, collecting all tag names per digest
    by_digest = {}
    for result in matching:
        digest = result["digest"]
        if digest not in by_digest:
            by_digest[digest] = {"digest": digest, "tags": []}
        by_digest[digest]["tags"].append(result["name"])

    return list(by_digest.values())


if __name__ == "__main__":
    variant = sys.argv[1]
    prefixes = json.loads(sys.argv[2])

    groups = fetch_tags(variant, prefixes)
    print(json.dumps(groups))