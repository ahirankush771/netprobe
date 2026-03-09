#!/usr/bin/env python3
"""
NetProbe - Network Scanner Module
Author: Ankush (cybersecurity)
ARP-based WiFi network scanning
"""
import os, sys, socket, subprocess, ipaddress, time, json
from datetime import datetime

class C:
    RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"; CYAN="\033[96m"
    MAGENTA="\033[95m"; WHITE="\033[97m"; BOLD="\033[1m"; DIM="\033[2m"; RESET="\033[0m"

# MAC Vendor OUI Database (offline, partial)
MAC_VENDORS = {
    "00:50:56": "VMware", "08:00:27": "VirtualBox", "00:1A:2B": "Cisco",
    "B8:27:EB": "Raspberry Pi", "DC:A6:32": "Raspberry Pi",
    "00:11:22": "Unknown", "AC:DE:48": "Apple",
    "F4:5C:89": "Apple", "A4:C3:F0": "Apple", "00:1B:63": "Apple",
    "00:25:00": "Apple", "34:36:3B": "Apple", "3C:15:C2": "Apple",
    "18:65:90": "Apple", "28:CF:E9": "Apple", "4C:57:CA": "Apple",
    "00:15:5D": "Microsoft", "28:D2:44": "Microsoft",
    "00:E0:4C": "Realtek", "14:DD:A9": "Samsung", "F4:42:8F": "Samsung",
    "00:16:3E": "Xen Virtual", "00:1C:42": "Parallels",
    "00:0C:29": "VMware", "00:05:69": "VMware",
    "00:50:C2": "IEEE",  "D8:BB:C1": "Intel",
    "98:29:A6": "Intel", "00:21:6B": "Intel",
    "FC:AA:14": "TP-Link", "50:C7:BF": "TP-Link", "54:AF:97": "TP-Link",
    "14:91:82": "TP-Link", "C0:4A:00": "TP-Link", "EC:08:6B": "TP-Link",
    "00:90:4C": "Epigram (Camera)", "00:40:8C": "Axis (IP Camera)",
    "00:02:D1": "Hikvision Camera", "4C:11:BF": "Hikvision Camera",
    "00:10:18": "Dahua Camera",
}

def get_mac_vendor(mac):
    """Lookup MAC vendor from OUI prefix"""
    prefix = mac.upper()[:8]
    return MAC_VENDORS.get(prefix, "Unknown Vendor")

class NetworkScanner:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.history_file = "reports/scan_history.json"
        os.makedirs("reports", exist_ok=True)

    def auto_detect_network(self):
        """Auto-detect local network range"""
        try:
            import netifaces
            gws = netifaces.gateways()
            default_gw = gws.get('default', {}).get(netifaces.AF_INET)
            if default_gw:
                iface = default_gw[1]
                addrs = netifaces.ifaddresses(iface).get(netifaces.AF_INET, [{}])[0]
                ip   = addrs.get('addr', '')
                mask = addrs.get('netmask', '255.255.255.0')
                network = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
                return str(network)
        except ImportError:
            pass

        # Fallback: use hostname
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            parts = local_ip.split(".")
            return f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
        except:
            return "192.168.1.0/24"

    def scan(self, target):
        """Run ARP scan on target network"""
        print(f"\n  {C.YELLOW}[*] Starting ARP scan on: {C.WHITE}{target}{C.RESET}")
        print(f"  {C.DIM}Powered by NetProbe | Author: Ankush (cybersecurity){C.RESET}\n")

        devices = []

        # ── Try scapy first ───────────────────────────────────────────────
        try:
            from scapy.all import ARP, Ether, srp
            devices = self._scapy_scan(target)
        except ImportError:
            print(f"  {C.YELLOW}[!] Scapy not available, using fallback ping scan...{C.RESET}")
            devices = self._ping_scan(target)
        except PermissionError:
            print(f"  {C.RED}[-] Permission denied. Run as root (sudo) or tsu in Termux{C.RESET}")
            devices = self._ping_scan(target)

        # Enrich with MAC vendor + hostname
        for d in devices:
            d["vendor"]   = get_mac_vendor(d.get("mac", ""))
            d["hostname"] = self._get_hostname(d["ip"])
            d["scan_time"]= datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self._save_history(target, devices)
        return devices

    def _scapy_scan(self, target):
        """ARP scan using Scapy"""
        from scapy.all import ARP, Ether, srp
        print(f"  {C.CYAN}[*] Sending ARP packets...{C.RESET}")
        arp = ARP(pdst=target)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp
        result = srp(packet, timeout=3, verbose=0)[0]
        devices = []
        for sent, received in result:
            devices.append({"ip": received.psrc, "mac": received.hwsrc})
        return devices

    def _ping_scan(self, target):
        """Fallback: ping sweep"""
        print(f"  {C.CYAN}[*] Running ping sweep (fallback)...{C.RESET}")
        devices = []
        try:
            network = ipaddress.IPv4Network(target, strict=False)
            hosts = list(network.hosts())
            total = len(hosts)
            for i, host in enumerate(hosts):
                ip = str(host)
                sys.stdout.write(f"\r  {C.CYAN}[*] Scanning {i+1}/{total}: {ip}   {C.RESET}")
                sys.stdout.flush()
                flag = "-n" if os.name == "nt" else "-c"
                resp = subprocess.run(
                    ["ping", flag, "1", "-W", "1", ip],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                if resp.returncode == 0:
                    devices.append({"ip": ip, "mac": "N/A (No-root)"})
            print()
        except Exception as e:
            print(f"\n  {C.RED}[-] Scan error: {e}{C.RESET}")
        return devices

    def _get_hostname(self, ip):
        """Reverse DNS hostname lookup"""
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return "Unknown"

    def _save_history(self, target, devices):
        """Save scan to history"""
        history = []
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file) as f:
                    history = json.load(f)
            except:
                pass
        history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "target": target,
            "device_count": len(devices),
            "devices": devices
        })
        # Keep last 50 scans
        history = history[-50:]
        with open(self.history_file, "w") as f:
            json.dump(history, f, indent=2)

    def display_results(self, devices):
        """Pretty print scan results"""
        if not devices:
            print(f"\n  {C.RED}[-] No devices found. Check your network range.{C.RESET}")
            return

        print(f"\n  {C.GREEN}{C.BOLD}[+] Found {len(devices)} device(s) on network:{C.RESET}\n")
        print(f"  {C.CYAN}{'─'*75}{C.RESET}")
        print(f"  {C.BOLD}{'#':<4} {'IP Address':<18} {'MAC Address':<20} {'Vendor':<20} {'Hostname'}{C.RESET}")
        print(f"  {C.CYAN}{'─'*75}{C.RESET}")

        for i, d in enumerate(devices, 1):
            ip       = d.get("ip", "N/A")
            mac      = d.get("mac", "N/A")
            vendor   = d.get("vendor", "Unknown")[:18]
            hostname = d.get("hostname", "Unknown")[:20]
            print(f"  {C.GREEN}{i:<4}{C.RESET} {C.WHITE}{ip:<18}{C.RESET} {C.YELLOW}{mac:<20}{C.RESET} {C.MAGENTA}{vendor:<20}{C.RESET} {C.DIM}{hostname}{C.RESET}")

        print(f"  {C.CYAN}{'─'*75}{C.RESET}")
        print(f"\n  {C.DIM}Scan by: Ankush (cybersecurity) | NetProbe v2.0{C.RESET}")

    def monitor_mode(self, target, alerts, interval=60):
        """Continuous monitoring - alert on new devices"""
        print(f"\n  {C.CYAN}[*] Monitor Mode Started — interval: {interval}s{C.RESET}")
        print(f"  {C.YELLOW}[!] Press Ctrl+C to stop{C.RESET}\n")

        known_ips = set()
        scan_count = 0

        try:
            while True:
                scan_count += 1
                print(f"\n  {C.CYAN}[*] Scan #{scan_count} at {datetime.now().strftime('%H:%M:%S')}{C.RESET}")
                devices = self.scan(target)
                current_ips = {d["ip"] for d in devices}

                # New devices
                new_devices = current_ips - known_ips
                for ip in new_devices:
                    dev = next((d for d in devices if d["ip"] == ip), {})
                    print(f"\n  {C.RED}{C.BOLD}[!] NEW DEVICE DETECTED!{C.RESET}")
                    print(f"  {C.RED}    IP: {ip} | MAC: {dev.get('mac','?')} | Vendor: {dev.get('vendor','?')}{C.RESET}")
                    if alerts:
                        alerts.send_alert(f"⚠ NetProbe Alert!\nNew Device: {ip}\nMAC: {dev.get('mac','?')}\nVendor: {dev.get('vendor','?')}")

                # Disconnected devices
                gone = known_ips - current_ips
                for ip in gone:
                    print(f"  {C.YELLOW}[!] Device disconnected: {ip}{C.RESET}")

                known_ips = current_ips
                print(f"  {C.DIM}Next scan in {interval}s... (Ctrl+C to stop){C.RESET}")
                time.sleep(interval)

        except KeyboardInterrupt:
            print(f"\n  {C.YELLOW}[!] Monitor mode stopped.{C.RESET}")
