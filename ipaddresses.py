
import urllib.parse

def ip_osint_links(ip):
    ip = ip.strip()
    enc = urllib.parse.quote_plus(ip)

    return {
        "IP Address OSINT": {
            "VD ReverseIP": f"https://viewdns.info/reverseip/?host={enc}&t=1",
            "VD LocateIP": f"https://viewdns.info/iplocation/?ip={enc}",
            "VD PortScan": f"https://viewdns.info/portscan/?host={enc}",
            "VD Whois": f"https://viewdns.info/whois/?domain={enc}",
            "VD TraceRoute": f"https://viewdns.info/traceroute/?domain={enc}",
            "VD ReverseDNS": f"https://viewdns.info/reversedns/?ip={enc}",
            "IPAddress.com": f"https://www.ipaddress.com/ipv4/{enc}",
            "DNSChecker": f"https://dnschecker.org/ip-whois-lookup.php?query={enc}",
            "IPLookup": f"https://www.ip-lookup.org/location/{enc}",
            "MXTool": f"https://mxtoolbox.com/SuperTool.aspx?action=arin%3a{enc}&run=toolpage",
            "MXBlacklist": f"https://mxtoolbox.com/SuperTool.aspx?action=blacklist%3a{enc}&run=toolpage",
            "MXBlocklist": f"https://mxtoolbox.com/SuperTool.aspx?action=blocklist%3a{enc}&run=networktools",
            "Bing IP": f"https://www.bing.com/search?q=ip%3A{enc}",
            "IPLocation": f"https://www.iplocation.net/ip-lookup?query={enc}&submit=IP+Lookup",
            "Torrents": f"https://iknowwhatyoudownload.com/en/peer/?ip={enc}",
            "Wigle SSID": f"https://wigle.net/search?ssid={enc}",
            "Wigle Postal": f"https://wigle.net/search#fullSearch?postalCode={enc}",
            "Shodan": f"https://www.shodan.io/search?query={enc}",
            "Shodan Beta": f"https://beta.shodan.io/host/{enc}",
            "Shodan Raw": f"https://beta.shodan.io/host/{enc}/raw?language=en",
            "Shodan History": f"https://beta.shodan.io/host/{enc}/history",
            "ThreatCrowd": f"https://ci-www.threatcrowd.org/ip.php?ip={enc}",
            "Censys": f"https://search.censys.io/hosts/{enc}",
            "LeakIX": f"https://leakix.net/host/{enc}",
            "Dehashed": f"https://dehashed.com/search?query=%22{enc}%22"
        }
    }
