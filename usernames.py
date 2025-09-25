# usernames.py
import urllib.parse
import re

def _clean_input(username: str) -> str:
    if username is None:
        return ""
    return username.strip()

def _slug_for_profile(u: str) -> str:
    """Remove internal spaces for direct-profile slugs (john doe -> johndoe)."""
    return re.sub(r"\s+", "", u)

def username_osint_links(username: str) -> dict:
    """
    Return flat dict {site: url} for a username.
    - Search links use quote_plus (spaces -> +)
    - Direct-profile slugs remove spaces
    """
    u = _clean_input(username)
    if not u:
        return {"error": "Empty username"}

    slug = _slug_for_profile(u)
    enc = urllib.parse.quote_plus(u)
    enc_raw = urllib.parse.quote(u)

    return {
        # Search engines
        "google": f"https://www.google.com/search?q={enc}",
        "bing": f"https://www.bing.com/search?q={enc}",
        "duckduckgo": f"https://duckduckgo.com/?q={enc}",
        "yandex": f"https://yandex.com/search/?text={enc}",
        "baidu": f"https://www.baidu.com/s?wd={enc}",

        # Code hosts & developer platforms
        "github_profile": f"https://github.com/{slug}",
        "github_search": f"https://github.com/search?q={enc}",
        "gist": f"https://gist.github.com/{slug}",
        "gitlab": f"https://gitlab.com/{slug}",
        "bitbucket": f"https://bitbucket.org/{slug}",
        "npm_profile": f"https://www.npmjs.com/~{slug}",
        "pypi_search": f"https://pypi.org/search/?q={enc}",

        # Social networks (direct or search where appropriate)
        "x_profile": f"https://x.com/{slug}",
        "instagram": f"https://www.instagram.com/{slug}",
        "facebook_search": f"https://www.google.com/search?q=site:facebook.com+%22{enc}%22",
        "linkedin_search": f"https://www.google.com/search?q=site:linkedin.com+%22{enc}%22",
        "tiktok": f"https://www.tiktok.com/@{slug}",
        "youtube": f"https://www.youtube.com/results?search_query={enc}",
        "pinterest": f"https://www.pinterest.com/search/pins/?q={enc}",
        "snapchat_search": f"https://www.google.com/search?q=site:snapchat.com+%22{enc}%22",

        # Community / forums / Q&A
        "reddit_user": f"https://www.reddit.com/user/{slug}",
        "reddit_search": f"https://www.reddit.com/search/?q={enc}",
        "stackoverflow_search": f"https://stackoverflow.com/search?q={enc}",
        "stackexchange_search": f"https://stackexchange.com/search?q={enc_raw}",
        "hn_algolia": f"https://hn.algolia.com/?query={enc}&sort=byDate",
        "quora": f"https://www.quora.com/search?q={enc}",
        "discourse_search": f"https://www.google.com/search?q=site:discourse.org+%22{enc}%22",
        "phpbb_vbulletin_xenforo": f"https://www.google.com/search?q=site:phpbb.com+OR+site:vbulletin.com+OR+site:xenforo.com+%22{enc}%22",
        "4chan_archive": f"https://archive.4plebs.org/_/search/text/{enc}/order/asc/",

        # Paste / leaks / archives
        "pastebin_search": f"https://www.google.com/search?q=site:pastebin.com+%22{enc}%22",
        "paste_combined": f"https://www.google.com/search?q=site:paste.ee+OR+site:ghostbin.com+OR+site:privatebin.net+%22{enc}%22",
        "mailing_lists": f"https://groups.google.com/groups/search?q={enc}",
        "mail_archive": f"https://www.mail-archive.com/search?l=&q={enc}",
        "wayback": f"https://web.archive.org/web/*/{enc}",

        # Marketplaces / portfolios / creative
        "behance": f"https://www.behance.net/{slug}",
        "dribbble": f"https://dribbble.com/{slug}",
        "fiverr": f"https://www.fiverr.com/{slug}",
        "upwork_search": f"https://www.google.com/search?q=site:upwork.com+%22{enc}%22",
        "freelancer_search": f"https://www.google.com/search?q=site:freelancer.com+%22{enc}%22",

        # Audio / streaming / gaming
        "soundcloud": f"https://soundcloud.com/{slug}",
        "twitch": f"https://www.twitch.tv/{slug}",
        "goodreads": f"https://www.goodreads.com/search?q={enc}",

        # Blogs / articles / dev blogs
        "medium_search": f"https://www.google.com/search?q=site:medium.com+%22{enc}%22",
        "devto": f"https://dev.to/{slug}",
        "hashnode": f"https://hashnode.com/@{slug}",

        # Messaging / federated / smaller platforms
        "telegram_tme": f"https://t.me/{slug}",
        "mastodon_search": f"https://mastodon.social/api/v2/search?q={enc}&limit=40&type=accounts",
        "vk_search": f"https://www.google.com/search?q=site:vk.com+%22{enc}%22",

        # Job / professional / academic
        "linkedin_profile_search": f"https://www.google.com/search?q=site:linkedin.com+%22{enc}%22",
        "researchgate": f"https://www.researchgate.net/search?q={enc}",
        "scholar_search": f"https://scholar.google.com/scholar?q={enc}",

        # Darkweb / onion proxies (public frontends)
        "ahmia": f"https://ahmia.fi/search/?q={enc}",
        "darksearch": f"https://darksearch.io/search?query={enc}",
        "onion_rip": f"https://onion.rip/search?q={enc}",

        # Combined quick dorks
        "flat_sites_dork": f"https://www.google.com/search?q=site:github.com+OR+site:gitlab.com+OR+site:reddit.com+OR+site:pastebin.com+%22{enc}%22"
    }
