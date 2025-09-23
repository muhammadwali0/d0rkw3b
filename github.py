# github.py
import urllib.parse

# -----------------------
# GitHub User Links
# -----------------------
def gh_user_links(username):
    """Return common GitHub links for a user/profile."""
    base = f"https://github.com/{username}"
    return {
        "Profile": base,
        "Repositories": f"{base}?tab=repositories",
        "Stars": f"{base}?tab=stars",
        "Followers": f"{base}?tab=followers",
        "Following": f"{base}?tab=following",
        "Gists": f"https://gist.github.com/{username}",
        "Contributions (graph)": f"{base}?tab=contributions",
    }

# -----------------------
# GitHub Repo Links
# -----------------------
def gh_repo_links(owner, repo):
    """Return common links for a repository."""
    base = f"https://github.com/{owner}/{repo}"
    return {
        "Repository": base,
        "Issues": f"{base}/issues",
        "Pull Requests": f"{base}/pulls",
        "Commits": f"{base}/commits",
        "Branches": f"{base}/branches",
        "Releases": f"{base}/releases",
        "Actions (CI)": f"{base}/actions",
        "Wiki": f"{base}/wiki",
        "Insights": f"{base}/pulse",
    }

# -----------------------
# GitHub Search Links
# -----------------------
def gh_search_links(term):
    """General GitHub search links (users, repos, code)."""
    q = urllib.parse.quote_plus(term)
    return {
        "Repositories": f"https://github.com/search?q={q}&type=repositories",
        "Code": f"https://github.com/search?q={q}&type=code",
        "Users": f"https://github.com/search?q={q}&type=users",
        "Issues": f"https://github.com/search?q={q}&type=issues",
        "Discussions": f"https://github.com/search?q={q}&type=discussions",
        "Packages": f"https://github.com/search?q={q}&type=packages",
        "Topics": f"https://github.com/search?q={q}&type=topics",
    }
