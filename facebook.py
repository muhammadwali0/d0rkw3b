
import urllib.parse
from datetime import datetime

def fb_username_links(username):
    base = f"https://www.facebook.com/{username}"
    return {
        "Timeline": f"{base}",
        "About": f"{base}/about",
        "Employement": f"{base}/about?section=work",
        "Education": f"{base}/about?section=education",
        "Locations": f"{base}/about?section=living",
        "Contact Info": f"{base}/about?section=contact-info",
        "Basic Info": f"{base}/about?section=basic-info",
        "Relationships": f"{base}/about?section=relationship",
        "Family": f"{base}/about?section=family",
        "Biography": f"{base}/about?section=bio",
        "Life Events": f"{base}/about?section=year-overviews",
        "Friends": f"{base}/friends",
        "Following": f"{base}/following",
        "Photos": f"{base}/photos",
        "Photos Albums": f"{base}/photos_albums",
        "Videos": f"{base}/videos",
        "Reels": f"{base}/reels/",
        "Check-ins": f"{base}/places_visited",
        "Visits": f"{base}/map",
        "Recent Check-ins": f"{base}/places_recent",
        "Sports": f"{base}/sports",
        "Music": f"{base}/music",
        "Movies": f"{base}/movies",
        "TV": f"{base}/tv",
        "Books": f"{base}/books",
        "Games": f"{base}/games",
        "Likes": f"{base}/likes",
        "Events": f"{base}/events",
        "Facts": f"{base}/did_you_know",
        "Reviews": f"{base}/reviews",
        "Reviews Given": f"{base}/reviews_given",
        "Reviews Written": f"{base}/reviews_written",
        "Notes": f"{base}/notes"
    }

def fb_number_links(number):
    return {"Profile": f"https://www.facebook.com/{number}"}

def fb_search_term_links(term):
    encoded = urllib.parse.quote_plus(term)
    return {
        "All": f"https://www.facebook.com/search/top/?q={encoded}",
        "Posts": f"https://www.facebook.com/search/posts/?q={encoded}",
        "People": f"https://www.facebook.com/search/people/?q={encoded}",
        "Photos": f"https://www.facebook.com/search/photos/?q={encoded}",
        "Videos": f"https://www.facebook.com/search/videos/?q={encoded}",
        "Marketplace": f"https://www.facebook.com/search/marketplace/?q={encoded}",
        "Pages": f"https://www.facebook.com/search/pages/?q={encoded}",
        "Places": f"https://www.facebook.com/search/places/?q={encoded}",
        "Groups": f"https://www.facebook.com/search/groups/?q={encoded}",
        "Events": f"https://www.facebook.com/search/events/?q={encoded}",
        "Links": f"https://www.facebook.com/search/links/?q={encoded}",
        "Watch": f"https://www.facebook.com/watch/search/?q={encoded}"
    }

def fb_user_id_links(user_id):
    return {"Profile": f"https://www.facebook.com/{user_id}"}

def fb_location_links(location_id):
    return {
        "Photos by Location": f"https://www.facebook.com/{location_id}/photos",
        "Videos by Location": f"https://www.facebook.com/{location_id}/videos"
    }
