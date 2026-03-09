#!/usr/bin/env python3
"""
NetProbe v2.0 - WiFi Network Scanner & Cybersecurity Analyzer
Author  : Ankush (cybersecurity)
GitHub  : https://github.com/Ankush-cyber/netprobe
Platform: Kali Linux | Termux (Android)
License : MIT
"""
import sys, os, time, argparse
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class C:
    RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"; CYAN="\033[96m"
    BLUE="\033[94m"; MAGENTA="\033[95m"; WHITE="\033[97m"
    BOLD="\033[1m"; DIM="\033[2m"; RESET="\033[0m"

def load_module(name):
    try:
        if name == "scanner":
            from modules.scanner import NetworkScanner; return NetworkScanner()
        elif name == "fingerprint":
            from modules.fingerprint import DeviceFingerprinter; return DeviceFingerprinter()
        elif name == "port_scanner":
            from modules.port_scanner import PortScanner; return PortScanner()
        elif name == "arp_detector":
            from modules.arp_detector import ARPSpoofDetector; return ARPSpoofDetector()
        elif name == "osint":
            from modules.osint import OSINTModule; return OSINTModule()
        elif name == "alerts":
            from modules.alerts import AlertManager; return AlertManager()
        elif name == "reporter":
            from modules.reporter import ReportGenerator; return ReportGenerator()
        elif name == "whitelist":
            from modules.whitelist import WhitelistManager; return WhitelistManager()
    except ImportError as e:
        print(f"{C.RED}[-] Module error: {e}{C.RESET}"); return None

def print_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"""{C.CYAN}{C.BOLD}
 ╔══════════════════════════════════════════════════════════════════════╗
 ║  ███╗   ██╗███████╗████████╗██████╗ ██████╗  ██████╗ ██████╗        ║
 ║  ████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗       ║
 ║  ██╔██╗ ██║█████╗     ██║   ██████╔╝██████╔╝██║   ██║██████╔╝       ║
 ║  ██║╚██╗██║██╔══╝     ██║   ██╔═══╝ ██╔══██╗██║   ██║██╔══██╗       ║
 ║  ██║ ╚████║███████╗   ██║   ██║     ██║  ██║╚██████╔╝██████╔╝       ║
 ║  ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═════╝        ║
 ╠══════════════════════════════════════════════════════════════════════╣
 ║  {C.GREEN}Author  : Ankush  |  cybersecurity Researcher & Tool Developer{C.CYAN}       ║
 ║  {C.YELLOW}Platform: Kali Linux | Termux Android | Ubuntu/Debian{C.CYAN}               ║
 ║  {C.MAGENTA}Version : 2.0.0   |  Complete WiFi Recon & Security Toolkit{C.CYAN}         ║
 ║  {C.RED}⚠  For Authorized Pentesting & Education Only — Stay Ethical ⚠{C.CYAN}    ║
 ╚══════════════════════════════════════════════════════════════════════╝{C.RESET}""")

def print_menu():
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    print(f"""
  {C.DIM}Time: {now}{C.RESET}

  {C.CYAN}{C.BOLD}┌──────────────────────────────────────────────┐
  │           NETPROBE v2.0 — MAIN MENU          │
  ├──────────────────────────────────────────────┤{C.RESET}

  {C.GREEN}[1]  🔍  WiFi Network Scan       (ARP Discovery)
  [2]  📱  Device Classifier        (Camera/PC/Phone)
  [3]  🔌  Port Scanner             (Per Device)
  [4]  🛡  ARP Spoof Detector       (MITM Detection)
  [5]  🌍  OSINT Lookup             (GeoIP + Shodan)
  [6]  📊  Report Generator         (HTML / PDF / JSON)
  [7]  🗺  Network Topology Map     (Visual Map)
  [8]  🌐  Live Web Dashboard       (Browser UI)
  [9]  🔔  Telegram Alert Setup
  [10] ✅  Whitelist / Blacklist Manager
  [11] 📡  Continuous Monitor Mode
  [12] 📜  Scan History Viewer
  [13] ℹ   About NetProbe
  [0]  🚪  Exit{C.RESET}

  {C.CYAN}{C.BOLD}└──────────────────────────────────────────────┘{C.RESET}""")

def show_about():
    print(f"""
{C.CYAN}{C.BOLD}
 ╔══════════════════════════════════════════════════════════╗
 ║                   ABOUT NETPROBE v2.0                   ║
 ╠══════════════════════════════════════════════════════════╣
 ║                                                         ║
 ║  Tool    : NetProbe - WiFi Network Security Analyzer    ║
 ║  Author  : Ankush                                       ║
 ║  Role    : cybersecurity Researcher & Tool Developer    ║
 ║  GitHub  : github.com/Ankush-cyber/netprobe             ║
 ║  License : MIT (Free & Open Source)                    ║
 ║                                                         ║
 ╠══════════════════════════════════════════════════════════╣
 ║  ALL FEATURES:                                          ║
 ║   ✔  ARP-Based WiFi Network Scanner                    ║
 ║   ✔  Device Fingerprinting & Classification            ║
 ║      └ Camera | PC | Phone | Router | IoT              ║
 ║   ✔  Port Scanner (TCP/UDP)                            ║
 ║   ✔  ARP Spoofing / MITM Detection                     ║
 ║   ✔  GeoIP + Shodan OSINT Integration                  ║
 ║   ✔  Telegram Bot Alerts (New Device Alert)            ║
 ║   ✔  HTML / PDF / JSON Report Generator                ║
 ║   ✔  Network Topology Visual Map                       ║
 ║   ✔  Live Web Dashboard                                ║
 ║   ✔  Whitelist / Blacklist System                      ║
 ║   ✔  Continuous Monitor Mode                           ║
 ║   ✔  Scan History & Comparison                        ║
 ║                                                         ║
 ╠══════════════════════════════════════════════════════════╣
 ║  SUPPORTED PLATFORMS:                                   ║
 ║   ✔  Kali Linux (Full features)                        ║
 ║   ✔  Termux Android (Root = Full | No-root = Limited)  ║
 ║   ✔  Ubuntu / Debian                                   ║
 ║                                                         ║
 ║   ⚠  Use only on YOUR OWN network. Be Ethical!  ⚠     ║
 ╚══════════════════════════════════════════════════════════╝
{C.RESET}""")

def main():
    parser = argparse.ArgumentParser(description="NetProbe v2.0 by Ankush (cybersecurity)")
    parser.add_argument("-t","--target",  help="IP/Range: 192.168.1.0/24")
    parser.add_argument("-m","--mode",    help="scan|ports|arp|osint|report|monitor", default="menu")
    parser.add_argument("-o","--output",  help="Output file: report.html / results.json")
    parser.add_argument("-v","--verbose", action="store_true")
    parser.add_argument("--monitor",      action="store_true")
    parser.add_argument("--interval",     type=int, default=60)
    parser.add_argument("--version",      action="version", version="NetProbe v2.0.0 by Ankush")
    args = parser.parse_args()

    print_banner()
    last_results = []

    # Direct CLI mode
    if args.mode != "menu" and args.target:
        scanner = load_module("scanner")
        if args.mode == "scan":
            last_results = scanner.scan(args.target)
            scanner.display_results(last_results)
        elif args.mode == "ports":
            ps = load_module("port_scanner"); ps.scan_ip(args.target)
        elif args.mode == "arp":
            arp = load_module("arp_detector"); arp.detect(args.target)
        elif args.mode == "osint":
            osint = load_module("osint"); osint.lookup(args.target)
        elif args.mode == "report":
            reporter = load_module("reporter")
            scanner = load_module("scanner")
            results = scanner.scan(args.target)
            reporter.generate(results, args.output or "report.html")
        return

    # Interactive Menu
    while True:
        print_menu()
        try:
            choice = input(f"\n  {C.CYAN}{C.BOLD}[Ankush@netprobe]➤ {C.RESET}").strip()
        except KeyboardInterrupt:
            print(f"\n  {C.GREEN}Bye! Stay Ethical — Ankush{C.RESET}\n"); sys.exit(0)

        if choice == "1":
            scanner = load_module("scanner")
            t = input(f"\n  {C.CYAN}[?] Network range (Enter=auto): {C.RESET}").strip()
            if not t:
                t = scanner.auto_detect_network()
                print(f"  {C.GREEN}[+] Auto-detected: {t}{C.RESET}")
            last_results = scanner.scan(t)
            scanner.display_results(last_results)

        elif choice == "2":
            scanner = load_module("scanner"); fp = load_module("fingerprint")
            t = input(f"\n  {C.CYAN}[?] Network range (Enter=auto): {C.RESET}").strip()
            if not t:
                t = scanner.auto_detect_network()
            devices = scanner.scan(t)
            fp.classify_and_display(devices)

        elif choice == "3":
            ps = load_module("port_scanner")
            ip = input(f"\n  {C.CYAN}[?] Target IP: {C.RESET}").strip()
            pr = input(f"  {C.CYAN}[?] Port range (default 1-1024): {C.RESET}").strip()
            s, e = 1, 1024
            if "-" in pr:
                try: s, e = map(int, pr.split("-"))
                except: pass
            ps.scan_ip(ip, s, e)

        elif choice == "4":
            arp = load_module("arp_detector"); scanner = load_module("scanner")
            t = input(f"\n  {C.CYAN}[?] Network range: {C.RESET}").strip()
            if not t: t = scanner.auto_detect_network()
            arp.detect(t)

        elif choice == "5":
            osint = load_module("osint")
            ip = input(f"\n  {C.CYAN}[?] IP for OSINT lookup: {C.RESET}").strip()
            osint.lookup(ip)

        elif choice == "6":
            reporter = load_module("reporter")
            if not last_results:
                print(f"\n  {C.YELLOW}[!] Run scan first (option 1){C.RESET}")
            else:
                fmt = input(f"\n  {C.CYAN}[?] Format: 1=HTML  2=PDF  3=JSON : {C.RESET}").strip()
                ext = {"1":"html","2":"pdf","3":"json"}.get(fmt,"html")
                fname = f"reports/netprobe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
                reporter.generate(last_results, fname)

        elif choice == "7":
            if not last_results:
                print(f"\n  {C.YELLOW}[!] Run scan first (option 1){C.RESET}")
            else:
                from modules.topology import TopologyMapper
                TopologyMapper().generate(last_results)

        elif choice == "8":
            from modules.dashboard import DashboardServer
            DashboardServer().run(last_results)

        elif choice == "9":
            alerts = load_module("alerts"); alerts.setup_telegram()

        elif choice == "10":
            wl = load_module("whitelist"); wl.interactive_menu()

        elif choice == "11":
            scanner = load_module("scanner"); alerts = load_module("alerts")
            t = input(f"\n  {C.CYAN}[?] Network range: {C.RESET}").strip()
            if not t: t = scanner.auto_detect_network()
            iv = input(f"  {C.CYAN}[?] Interval seconds (default 60): {C.RESET}").strip()
            iv = int(iv) if iv.isdigit() else 60
            scanner.monitor_mode(t, alerts, iv)

        elif choice == "12":
            reporter = load_module("reporter"); reporter.show_history()

        elif choice == "13":
            show_about()

        elif choice == "0":
            print(f"\n  {C.GREEN}[+] Exiting NetProbe. Stay Ethical! — Ankush{C.RESET}\n"); sys.exit(0)

        else:
            print(f"\n  {C.RED}[-] Invalid choice.{C.RESET}")

        try:
            input(f"\n  {C.DIM}Press Enter to continue...{C.RESET}")
        except KeyboardInterrupt:
            sys.exit(0)
        print_banner()

if __name__ == "__main__":
    main()
