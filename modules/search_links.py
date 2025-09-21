
import urllib.parse

def generate_links(search_terms):
    result = '+'.join(search_terms.split())
    encoded_search = urllib.parse.quote_plus(search_terms)
    ftp_dork = urllib.parse.quote_plus(f'inurl:ftp -inurl:(http|https) {search_terms}')
    index_dork = urllib.parse.quote_plus(f'intitle:index.of {search_terms}')

    engines = {
        "Google":         f"https://www.google.com/search?q={result}",
        "Google Date":    f"https://www.google.com/search?q={result}&tbs=cdr:1,cd_min:1/1/0,sbd:1",
        "Google News":    f"https://www.google.com/search?tbm=nws&q={result}",
        "Google FTP":     f"https://www.google.com/search?q={ftp_dork}",
        "Google Index":   f"https://www.google.com/search?q={index_dork}",
        "Google Scholar": f"https://scholar.google.com/scholar?q={result}",
        "Google Patents": f"https://patents.google.com/?q={result}",
        "Bing":           f"https://www.bing.com/search?q={result}",
        "Bing News":      f"https://www.bing.com/news/search?q={result}",
        "Yahoo":          f"https://search.yahoo.com/search?p={result}",
        "Yandex":         f"https://yandex.com/search/?text={result}",
        "Baidu":          f"https://www.baidu.com/s?wd={result}",
        "Searx":          f"https://searx.be/search?q={result}",
        "DuckDuckGo":     f"https://duckduckgo.com/?q={result}",
        "Startpage":      f"https://www.startpage.com/do/search?query={result}",
        "Qwant":          f"https://www.qwant.com/?q={result}",
        "Brave":          f"https://search.brave.com/search?q={result}",
        "Wayback":        f"https://web.archive.org/web/*/{search_terms}",
        "Ahmia":          f"https://ahmia.fi/search/?q={result}",
        "Tor.link":       f"https://tor.link/?q={result}"
    }

    tor_engines = {
        "Torch": f"http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion/cgi-bin/omega/omega?P={result}&DEFAULTOP=and&DB=default&FMT=query&xDB=default&xFILTERS=.%7E%7E&tkn=bf850c9344b659c1f203fbb53a9ec04a%0D%0A",
        "Deep Search": f"http://search7tdrcvri22rieiwgi5g46qnwsesvnubqav2xakhezv4hjzkkad.onion/result.php?search={result}&url=search7tdrcvri22rieiwgi5g46qnwsesvnubqav2xakhezv4hjzkkad.onion",
        "Ahmia": f"http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search/?q={result}",
        "Tordex": f"http://tordexpmg4xy32rfp4ovnz7zq5ujoejwq2u26uxxtkscgo5u3losmeid.onion/search?query={result}",
        "VormWeb": f"http://volkancfgpi4c7ghph6id2t7vcntenuly66qjt6oedwtjmyj4tkk5oqd.onion/en/search?q={result}",
        "OnionLand": f"http://3bbad7fauom4d6sgppalyqddsqbf5u5p56b5k5uk2zxsy3d6ey2jobad.onion/search?q={result}",
        "Torland": f"http://torlbmqwtudkorme6prgfpmsnile7ug2zm4u3ejpcncxuhpu4k2j4kyd.onion/index.php?a=search&q={result}",
        "Tor66": f"http://www.tor66sewebgixwhcqfnp5inzp5x5uohhdy3kvtnyfxc2e5mxiuh34iid.onion/search?q={result}",
        "GDark": f"http://zb2jtkhnbvhkya3d46twv3g7lkobi4s62tjffqmafjibixk6pmq75did.onion/gdark/search.php?query={result}&search=1",
        "Hidden Reviews": f"http://u5lyidiw4lpkonoctpqzxgyk6xop7w7w3oho4dzzsi272rwnjhyx7ayd.onion/?s={result}",
        "Submarine": f"http://no6m4wzdexe3auiupv2zwif7rm6qwxcyhslkcnzisxgeiw6pvjsgafad.onion/search.php?term={result}",
        "OnionCentre": f"http://5qqrlc7hw3tsgokkqifb33p3mrlpnleka2bjg7n46vih2synghb6ycid.onion/index.php?a=search&q={result}",
        "FreshOnion": f"http://freshonifyfe4rmuh6qwpsexfhdrww7wnt5qmkoertwxmcuvm4woo4ad.onion/?query={result}"
    }

    return engines, tor_engines
