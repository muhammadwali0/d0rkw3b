
import urllib.parse

def x_username_links(username):
    encoded = urllib.parse.quote_plus(username)
    return {
        "Profile": f"https://x.com/{username}",
        "Outgoing Tweets": f"https://x.com/search?q=from%3A{encoded}&f=live",
        "Incoming Tweets": f"https://x.com/search?q=to%3A{encoded}&f=live",
        "Only Replies": f"https://x.com/search?q=from%3A{encoded}%20filter%3Areplies&src=typed_query&f=live",
        "No Replies": f"https://x.com/search?q=from%3A{encoded}%20-filter%3Areplies&src=typed_query&f=live",
        "Media Tweets": f"https://x.com/{username}/media/",
        "Highlighted Tweets": f"https://x.com/{username}/highlights/",
        "Lists Created": f"https://x.com/{username}/lists/",
        "Lists Included": f"https://x.com/{username}/lists/memberships",
        "Topics": f"https://x.com/{username}/topics",
        "Links": f"https://x.com/search?q=from%3A{encoded}%20filter%3Alinks&src=typed_query&f=live",
        "Followers": f"https://x.com/{username}/followers",
        "Following": f"https://x.com/{username}/following",
        "Google Archives": f"https://www.google.com/search?q=site%3Atwitter.com%2F{encoded}",
        "Google Tweets": f"https://www.google.com/search?q=site%3Atwitter.com%2F{encoded}%2Fstatus%2F",
        "Bing Archives": f"https://www.bing.com/search?q=twitter.com/{encoded}",
        "Yandex Archives": f"https://www.yandex.com/search/?text=https%3A%2F%2Ftwitter.com%2F{encoded}&lr=10615",
        "Wayback Machine": f"https://web.archive.org/web/20250000000000*/twitter.com/{encoded}",
        "Historical": f"https://api.memory.lol/v1/tw/{encoded}",
        "Twitter Audit": f"https://www.twitteraudit.com/result/{encoded}"
    }

def x_username_by_year(username, year):
    encoded = urllib.parse.quote_plus(username)
    return {
        "Outgoing by Year": f"https://x.com/search?q=from%3A{encoded}%20since%3A{year}-01-01%20until%3A{year}-12-31&src=typd&f=live",
        "Incoming by Year": f"https://x.com/search?q=to%3A{encoded}%20since%3A{year}-01-01%20until%3A{year}-12-31&src=typd&f=live",
        "Media by Year": f"https://x.com/search?q=from%3A{encoded}%20since%3A{year}-01-01%20until%3A{year}-12-31%20filter%3Amedia&src=typd&f=live",
        "Term by Year": f"https://x.com/search?q={encoded}%20since%3A{year}-01-01%20until%3A{year}-12-31&src=typd&f=live",
        "No replies by Year": f"https://x.com/search?q=from%3A{encoded}%20since%3A{year}-01-01%20until%3A{year}-12-31%20-filter%3Areplies&src=typd&f=live",
        "Only Replies by Year": f"https://x.com/search?q=from%3A{encoded}%20since%3A{year}-01-01%20until%3A{year}-12-31%20filter%3Areplies&src=typd&f=live"
    }

def x_user_id_links(user_id):
    return {"Historical": f"https://api.memory.lol/v1/tw/id/{user_id}"}

def x_real_name_links(real_name):
    encoded = urllib.parse.quote_plus(real_name)
    return {"Profile": f"https://x.com/search?q={encoded}&f=user"}

def x_list_links(list_id):
    return {
        "List": f"https://x.com/i/lists/{list_id}",
        "List Members": f"https://x.com/i/lists/{list_id}/members",
        "List Followers": f"https://x.com/i/lists/{list_id}/followers"
    }
