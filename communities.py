
import urllib.parse

def community_search_links(term):
    encoded = urllib.parse.quote_plus(term)
    return {
        "Reddit": {
            "Keyword Search": f"https://www.reddit.com/search?q={encoded}",
            "Keyword Search (Old)": f"https://old.reddit.com/search?q={encoded}",
            "Subreddit Search": f"https://www.reddit.com/subreddits/search?q={encoded}",
            "Domain": f"https://reddit.com/search?q=site:{encoded}",
            "Domain Mention": f"https://reddit.com/search?q=url:{encoded}",
            "Image Search": "https://www.google.com/imghp?sbi=1"
        },
        "Hacker News": {
            "Keyword Search": f"https://hn.algolia.com/?query={encoded}&sort=byDate&prefix&page=0&dateRange=all&type=all",
            "Google Search": f"https://www.google.com/search?q=site:news.ycombinator.com+{encoded}"
        },
        "4chan": {
            "Keyword Search": f"https://4chansearch.com/?q={encoded}&s=4",
            "Archive Search I": f"https://4chansearch.com/?q={encoded}&s=7",
            "Archive Search II": f"https://archive.4plebs.org/_/search/text/{encoded}/order/asc/",
            "Google": f"https://www.google.com/search?q=site:4chan.org%20{encoded}"
        },
        "TikTok": {
            "Tags": f"https://www.tiktok.com/tag/{encoded}",
            "Term Search": f"https://www.tiktok.com/search?q={encoded}",
            "Video Search": f"https://www.tiktok.com/search/video?q={encoded}",
            "Google Search": f"https://www.google.com/search?q=site:tiktok.com+{encoded}"
        },
        "Meetup": {
            "Event Search": f"https://www.google.com/search?q=site:meetup.com+inurl:events+{encoded}",
            "Post Search": f"https://www.google.com/search?q=site:meetup.com+inurl:discussions+{encoded}",
            "Google Search": f"https://www.google.com/search?q=site:meetup.com+{encoded}"
        },
        "Ebay": {
            "Text Search": f"https://www.ebay.com/sch/i.html?&LH_TitleDesc=1&_nkw={encoded}",
            "Sold Search": f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={encoded}&LH_Sold=1&LH_Complete=1",
            "Completed Search": f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={encoded}&LH_Complete=1"
        },
        "Pinterest": {
            "Pins Search": f"https://www.pinterest.com/search/pins/?q={encoded}&rs=typo_auto_original&auto_correction_disabled=true",
            "Boards Search": f"https://www.pinterest.com/search/boards/?q={encoded}&rs=typo_auto_original&auto_correction_disabled=true",
            "Google Search": f"https://www.google.com/search?q=site:pinterest.com+{encoded}"
        },
        "Discord": {
            "Disboard": f"https://disboard.org/search?keyword={encoded}",
            "Discord.me": f"https://discord.me/servers?search={encoded}",
            "Servers": f"https://discordservers.com/search/{encoded}",
            "Discordbee": f"https://discordbee.com/servers?q={encoded}",
            "Google Search": f"https://www.google.com/search?q=site:discord.com+{encoded}"
        },
        "Parler": {
            "Hashtag Search": f"https://app.parler.com/hashtag/{encoded}"
        },
        "Gab": {
            "Groups Search": f"https://gab.com/search/hashtags?q={encoded}",
            "Hashtag Search": f"https://gab.com/search/hashtags?q={encoded}"
        },
        "Mastodon": {
            "Hashtag Search": f"https://mastodon.social/api/v2/search?q={encoded}&limit=40&type=hashtags"
        },
        "Telegram": {
            "Group Search": f"https://www.telegram-group.com/en?s={encoded}",
            "Channel Search I": f"https://telegramchannels.me/search?type=all&search={encoded}",
            "Channel Search II": f"https://telemetr.io/en/catalog/global?term={encoded}"
        }
    }

def community_user_links(username):
    encoded = urllib.parse.quote_plus(username)
    return {
        "Reddit": {
            "User Profile": f"https://reddit.com/user/{username}",
            "User Submissions": f"https://reddit.com/user/{username}/submitted",
            "User Comments": f"https://reddit.com/user/{username}/comments/",
            "User Archive": f"https://web.archive.org/web/20250000000000*/https://www.reddit.com/user/{username}"
        },
        "Hacker News": {
            "User Search": f"https://news.ycombinator.com/user?id={username}",
            "User Posts": f"https://news.ycombinator.com/submitted?id={username}",
            "User Comments": f"https://news.ycombinator.com/threads?id={username}",
            "Favorite": f"https://news.ycombinator.com/favorites?id={username}"
        },
        "TikTok": {
            "Profile": f"https://www.tiktok.com/@{username}",
            "Profile Search": f"https://www.tiktok.com/search/user?q={username}",
            "Analytics I": f"https://tokcount.com/?user={username}",
            "Analytics II": f"https://exolyt.com/user/{username}",
            "Analytics III": f"https://tokcounter.com/?user={username}"
        },
        "Meetup": {
            "Member Search": f"https://www.google.com/search?q=site:meetup.com+{encoded}"
        },
        "Ebay": {
            "User Account": f"https://www.ebay.com/usr/{username}",
            "User Feedback": f"https://feedback.ebay.com/fdbk/feedback_profile/{username}",
            "User Items": f"https://www.ebay.com/sch/i.html?_ssn={username}",
            "User Search": f"https://www.google.com/search?q=site%3Ahttps%3A%2F%2Fwww.ebay.com%2Fusr+%22{encoded}%22"
        },
        "Pinterest": {
            "User Search": f"https://www.pinterest.com/{username}/",
            "User Created": f"https://www.pinterest.com/{username}/_created/",
            "User Saved": f"https://www.pinterest.com/{username}/_saved/"
        },
        "Discord": {
            "Invite Check": f"https://discord.com/invite/{username}"
        },
        "Parler": {
            "User Profile": f"https://app.parler.com/{username}",
            "User Search": f"https://app.parler.com/username/{username}"
        },
        "Gab": {
            "User Profile": f"https://gab.com/{username}"
        },
        "Gettr": {
            "User Profile": f"https://gettr.com/user/{username}",
            "Comments": f"https://gettr.com/user/{username}/comments",
            "Media": f"https://gettr.com/user/{username}/medias",
            "Likes": f"https://gettr.com/user/{username}/likes"
        },
        "Mastodon": {
            "Username Search": f"https://mastodon.social/api/v2/search?q={username}&limit=40&type=accounts"
        },
        "Telegram": {
            "Profile/Channel": f"https://t.me/{username}",
            "User Videos": f"https://telesco.pe/{username}"
        }
    }
