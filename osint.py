#!/usr/bin/env python3
"""
NetProbe - OSINT Module
Author: Ankush (cybersecurity)
GeoIP Lookup + Shodan Integration + Reverse DNS + Whois
"""
import json, os, socket

class C:
    RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"; CYAN="\033[96m"
    MAGENTA="\033[95m"; WHITE="\033[97m"; BOLD="\033[1m"; DIM="\033[2m"; RESET="\033[0m"

SHODAN_KEY_FILE = ".shodan_key"
GEOIP_API = "http://ip-api.com/json/"

class OSINTModule:
    def __init__(self):
        self.shodan_key = self._load_shodan_key()

    def _load_shodan_key(self):
        if os.path.exists(SHODAN_KEY_FILE):
            with open(SHODAN_KEY_FILE) as f:
                return f.read().strip()
        return None

    def lookup(self, ip):
        print(f"\n  {C.CYAN}{C.BOLD}[*] OSINT Lookup: {ip}{C.RESET}")
        print(f"  {C.DIM}NetProbe by Ankush (cybersecurity){C.RESET}\n")

        # Skip private IPs for public OSINT
        if self._is_private(ip):
            print(f"  {C.YELLOW}[!] {ip} is a private/local IP.{C.RESET}")
            print(f"  {C.YELLOW}    GeoIP & Shodan only work for public IPs.{C.RESET}")
            self._local_info(ip)
            return

        self._geoip_lookup(ip)
        self._reverse_dns(ip)
        if self.shodan_key:
            self._shodan_lookup(ip)
        else:
            print(f"\n  {C.YELLOW}[!] Shodan API key not configured.{C.RESET}")
            print(f"  {C.DIM}    Add key: echo 'YOUR_KEY' > .shodan_key{C.RESET}")

    def _is_private(self, ip):
        import ipaddress
        try:
            return ipaddress.ip_address(ip).is_private
        except:
            return False

    def _local_info(self, ip):
        """Local IP info"""
        print(f"\n  {C.CYAN}[*] Local Device Info:{C.RESET}")
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            print(f"  {C.GREEN}  Hostname : {hostname}{C.RESET}")
        except:
            print(f"  {C.DIM}  Hostname : Not resolvable{C.RESET}")
        print(f"  {C.DIM}  Type     : Private/Local Network IP{C.RESET}")

    def _geoip_lookup(self, ip):
        """GeoIP lookup via ip-api.com"""
        print(f"  {C.CYAN}[*] GeoIP Lookup...{C.RESET}")
        try:
            import urllib.request
            url = f"{GEOIP_API}{ip}?fields=status,country,regionName,city,zip,lat,lon,isp,org,as,query"
            with urllib.request.urlopen(url, timeout=5) as r:
                data = json.loads(r.read())

            if data.get("status") == "success":
                print(f"\n  {C.BOLD}{C.WHITE}  ╔══ GeoIP Results ══════════════════════════╗{C.RESET}")
                fields = [
                    ("IP",      data.get("query","")),
                    ("Country", data.get("country","")),
                    ("Region",  data.get("regionName","")),
                    ("City",    data.get("city","")),
                    ("ZIP",     data.get("zip","")),
                    ("Lat/Lon", f"{data.get('lat','')} / {data.get('lon','')}"),
                    ("ISP",     data.get("isp","")),
                    ("Org",     data.get("org","")),
                    ("AS",      data.get("as","")),
                ]
                for k, v in fields:
                    if v:
                        print(f"  {C.WHITE}  ║  {C.CYAN}{k:<10}{C.RESET}: {C.GREEN}{v}{C.RESET}")
                print(f"  {C.WHITE}  ╚══════════════════════════════════════════╝{C.RESET}")
            else:
                print(f"  {C.RED}[-] GeoIP lookup failed.{C.RESET}")
        except Exception as e:
            print(f"  {C.RED}[-] GeoIP error: {e}{C.RESET}")
            print(f"  {C.YELLOW}[!] Check internet connection.{C.RESET}")

    def _reverse_dns(self, ip):
        """Reverse DNS lookup"""
        print(f"\n  {C.CYAN}[*] Reverse DNS Lookup...{C.RESET}")
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            print(f"  {C.GREEN}  Hostname: {hostname}{C.RESET}")
        except socket.herror:
            print(f"  {C.DIM}  No PTR record found.{C.RESET}")
        except Exception as e:
            print(f"  {C.RED}[-] DNS error: {e}{C.RESET}")

    def _shodan_lookup(self, ip):
        """Shodan IP lookup"""
        print(f"\n  {C.CYAN}[*] Shodan Intelligence Lookup...{C.RESET}")
        try:
            import shodan
            api = shodan.Shodan(self.shodan_key)
            host = api.host(ip)

            print(f"\n  {C.BOLD}{C.MAGENTA}  ╔══ Shodan Results ═════════════════════════╗{C.RESET}")
            print(f"  {C.MAGENTA}  ║  OS       : {host.get('os','Unknown'):<32}║{C.RESET}")
            print(f"  {C.MAGENTA}  ║  Org      : {str(host.get('org','?'))[:32]:<32}║{C.RESET}")
            print(f"  {C.MAGENTA}  ║  Last Seen: {host.get('last_update','?')[:32]:<32}║{C.RESET}")
            print(f"  {C.MAGENTA}  ║  Open Ports: {str([p['port'] for p in host.get('data',[])])[:30]:<30}║{C.RESET}")

            vulns = host.get("vulns", [])
            if vulns:
                print(f"\n  {C.RED}  ⚠  CVEs / Vulnerabilities Found:{C.RESET}")
                for cve in list(vulns)[:5]:
                    print(f"  {C.RED}     └ {cve}{C.RESET}")

            print(f"  {C.MAGENTA}  ╚══════════════════════════════════════════╝{C.RESET}")
        except ImportError:
            print(f"  {C.YELLOW}[!] Install: pip install shodan{C.RESET}")
        except Exception as e:
            print(f"  {C.RED}[-] Shodan error: {e}{C.RESET}")

    def configure_shodan(self):
        """Interactive Shodan key setup"""
        print(f"\n  {C.CYAN}[?] Enter your Shodan API key:{C.RESET}")
        print(f"  {C.DIM}    Get free key at: https://shodan.io{C.RESET}")
        key = input(f"  Key: ").strip()
        if key:
            with open(SHODAN_KEY_FILE, "w") as f:
                f.write(key)
            self.shodan_key = key
            print(f"  {C.GREEN}[+] Shodan key saved!{C.RESET}")
