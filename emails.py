# emails.py
import urllib.parse
import re

def _is_valid_email(email: str) -> bool:
    """Simple email validation: user@domain.tld (no spaces)."""
    if not email or " " in email:
        return False
    pattern = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
    return re.match(pattern, email) is not None

def email_search_links(email: str) -> dict:
    """
    Flat single-link-per-site email search templates.
    Bug-bounty links removed as requested.
    """
    e = (email or "").strip()
    if not _is_valid_email(e):
        return {"error": f"Invalid email: '{email}'"}

    enc = urllib.parse.quote_plus(e)
    enc_raw = urllib.parse.quote(e)

    return {
        # Search engines
        "google": f"https://www.google.com/search?q=%22{enc}%22",
        "bing": f"https://www.bing.com/search?q=%22{enc}%22",
        "duckduckgo": f"https://duckduckgo.com/?q=%22{enc}%22",
        "yandex": f"https://yandex.com/search/?text=%22{enc}%22",
        "baidu": f"https://www.baidu.com/s?wd=%22{enc}%22",

        # Code hosts & repos (single link each)
        "github": f"https://github.com/search?q={enc}",
        "gitlab": f"https://gitlab.com/search?search={enc}",
        "bitbucket": f"https://www.google.com/search?q=site:bitbucket.org+%22{enc}%22",

        # Paste / leaks / breach
        "pastes": f"https://www.google.com/search?q=site:pastebin.com+OR+site:paste.ee+OR+site:ghostbin.com+OR+site:privatebin.net+%22{enc}%22",
        "breaches": f"https://www.google.com/search?q=site:breachdirectory.org+OR+site:dehashed.com+%22{enc}%22",
        "haveibeenpwned": f"https://haveibeenpwned.com/account/{urllib.parse.quote(e)}",
        "wayback": f"https://web.archive.org/web/*/{enc}",

        # Forums & mailing lists & archives
        "reddit": f"https://www.reddit.com/search/?q=%22{enc}%22",
        "hn_algolia": f"https://hn.algolia.com/?query={enc}&sort=byDate&prefix&page=0&dateRange=all&type=all",
        "4plebs": f"https://archive.4plebs.org/_/search/text/{enc}/order/asc/",
        "nabble": f"https://www.google.com/search?q=site:nabble.com+%22{enc}%22",
        "google_groups": f"https://groups.google.com/groups/search?q={enc}",
        "mail_archive": f"https://www.mail-archive.com/search?l=&q={enc}",
        "discourse": f"https://www.google.com/search?q=site:discourse.org+%22{enc}%22",
        "forum_engines": f"https://www.google.com/search?q=site:phpbb.com+OR+site:vbulletin.com+OR+site:xenforo.com+%22{enc}%22",
        "stackexchange": f"https://stackexchange.com/search?q={enc_raw}",
        "stackoverflow": f"https://stackoverflow.com/search?q={enc}",

        # Q&A / blogs / dev platforms
        "quora": f"https://www.quora.com/search?q={enc}",
        "medium": f"https://www.google.com/search?q=site:medium.com+%22{enc}%22",
        "devto": f"https://www.google.com/search?q=site:dev.to+%22{enc}%22",
        "wordpress_blogs": f"https://www.google.com/search?q=site:wordpress.com+%22{enc}%22",

        # Socials (use site:dork where platform blocks)
        "twitter_x": f"https://x.com/search?q=%22{enc}%22&src=typed_query",
        "facebook": f"https://www.google.com/search?q=site:facebook.com+%22{enc}%22",
        "linkedin": f"https://www.google.com/search?q=site:linkedin.com+%22{enc}%22",
        "instagram": f"https://www.google.com/search?q=site:instagram.com+%22{enc}%22",
        "tiktok": f"https://www.google.com/search?q=site:tiktok.com+%22{enc}%22",
        "pinterest": f"https://www.google.com/search?q=site:pinterest.com+%22{enc}%22",
        "youtube": f"https://www.youtube.com/results?search_query={enc}",

        # Messaging / fediverse
        "telegram": f"https://www.google.com/search?q=site:t.me+%22{enc}%22",
        "mastodon": f"https://www.google.com/search?q=site:mastodon.social+%22{enc}%22",
        "vk": f"https://www.google.com/search?q=site:vk.com+%22{enc}%22",

        # Enterprise / Jira / corporate dorks (single)
        "jira_corporate": f"https://www.google.com/search?q=site:atlassian.net+OR+site:example.com+%22{enc}%22",

        # Darkweb / onion proxies
        "ahmia": f"https://ahmia.fi/search/?q={enc}",
        "darksearch": f"https://darksearch.io/search?query={enc}",
        "onion_rip": f"https://onion.rip/search?q={enc}",

        # Quick flat combo dork
        "flat_sites_dork": f"https://www.google.com/search?q=site:github.com+OR+site:gitlab.com+OR+site:reddit.com+OR+site:pastebin.com+%22{enc}%22"
    }



