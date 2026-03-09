#!/usr/bin/env python3
"""
NetProbe - Whitelist / Blacklist Manager
Author: Ankush (cybersecurity)
"""
import os, json

class C:
    RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"; CYAN="\033[96m"
    BOLD="\033[1m"; DIM="\033[2m"; RESET="\033[0m"

WL_FILE = ".whitelist.json"

class WhitelistManager:
    def __init__(self):
        self.data = self._load()

    def _load(self):
        if os.path.exists(WL_FILE):
            with open(WL_FILE) as f:
                return json.load(f)
        return {"whitelist": [], "blacklist": []}

    def _save(self):
        with open(WL_FILE, "w") as f:
            json.dump(self.data, f, indent=2)

    def is_whitelisted(self, ip_or_mac):
        return ip_or_mac in self.data["whitelist"]

    def is_blacklisted(self, ip_or_mac):
        return ip_or_mac in self.data["blacklist"]

    def interactive_menu(self):
        while True:
            wl = self.data["whitelist"]
            bl = self.data["blacklist"]
            print(f"\n  {C.CYAN}{C.BOLD}[ Whitelist / Blacklist Manager ]{C.RESET}")
            print(f"  {C.DIM}NetProbe by Ankush (cybersecurity){C.RESET}\n")
            print(f"  {C.GREEN}Whitelist ({len(wl)} entries): {wl[:5]}{C.RESET}")
            print(f"  {C.RED}Blacklist ({len(bl)} entries): {bl[:5]}{C.RESET}\n")
            print(f"  [1] Add to Whitelist (Trusted Device)")
            print(f"  [2] Add to Blacklist (Block/Alert Device)")
            print(f"  [3] Remove entry")
            print(f"  [4] View all entries")
            print(f"  [0] Back to main menu\n")

            choice = input(f"  {C.CYAN}> {C.RESET}").strip()

            if choice == "1":
                val = input(f"  {C.CYAN}[?] Enter IP or MAC to whitelist: {C.RESET}").strip()
                if val and val not in wl:
                    self.data["whitelist"].append(val)
                    self._save()
                    print(f"  {C.GREEN}[+] Added to whitelist: {val}{C.RESET}")

            elif choice == "2":
                val = input(f"  {C.CYAN}[?] Enter IP or MAC to blacklist: {C.RESET}").strip()
                if val and val not in bl:
                    self.data["blacklist"].append(val)
                    self._save()
                    print(f"  {C.RED}[+] Added to blacklist: {val}{C.RESET}")

            elif choice == "3":
                val = input(f"  {C.CYAN}[?] Enter IP or MAC to remove: {C.RESET}").strip()
                removed = False
                for lst in ["whitelist", "blacklist"]:
                    if val in self.data[lst]:
                        self.data[lst].remove(val)
                        removed = True
                if removed:
                    self._save()
                    print(f"  {C.YELLOW}[+] Removed: {val}{C.RESET}")
                else:
                    print(f"  {C.RED}[-] Not found.{C.RESET}")

            elif choice == "4":
                print(f"\n  {C.GREEN}{C.BOLD}Whitelist:{C.RESET}")
                for e in self.data["whitelist"]:
                    print(f"    ✔ {e}")
                print(f"\n  {C.RED}{C.BOLD}Blacklist:{C.RESET}")
                for e in self.data["blacklist"]:
                    print(f"    ✘ {e}")

            elif choice == "0":
                break
