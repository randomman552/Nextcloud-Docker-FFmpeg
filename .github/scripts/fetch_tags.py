import json
import os
import sys
import urllib.request

REGISTRY_URL = "https://hub.docker.com/v2/repositories/library/nextcloud/tags/?page_size=100"

def fetch_tags(variant: str, prefixes: list[str], registry: str, repository: str) -> list[dict]:
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
            by_digest[digest] = {
                "digest": digest,
                "tags": [],
                "image_tags": [],
            }
        by_digest[digest]["tags"].append(result["name"])
        by_digest[digest]["image_tags"].append(f"{registry}/{repository.lower()}:{result['name']}")

    return list(by_digest.values())


if __name__ == "__main__":
    variant = os.environ["VARIANT"]
    prefixes = json.loads(os.environ["PREFIXES"])
    registry = os.environ["REGISTRY"]
    repository = os.environ["REPOSITORY"]

    groups = fetch_tags(variant, prefixes, registry, repository)
    print(json.dumps(groups))