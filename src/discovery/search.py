from typing import Dict, List
from .keyword_gen import generate_keywords


def search_channels(keyword: str) -> List[Dict]:
    "Search Eitaa for channels matching a keyword"
    # FIX: use AI and Eitaa API later
    return [
        {
            "id": f"channel_{keyword}_1",
            "username": f"{keyword}_shop"
        },
        {
            "id": "channel_2",
            "username": "the_world_news"
        }
    ]


def discover_channels() -> List[Dict]:
    "Discover candidate channels using generated keywords"
    discovered = []
    keywords = generate_keywords()

    for kw in keywords:
        channels = search_channels(kw)
        discovered.extend(channels)

    return discovered
