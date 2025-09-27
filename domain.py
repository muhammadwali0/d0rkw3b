import urllib.parse

def domain_osint_links(domain):
    
    links = {
        "Google Search": f"https://www.google.com/search?q={domain}",
        "Bing Search": f"https://www.bing.com/search?q={domain}",
        "DuckDuckGo": f"https://duckduckgo.com/?q={domain}",
        "Who.is": f"https://www.whois.com/whois/{domain}",
        "Who.is DNS": f"https://who.is/dns/{domain}",
        "Who.is History": f"https://who.is/domain-history/{domain}",
        "URLScan": f"https://urlscan.io/search/#page.domain%3A{domain}",
        "DomainApp DNS": f"https://dmns.app/domains?q={domain}",
        "Reverse IP": f"https://viewdns.info/reverseip/?host={domain}&t=1",
        "Reverse Domain": f"https://viewdns.info/reversewhois/?q={domain}&t=1",
        "Port Scan": f"https://viewdns.info/portscan/?host={domain}",
        "IP History": f"https://viewdns.info/iphistory/?domain={domain}",
        "DNS Report": f"https://viewdns.info/dnsreport/?domain={domain}",
        "Traceroute": f"https://viewdns.info/traceroute/?domain={domain}",
        "Whois": f"https://viewdns.info/whois/?domain={domain}",
        "Whoxy": f"https://www.whoxy.com/{domain}",
        "Whoisology": f"https://whoisology.com/{domain}",
        "DNSChecker": f"https://dnschecker.org/all-dns-records-of-domain.php/{domain}",
        "VirusTotal": f"https://www.virustotal.com/gui/domain/{domain}/relations",
        "SecurityTrails": f"https://securitytrails.com/domain/{domain}/history",
        "Shodan": f"https://www.shodan.io/search?query={domain}",
        "Censys": f"https://search.censys.io/search?q=parsed.names%3A%20%22{domain}%22",
        "crt.sh": f"https://crt.sh/?q=%25.{domain}",
        "Whois Archive I": f"https://web.archive.org/web/20250708150623/https://who.is/whois/{domain}",
        "Whois Archive II": f"https://web.archive.org/web/20250914170937/https://whois.domaintools.com/{domain}",
        "Whois Archive III": f"https://web.archive.org/web/https://www.whoxy.com/{domain}",
        "Whois Archive IV": f"https://web.archive.org/web/https://domainbigdata.com/{domain}",
        "Whois Archive V": f"https://web.archive.org/web/https://whoisology.com/{domain}",
        "BuiltWith": f"https://builtwith.com/{domain}",
        "MXToolbox": f"https://mxtoolbox.com/SuperTool.aspx?action=mx%3a{domain}&run=toolpage",
        "AlienVault OTX": f"https://otx.alienvault.com/indicator/domain/{domain}",
        "SSL test": f"https://www.ssllabs.com/ssltest/analyze.html?d={domain}",
        "DNSlytics": f"https://dnslytics.com/domain/{domain}",
        "SimilarWeb": f"https://www.similarweb.com/website/{domain}/",
        }

    return links