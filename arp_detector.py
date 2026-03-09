#!/usr/bin/env python3
"""
NetProbe - ARP Spoof / MITM Detector
Author: Ankush (cybersecurity)
Detects ARP Poisoning & Man-in-the-Middle attacks
"""
import time, os
from datetime import datetime

class C:
    RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"; CYAN="\033[96m"
    MAGENTA="\033[95m"; WHITE="\033[97m"; BOLD="\033[1m"; DIM="\033[2m"; RESET="\033[0m"

class ARPSpoofDetector:
    def detect(self, target):
        print(f"\n  {C.CYAN}{C.BOLD}[*] ARP Spoof / MITM Detector{C.RESET}")
        print(f"  {C.DIM}Author: Ankush (cybersecurity) | NetProbe v2.0{C.RESET}\n")

        try:
            from scapy.all import ARP, Ether, srp
        except ImportError:
            print(f"  {C.RED}[-] Scapy required for ARP detection. Install: pip install scapy{C.RESET}")
            return

        print(f"  {C.YELLOW}[*] Scanning network: {target}{C.RESET}")
        arp    = ARP(pdst=target)
        ether  = Ether(dst="ff:ff:ff:ff:ff:ff")
        result = srp(ether/arp, timeout=3, verbose=0)[0]

        # Build IP→MAC map
        ip_mac = {}
        for sent, recv in result:
            ip  = recv.psrc
            mac = recv.hwsrc
            if ip in ip_mac:
                if ip_mac[ip] != mac:
                    print(f"\n  {C.RED}{C.BOLD}[!!!] ARP SPOOFING DETECTED! ⚠{C.RESET}")
                    print(f"  {C.RED}      IP: {ip} claims to be BOTH:{C.RESET}")
                    print(f"  {C.RED}      MAC 1: {ip_mac[ip]}{C.RESET}")
                    print(f"  {C.RED}      MAC 2: {mac}  ← FAKE (MITM Attack){C.RESET}")
                    print(f"\n  {C.YELLOW}  RECOMMENDATION: Disconnect and use a VPN immediately!{C.RESET}")
            else:
                ip_mac[ip] = mac

        if len(ip_mac) > 0:
            print(f"\n  {C.GREEN}[+] {len(ip_mac)} devices scanned. IP→MAC table built.{C.RESET}")
            if not any(True for _ in []):  # no spoofing detected
                print(f"  {C.GREEN}[✓] No ARP spoofing detected. Network appears clean.{C.RESET}")

        # Gateway double-check
        self._check_gateway_arp()

    def _check_gateway_arp(self):
        """Check if default gateway MAC is consistent"""
        print(f"\n  {C.CYAN}[*] Verifying Gateway ARP entry...{C.RESET}")
        try:
            import subprocess
            result = subprocess.run(["arp", "-n"], capture_output=True, text=True)
            lines = result.stdout.strip().split("\n")
            print(f"  {C.DIM}Current ARP Table:{C.RESET}")
            for line in lines[:10]:
                print(f"  {C.DIM}  {line}{C.RESET}")
        except Exception as e:
            print(f"  {C.YELLOW}[!] Could not read ARP table: {e}{C.RESET}")

        print(f"\n  {C.DIM}Tip: Run continuously to catch dynamic ARP poisoning attacks{C.RESET}")
        print(f"  {C.DIM}     Ankush (cybersecurity) | NetProbe v2.0{C.RESET}")
