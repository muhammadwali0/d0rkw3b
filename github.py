import urllib.parse


def gh_user_links(username):
    
    encoded_user = urllib.parse.quote_plus(username.strip())
    base = f"https://github.com/{encoded_user}"
    return {
        
        "Search Users": f"https://github.com/search?q={encoded_user}&type=users",
    }


def gh_repo_search(repo_name):
    """Search repositories by repo name only."""
    q = urllib.parse.quote_plus(repo_name.strip())
    return {
        "Search Repositories": f"https://github.com/search?q={q}&type=repositories",
        "Search Code": f"https://github.com/search?q={q}&type=code",
        "Search Issues": f"https://github.com/search?q={q}&type=issues",
        "Search Discussions": f"https://github.com/search?q={q}&type=discussions",
        "Search Topics": f"https://github.com/search?q={q}&type=topics",
    }


def gh_search_links(term):
    """General GitHub search links (users, repos, code)."""
    q = urllib.parse.quote_plus(term.strip())
    return {
        "Repositories": f"https://github.com/search?q={q}&type=repositories",
        "Code": f"https://github.com/search?q={q}&type=code",
        "Users": f"https://github.com/search?q={q}&type=users",
        "Issues": f"https://github.com/search?q={q}&type=issues",
        "Discussions": f"https://github.com/search?q={q}&type=discussions",
        "Packages": f"https://github.com/search?q={q}&type=packages",
        "Topics": f"https://github.com/search?q={q}&type=topics",
    }