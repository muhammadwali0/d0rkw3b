"""Logical groups over existing metadata; definitions remain in one registry."""

PACKS = {
    "core": {"description": "General web discovery", "categories": {"search_links"}},
    "social": {
        "description": "Social profiles and communities",
        "categories": {
            "usernames",
            "facebook",
            "instagram",
            "x",
            "linkedin",
            "communities",
        },
    },
    "infrastructure": {
        "description": "Domains, DNS and IP information",
        "categories": {"domain", "ipaddresses"},
    },
    "development": {
        "description": "Repository and code research",
        "categories": {"github"},
    },
    "documents": {
        "description": "Indexed documents and publications",
        "categories": {"documents"},
    },
    "media": {
        "description": "Image and video investigation paths",
        "categories": {"images", "videos"},
    },
    "email": {"description": "Email research", "categories": {"emailaddresses"}},
    "darkweb": {
        "description": "Tor-only query providers; explicit Tor selection still required",
        "categories": set(),
    },
}


def in_pack(provider, pack):
    if pack not in PACKS:
        return pack in provider.get("packs", [])
    if pack == "darkweb":
        return provider["network"] == "tor"
    return provider["category"] in PACKS[pack]["categories"] or pack in provider.get(
        "packs", []
    )


def packs(providers):
    names = sorted(
        set(PACKS) | {p for item in providers for p in item.get("packs", [])}
    )
    return [
        {
            "id": name,
            "description": PACKS.get(name, {}).get(
                "description", "Contributed provider pack"
            ),
            "providers": sum(in_pack(p, name) for p in providers),
        }
        for name in names
    ]
