
import urllib.parse

def reverse_image_search(image_url):
    encoded = urllib.parse.quote_plus(image_url.strip())

    return {
        "Reverse Image Search": {
            "Google Images": f"https://www.google.com/searchbyimage?image_url={encoded}",
            "Google Lens": f"https://lens.google.com/uploadbyurl?url={encoded}",
            "Bing Visual Search": f"https://www.bing.com/images/search?view=detailv2&iss=sbi&q=imgurl:{encoded}",
            "TinEye": f"https://tineye.com/search?url={encoded}",
            "Yandex": f"https://yandex.com/images/search?rpt=imageview&url={encoded}",
            "FaceCheck": f"https://facecheck.id/search-by-url?url={encoded}",
        }
    }

def image_keyword_search(term):
    encoded = urllib.parse.quote_plus(term.strip())

    return {
        "Image Search": {
            "Google Images": f"https://www.google.com/search?q={encoded}&sca_esv=d2ab6361f8823ac8&sxsrf=AE3TifMMxaz7DcLQ63hXOiXFxQ9hna1ihg:1758815445335&source=hp&ei=1WTVaJG1ErKJ7NYPlrf8UA&iflsig=AOw8s4IAAAAAaNVy5X4yk2OpJeYnvduxT6DcEjvEkoQQ&ved=0ahUKEwjR896OovSPAxWyBNsEHZYbHwoQ4dUDCBc&uact=5&oq=apple&gs_lp=Egtnd3Mtd2l6LWltZyIFYXBwbGUyChAjGCcYyQIY6gIyChAjGCcYyQIY6gIyChAjGCcYyQIY6gIyChAjGCcYyQIY6gIyChAjGCcYyQIY6gIyChAjGCcYyQIY6gIyChAjGCcYyQIY6gIyChAjGCcYyQIY6gIyChAjGCcYyQIY6gIyChAjGCcYyQIY6gJI8g5QogZY1g1wAXgAkAEAmAEAoAEAqgEAuAEDyAEA-AEBmAIBoAIIqAIKmAMIkgcBMaAHALIHALgHAMIHAzItMcgHBg&sclient=gws-wiz-img&udm=2",
            "Bing Images": f"https://www.bing.com/images/search?q={encoded}",
            "Yandex Images": f"https://yandex.com/images/search?text={encoded}",
            "X": f"https://x.com/search?q={encoded}&src=typed_query&f=media",
            "Facebook": f"https://www.facebook.com/search/photos/?q={encoded}",
            "Instagram": f"https://www.google.com/search?q=site%3Ainstagram.com+{encoded}&tbm=isch",
            "LinkedIn": f"https://www.google.com/search?q=site%3Alinkedin.com+{encoded}&tbm=isch",
            "Flickr": f"https://www.flickr.com/search/?text={encoded}",
            "Pinterest": f"https://www.pinterest.com/search/pins/?q={encoded}&rs=typed",
            "DuckDuckGo Images": f"https://duckduckgo.com/?q={encoded}&iax=images&ia=images"
        }
    }