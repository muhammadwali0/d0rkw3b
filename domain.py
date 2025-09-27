import urllib.parse

def domain_osint_links(domain):
    
    links = {
        "Google Search": f"https://www.google.com/search?q={domain}",
        "Bing Search": f"https://www.bing.com/search?q={domain}",
        "DuckDuckGo": f"https://duckduckgo.com/?q={domain}",
        "Whois": f"https://www.whois.com/whois/{domain}",
        "DNSChecker": f"https://dnschecker.org/all-dns-records-of-domain.php/{domain}",
        "VirusTotal": f"https://www.virustotal.com/gui/domain/{domain}/relations",
        "SecurityTrails": f"https://securitytrails.com/domain/{domain}/history",
        "Shodan": f"https://www.shodan.io/search?query={domain}",
        "Censys": f"https://search.censys.io/search?q=parsed.names%3A%20%22{domain}%22",
        "crt.sh": f"https://crt.sh/?q=%25.{domain}",
        "Wayback Machine": f"https://web.archive.org/web/*/{domain}",
        "BuiltWith": f"https://builtwith.com/{domain}",
        "MXToolbox": f"https://mxtoolbox.com/SuperTool.aspx?action=mx%3a{domain}&run=toolpage",
        "AlienVault OTX": f"https://otx.alienvault.com/indicator/domain/{domain}",
        "SSL Labs (SSL test)": f"https://www.ssllabs.com/ssltest/analyze.html?d={domain}",
        "DNSlytics": f"https://dnslytics.com/domain/{domain}",
        "SimilarWeb": f"https://www.similarweb.com/website/{domain}/",
        }

    return links