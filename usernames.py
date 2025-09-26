import urllib.parse

def username_osint_links(username):
    enc = urllib.parse.quote_plus(username.strip())

    return {
        "Username OSINT": {
            "Google": f"https://www.google.com/search?q=%22{enc}%22",
            "Bing": f"https://www.bing.com/search?q=%22{enc}%22",
            "Yandex": f"https://yandex.com/search/?text=%22{enc}%22&lr=10615",
            "ID Crawl": f"https://www.idcrawl.com/u/{enc}",
            "InstantUsername": f"https://instantusername.com/?q={enc}",
            "NameChecker": f"https://www.namechecker.org/#{enc}",
            "NameChk": f"https://namechk.com/namechk-plugin-search-results/?n={enc}",
            "NameVine": f"https://namevine.com/#/{enc}",
            "CandidateChecker": f"https://candidatechecker.io/{enc}",
            "SocialSearcher": f"https://www.social-searcher.com/google-social-search/?q={enc}",
            "Checkistan": f"https://usernamechecker.checkistan.com/#{enc}",
            "UserSearch": f"https://usersearch.org/results_normal.php?URL_username={enc}",
            "Dehashed": f"https://dehashed.com/search?query=%22{enc}%22",
            "PSBDMP": f"https://psbdmp.ws/api/search/{enc}",
            "Gravatar": f"https://gravatar.com/{enc}",
            "LinkTree": f"https://linktr.ee/{enc}",
            "X": f"https://x.com/{enc}",
            "Facebook": f"https://www.facebook.com/{enc}/",
            "Instagram": f"https://www.instagram.com/{enc}/",
            "TikTok": f"https://www.tiktok.com/@{enc}",
            "Tinder": f"https://tinder.com/@{enc}",
            "Tumblr": f"https://{enc}.tumblr.com/",
            "Snapchat": f"https://www.snapchat.com/@{enc}",
            "Medium": f"https://medium.com/@{enc}",
            "YouTube": f"https://www.youtube.com/{enc}",
            "Reddit": f"https://www.reddit.com/user/{enc}/",
            "Ghunt": f"https://gmail-osint.activetk.jp/{enc}",
            "Dehashed Emails": f"https://dehashed.com/search?query=%22{enc}%40gmail.com%22",
            "Email Search": f"https://www.google.com/search?q=%22{enc}%40gmail.com%22OR%22{enc}%40yahoo.com%22OR%22{enc}%40hotmail.com%22OR%22{enc}%40protonmail.com%22OR%22{enc}%40live.com%22OR%22{enc}%40icloud.com%22OR%22{enc}%40yandex.com%22OR%22{enc}%40gmx.com%22OR%22{enc}%40mail.com%22OR%22{enc}%40mac.com%22OR%22{enc}%40me.com%22"
        }
    }
