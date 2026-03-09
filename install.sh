#!/bin/bash
# ╔══════════════════════════════════════════════════════════════╗
# ║         NetProbe - Auto Installer                           ║
# ║         Works on: Kali Linux | Termux (Android)            ║
# ║         Author: Ankush | cybersecurity                      ║
# ╚══════════════════════════════════════════════════════════════╝

RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
CYAN='\033[96m'
BOLD='\033[1m'
RESET='\033[0m'

echo -e "${CYAN}${BOLD}"
echo " ███╗   ██╗███████╗████████╗██████╗ ██████╗  ██████╗ ██████╗ "
echo " ████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗"
echo " ██╔██╗ ██║█████╗     ██║   ██████╔╝██████╔╝██║   ██║██████╔╝"
echo " ██║╚██╗██║██╔══╝     ██║   ██╔═══╝ ██╔══██╗██║   ██║██╔══██╗"
echo " ██║ ╚████║███████╗   ██║   ██║     ██║  ██║╚██████╔╝██████╔╝"
echo " ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ "
echo -e "${RESET}"
echo -e "${GREEN}        Auto Installer | Author: Ankush (cybersecurity)${RESET}"
echo -e "${YELLOW}        Platform Detection...${RESET}"
echo ""

# ─── Detect Platform ──────────────────────────────────────────
detect_platform() {
    if [ -d "/data/data/com.termux" ] || [ "$TERMUX_VERSION" != "" ]; then
        echo "termux"
    elif [ -f "/etc/kali-release" ] || grep -qi "kali" /etc/os-release 2>/dev/null; then
        echo "kali"
    elif [ -f "/etc/debian_version" ] || grep -qi "debian\|ubuntu" /etc/os-release 2>/dev/null; then
        echo "debian"
    else
        echo "unknown"
    fi
}

PLATFORM=$(detect_platform)
echo -e "${CYAN}[*] Detected Platform: ${YELLOW}${PLATFORM}${RESET}"
echo ""

# ─── Termux Install ───────────────────────────────────────────
install_termux() {
    echo -e "${GREEN}[+] Installing for Termux (Android)...${RESET}"
    
    echo -e "${CYAN}[*] Updating Termux packages...${RESET}"
    pkg update -y && pkg upgrade -y
    
    echo -e "${CYAN}[*] Installing system dependencies...${RESET}"
    pkg install -y python python-pip nmap net-tools iproute2 libxml2 libxslt
    pkg install -y openssl-tool wget curl git
    
    echo -e "${CYAN}[*] Installing Python packages...${RESET}"
    pip install --upgrade pip
    pip install scapy requests python-nmap rich colorama
    pip install reportlab jinja2 flask
    pip install python-telegram-bot
    pip install netifaces geoip2
    
    echo -e "${GREEN}[+] Termux setup complete!${RESET}"
    echo -e "${YELLOW}[!] Note: Some features (raw sockets) need root on Android${RESET}"
    echo -e "${YELLOW}[!] Use: tsu (Termux su) for full functionality${RESET}"
}

# ─── Kali Linux Install ───────────────────────────────────────
install_kali() {
    echo -e "${GREEN}[+] Installing for Kali Linux...${RESET}"
    
    if [ "$EUID" -ne 0 ]; then
        echo -e "${RED}[-] Run as root: sudo bash install.sh${RESET}"
        exit 1
    fi
    
    echo -e "${CYAN}[*] Updating apt packages...${RESET}"
    apt-get update -y
    
    echo -e "${CYAN}[*] Installing system dependencies...${RESET}"
    apt-get install -y python3 python3-pip python3-dev
    apt-get install -y nmap net-tools iproute2 arp-scan
    apt-get install -y libssl-dev libffi-dev build-essential
    apt-get install -y wkhtmltopdf git curl wget
    
    echo -e "${CYAN}[*] Installing Python packages...${RESET}"
    pip3 install --upgrade pip
    pip3 install scapy requests python-nmap rich colorama
    pip3 install reportlab jinja2 flask
    pip3 install python-telegram-bot
    pip3 install netifaces geoip2 shodan
    pip3 install networkx matplotlib
    
    echo -e "${GREEN}[+] Kali Linux setup complete!${RESET}"
}

# ─── Debian/Ubuntu Install ────────────────────────────────────
install_debian() {
    echo -e "${GREEN}[+] Installing for Debian/Ubuntu...${RESET}"
    
    if [ "$EUID" -ne 0 ]; then
        echo -e "${RED}[-] Run as root: sudo bash install.sh${RESET}"
        exit 1
    fi
    
    apt-get update -y
    apt-get install -y python3 python3-pip nmap net-tools
    pip3 install scapy requests python-nmap rich colorama
    pip3 install reportlab jinja2 flask python-telegram-bot
    pip3 install netifaces geoip2 shodan networkx matplotlib
    
    echo -e "${GREEN}[+] Setup complete!${RESET}"
}

# ─── Run Installer ────────────────────────────────────────────
case $PLATFORM in
    termux)  install_termux ;;
    kali)    install_kali ;;
    debian)  install_debian ;;
    *)
        echo -e "${YELLOW}[!] Unknown platform. Running generic install...${RESET}"
        pip3 install scapy requests rich colorama reportlab jinja2 flask
        pip3 install python-telegram-bot netifaces geoip2
        ;;
esac

# ─── Set Permissions ──────────────────────────────────────────
echo ""
echo -e "${CYAN}[*] Setting permissions...${RESET}"
chmod +x main.py
chmod +x install.sh

echo ""
echo -e "${GREEN}${BOLD}╔══════════════════════════════════════════╗${RESET}"
echo -e "${GREEN}${BOLD}║   ✅  NetProbe Installation Complete!   ║${RESET}"
echo -e "${GREEN}${BOLD}╠══════════════════════════════════════════╣${RESET}"
echo -e "${GREEN}║                                          ║${RESET}"
echo -e "${GREEN}║   Run tool:  python3 main.py             ║${RESET}"
echo -e "${GREEN}║   Help:      python3 main.py --help      ║${RESET}"
echo -e "${GREEN}║                                          ║${RESET}"
echo -e "${GREEN}║   Author: Ankush | cybersecurity         ║${RESET}"
echo -e "${GREEN}${BOLD}╚══════════════════════════════════════════╝${RESET}"
echo ""
