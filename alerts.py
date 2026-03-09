#!/usr/bin/env python3
"""
NetProbe - Alert Manager (Telegram)
Author: Ankush (cybersecurity)
"""
import os, json

class C:
    RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"; CYAN="\033[96m"
    BOLD="\033[1m"; DIM="\033[2m"; RESET="\033[0m"

CONFIG_FILE = ".alert_config.json"

class AlertManager:
    def __init__(self):
        self.config = self._load_config()

    def _load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE) as f:
                return json.load(f)
        return {"telegram_token": "", "telegram_chat_id": ""}

    def _save_config(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.config, f, indent=2)

    def setup_telegram(self):
        print(f"\n  {C.CYAN}{C.BOLD}[ Telegram Alert Setup ]{C.RESET}")
        print(f"  {C.DIM}Author: Ankush (cybersecurity) | NetProbe v2.0{C.RESET}\n")
        print(f"  {C.YELLOW}Step 1: Open Telegram, search @BotFather{C.RESET}")
        print(f"  {C.YELLOW}Step 2: Create bot with /newbot command{C.RESET}")
        print(f"  {C.YELLOW}Step 3: Copy the API token{C.RESET}")
        print(f"  {C.YELLOW}Step 4: Send a message to your bot, then get chat_id from:{C.RESET}")
        print(f"  {C.DIM}         https://api.telegram.org/bot<TOKEN>/getUpdates{C.RESET}\n")

        token = input(f"  {C.CYAN}[?] Bot Token: {C.RESET}").strip()
        chat_id = input(f"  {C.CYAN}[?] Chat ID:   {C.RESET}").strip()

        if token and chat_id:
            self.config["telegram_token"]   = token
            self.config["telegram_chat_id"] = chat_id
            self._save_config()

            # Test message
            self.send_alert("✅ NetProbe Alert Connected!\nAuthor: Ankush (cybersecurity)\nTool: NetProbe v2.0")
            print(f"\n  {C.GREEN}[+] Telegram configured! Test message sent.{C.RESET}")
        else:
            print(f"  {C.RED}[-] Setup cancelled.{C.RESET}")

    def send_alert(self, message):
        token   = self.config.get("telegram_token","")
        chat_id = self.config.get("telegram_chat_id","")
        if not token or not chat_id:
            return False
        try:
            import urllib.request, urllib.parse
            url  = f"https://api.telegram.org/bot{token}/sendMessage"
            data = urllib.parse.urlencode({"chat_id": chat_id, "text": message, "parse_mode":"HTML"}).encode()
            urllib.request.urlopen(url, data, timeout=5)
            return True
        except Exception as e:
            print(f"  {C.RED}[-] Telegram error: {e}{C.RESET}")
            return False
