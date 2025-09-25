
import urllib.parse
import re

def _is_valid_email(email: str) -> bool:
    
    if not email or " " in email:
        return False
    pattern = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
    return re.match(pattern, email) is not None

def email_search_links(email: str) -> dict:
    e = (email or "").strip()
    if not _is_valid_email(e):
        return {"error": f"Invalid email: '{email}'"}

    enc = urllib.parse.quote_plus(e)
    enc_raw = urllib.parse.quote(e)

    return {
        "Google": f"https://www.google.com/search?q=%22{enc}%22",
        "Bing": f"https://www.bing.com/search?q=%22{enc}%22",
        "Yandex": f"https://yandex.com/search/?text=%22{enc}%22",
        "HIBP": f"https://haveibeenpwned.com/unifiedsearch/{enc}",
        "Gravatar": f"https://gravatar.com/site/check/{enc}",
        "Dehashed": f"https://dehashed.com/search?query=%22{enc}%22",
        "Spycloud": f"https://spycloud.com/",
        "HudsonRock": f"https://cavalier.hudsonrock.com/api/json/v2/preview/search-by-login/osint-tools?email={enc}",
        "PSBDMP": f"https://psbdmp.ws/api/search/{enc}",
        "IntelIX": f"https://intelx.io/?s={enc}",
        "CleanTalk": f"https://cleantalk.org/email-checker/{enc}",
        "LeakIX": f"https://leakix.net/search?scope=leak&q=%22{enc}%22",
        "HunterVerify": f"https://hunter.io/email-verifier/{enc}",
        "OCCRP": f"https://data.occrp.org/search?q={enc}",
        "Whoisology": f"https://whoisology.com/email/{enc}",
        "AnalyzeID": f"https://analyzeid.com/id/{enc}",
        "Whoxy": f"https://www.whoxy.com/search.php?email={enc}",
        "ScamSearch": f"https://scamsearch.io/search_report?searchoption=all&search={enc}",
        "SkyMem" : f"https://www.skymem.info/srch?q={enc}",
        "Flickr": f"https://www.flickr.com/search/people/?q={enc}",
        


    }



