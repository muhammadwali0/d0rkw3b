import urllib.parse

def instagram_username_links(username):
    encoded = urllib.parse.quote_plus(username)
    return {
        "IG Profile": f"https://www.instagram.com/{username}",
        "IG Channels": f"https://www.instagram.com/{username}/channel/",
        "IG Tagged": f"https://www.instagram.com/{username}/tagged/",
        "Outgoing Search": f"https://www.google.com/search?q=site%3Ainstagram.com+%22{encoded}%22",
        "Incoming Search": f"https://www.google.com/search?q=site%3Ainstagram.com+%22@{encoded}%22",
        "Bing Search": f"https://www.bing.com/search?q=site%3Ainstagram.com+%22{encoded}%22",
        "Yandex Search": f"https://yandex.com/search/?text=site%3Ainstagram.com+%22{encoded}%22&lr=10615",
        "X Posts": f"https://www.google.com/search?q=site%3Atwitter.com+%22{encoded}%22+%22instagram.com%2Fp%22",
        "Dumpor Profile": f"https://dumpor.io/v/{username}/",
        "Toolzu Profile": f"https://toolzu.com/profile-analyzer/instagram/?username={username}",
        "Threads": f"https://www.threads.com/@{username}"
    }

def instagram_user_id_links(user_id):
    return {
        "Followers": f"https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={{%22id%22:%22{user_id}%22,%22include_reel%22:true,%22fetch_mutual%22:true,%22first%22:50}}",
        "Following": f"https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables={{%22id%22:%22{user_id}%22,%22include_reel%22:true,%22fetch_mutual%22:false,%22first%22:50}}"
    }

def instagram_username_term_links(username, term):
    encoded_user = urllib.parse.quote_plus(username)
    encoded_term = urllib.parse.quote_plus(term)
    return {
        "User + Term": f"https://www.google.com/search?q=site%3Ainstagram.com+%22{encoded_user}%22+%22{encoded_term}%22"
    }

def instagram_username_association_links(username1, username2):
    encoded_user1 = urllib.parse.quote_plus(username1)
    encoded_user2 = urllib.parse.quote_plus(username2)
    return {
        "Associations": f"https://www.google.com/search?q=site%3Ainstagram.com+%22{encoded_user1}%22+%22{encoded_user2}%22"
    }

def instagram_term_only_links(term):
    encoded_term = urllib.parse.quote_plus(term)
    return {
        "IG Hashtags": f"https://www.instagram.com/explore/search/keyword/?q=%23{encoded_term}",
        "IG Terms": f"https://www.google.com/search?q=site%3Ainstagram.com+{encoded_term}",
        "Dumpor Tag": "https://dumpor.io/"
    }



