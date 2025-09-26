
import urllib.parse

def video_id_links(video_id):
    enc = urllib.parse.quote_plus(video_id.strip())
    thumb_url = f"https://i.ytimg.com/vi/{enc}/maxresdefault.jpg"

    return {
        "YouTube Video ID": {
            "Age Bypass": f"https://www.nsfwyoutube.com/watch?v={enc}",
            "Full Screen": f"https://www.youtube.com/embed/{enc}",
            "Thumbnail HQ": thumb_url,
            "Thumbnail II": f"https://img.youtube.com/vi/{enc}/1.jpg",
            "Thumbnail III": f"https://img.youtube.com/vi/{enc}/2.jpg",
            "Thumbnail IV": f"https://img.youtube.com/vi/{enc}/3.jpg",
            "Google Reverse": f"https://www.google.com/search?q={enc}&tbm=isch&udm=2",
            "Bing Reverse": f"https://www.bing.com/images/search?view=detailv2&iss=sbi&q=imgurl:{thumb_url}",
            "Yandex Reverse": f"https://yandex.com/images/search?rpt=imageview&url={urllib.parse.quote_plus(thumb_url)}",
            "TinEye Reverse": f"https://www.tineye.com/search/?url={urllib.parse.quote_plus(thumb_url)}",
            "Restrictions": f"https://polsy.org.uk/stuff/ytrestrict.cgi?ytid={enc}",
            "Metadata": f"https://www.googleapis.com/youtube/v3/videos?id={enc}&part=snippet,statistics,recordingDetails&key=AIzaSyDNALbuV1FZSRy6JpafwUaV_taSVV12wZw",
            "Download": f"https://deturl.com/watch?v={enc}",
            "Archives": f"https://web.archive.org/web/20250925215933/https://www.youtube.com/watch?v={enc}"
        }
    }

def video_search_links(term):
    enc = urllib.parse.quote_plus(term.strip())

    return {
        "Video Search": {
            "Google Videos": f"https://www.google.com/search?q={enc}&udm=7",
            "Bing Videos": f"https://www.bing.com/videos/search?q={enc}",
            "Yandex Videos": f"https://yandex.ru/video/search?text={enc}&rpt=imageview",
            "YouTube Videos": f"https://www.youtube.com/results?search_query={enc}",
            "X Media": f"https://x.com/search?q={enc}&f=media",
            "Facebook Videos": f"https://www.facebook.com/search/videos/?q={enc}",
            "Reddit Videos": f"https://www.reddit.com/search?q=site:v.redd.it%20AND%20{enc}",
            "TikTok Videos": f"https://www.tiktok.com/tag/{enc}",
            "Archives I": f"https://archive.org/details/movies?tab=collection&query={enc}",
            "Archives II": f"https://archive.org/details/opensource_movies?tab=collection&query={enc}",
            "TV Archives": f"https://archive.org/details/tv?q={enc}"
        }
    }

def youtube_username_links(username):
    enc = urllib.parse.quote_plus(username.strip())
    return {
        "YouTube Username": {
            "Profile": f"https://www.youtube.com/user/{enc}",
            "Account Feed": f"https://www.youtube.com/feeds/videos.xml?user={enc}"
        }
    }
