
import urllib.parse
from datetime import datetime
import requests
import re


# LinkedIn Profile Links
def li_profile_links(username):
    encoded = urllib.parse.quote_plus(username.strip())
    base = f"https://www.linkedin.com/in/{encoded}"
    return {
        "Profile": f"{base}",
        "About": f"{base}/details/about/",
        "Experience": f"{base}/details/experience/",
        "Education": f"{base}/details/education/",
        "Skills": f"{base}/details/skills/",
        "Recommendations": f"{base}/details/recommendations/",
        "Accomplishments": f"{base}/details/accomplishments/",
        "Posts": f"{base}/recent-activity/all/",
        "Articles": f"{base}/recent-activity/posts/",
        "Documents": f"{base}/recent-activity/documents/",
        "Images": f"{base}/recent-activity/images/",
        "Videos": f"{base}/recent-activity/videos/",
        "Comments": f"{base}/recent-activity/comments/",
        "Profile": f"https://www.linkedin.com/in/{username}",
        "Google Photos": f"https://www.google.com/search?q=site:linkedin.com+{encoded}&source=lnms&udm=2",
        "Bing Photos": f"https://www.bing.com/images/search?q=site%3Alinkedin.com+{encoded}&scenario=ImageBasicHover"
    }

# LinkedIn Company Links
def li_company_links(company_name):
    encoded = urllib.parse.quote_plus(company_name.strip())
    base = f"https://www.linkedin.com/company/{encoded}"
    return {
        "Company Page": f"{base}",
        "About": f"{base}/about/",
        "Jobs": f"{base}/jobs/",
        "People": f"{base}/people/",
        "Events": f"{base}/events/",
        "Posts": f"{base}/posts/",
        "Videos": f"{base}/videos/",
        "Life": f"{base}/life/"
    }

# LinkedIn Generic Search Links
def li_search_links(term):
    encoded = urllib.parse.quote_plus(term.strip())
    return {
        "All": f"https://www.linkedin.com/search/results/all/?keywords={encoded}",
        "People": f"https://www.linkedin.com/search/results/people/?keywords={encoded}",
        "Companies": f"https://www.linkedin.com/search/results/companies/?keywords={encoded}",
        "Jobs": f"https://www.linkedin.com/search/results/jobs/?keywords={encoded}",
        "Groups": f"https://www.linkedin.com/search/results/groups/?keywords={encoded}",
        "Posts": f"https://www.linkedin.com/search/results/content/?keywords={encoded}",
        "Events": f"https://www.linkedin.com/search/results/events/?keywords={encoded}",
        "Courses": f"https://www.linkedin.com/learning/search?keywords={encoded}"
    }


def linkedin_post_upload_date(post_url):
    encoded_url = urllib.parse.quote_plus(post_url.strip())
    return {
        "Timestamp Extractor": f"https://ollie-boyd.github.io/Linkedin-post-timestamp-extractor/?url={encoded_url}"
    }
