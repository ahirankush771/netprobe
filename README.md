# ⚡ NetProbe v2.0 — WiFi Network Scanner & Security Analyzer

<p align="center">
  <img src="https://img.shields.io/badge/Author-Ankush-00d4ff?style=for-the-badge&logo=github"/>
  <img src="https://img.shields.io/badge/Role-cybersecurity%20Researcher-ff4444?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Python-3.7+-yellow?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/Platform-Kali%20Linux%20%7C%20Termux-blueviolet?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>
</p>

<p align="center">
  <b>A complete WiFi network recon & security toolkit for Kali Linux and Termux (Android)</b>
</p>

---

## 👨‍💻 Author

| | |
|---|---|
| **Name** | Ankush |
| **Role** | cybersecurity Researcher & Tool Developer |
| **Platform** | Kali Linux, Termux Android |
| **GitHub** | [@Ahirankush771](https://github.com/Ahirankush771) |

---

## 🚀 Features

| Feature | Description |
|--------|-------------|
| 🔍 **WiFi Network Scan** | ARP-based device discovery on local network |
| 📱 **Device Classifier** | Automatically identifies Camera / PC / Phone / Router / IoT |
| 🔌 **Port Scanner** | Multi-threaded TCP port scanner with service detection |
| 🛡 **ARP Spoof Detector** | Detects MITM / ARP poisoning attacks |
| 🌍 **OSINT Module** | GeoIP + Shodan lookup + Reverse DNS |
| 📊 **Report Generator** | HTML / PDF / JSON professional reports |
| 🗺 **Topology Map** | Interactive visual network map (browser) |
| 🌐 **Live Dashboard** | Real-time web dashboard (Flask) |
| 🔔 **Telegram Alerts** | Instant alert when new device joins network |
| ✅ **Whitelist/Blacklist** | Trusted & blocked device management |
| 📡 **Monitor Mode** | Continuous scanning with auto-alerts |
| 📜 **Scan History** | View and compare past scans |

---

## 📦 Installation

### 🐉 Kali Linux

```bash
git clone https://github.com/Ahirankush771/netprobe.git
cd netprobe
sudo bash install.sh
```

### 📱 Termux (Android)

```bash
pkg update && pkg install git python
git clone https://github.com/Ahirankush771/netprobe.git
cd netprobe
bash install.sh
```

> ⚠ **Root required** in Termux for ARP scanning. Use `tsu` command.

---

## 🎮 Usage

### Interactive Menu (Recommended)
```bash
# Kali Linux
sudo python3 main.py

# Termux (with root)
tsu
python3 main.py
```

### Command Line Mode
```bash
# Quick network scan
sudo python3 main.py -t 192.168.1.0/24 -m scan

# Port scan specific IP
sudo python3 main.py -t 192.168.1.105 -m ports

# ARP spoof detection
sudo python3 main.py -t 192.168.1.0/24 -m arp

# OSINT on public IP
python3 main.py -t 8.8.8.8 -m osint

# Generate HTML report
sudo python3 main.py -t 192.168.1.0/24 -m report -o reports/scan.html

# Monitor mode (alert on new devices)
sudo python3 main.py --monitor --interval 30

# Launch web dashboard
python3 main.py --dashboard
```

---

## 📁 Project Structure

```
netprobe/
├── 📄 main.py                    ← Main tool entry point
├── 📄 install.sh                 ← Auto installer (Kali + Termux)
├── 📄 requirements.txt           ← Python dependencies
├── 📄 README.md
├── 📄 LICENSE
│
├── 📁 modules/
│   ├── scanner.py                ← ARP WiFi scanner + monitor mode
│   ├── fingerprint.py            ← Device type classifier
│   ├── port_scanner.py           ← Multi-threaded port scanner
│   ├── arp_detector.py           ← ARP spoof / MITM detection
│   ├── osint.py                  ← GeoIP + Shodan + DNS
│   ├── alerts.py                 ← Telegram bot alerts
│   ├── reporter.py               ← HTML/PDF/JSON reports
│   ├── topology.py               ← Network topology map
│   ├── dashboard.py              ← Flask web dashboard
│   └── whitelist.py              ← Whitelist/blacklist manager
│
└── 📁 reports/                   ← Auto-generated scan reports
```

---

## 🖥 Screenshots

> Run the tool and take screenshots here!

---

## 📱 Device Classification

NetProbe automatically classifies devices using:
- **MAC OUI** — Vendor identification from MAC prefix
- **Port Probing** — Common port fingerprinting
- **Hostname Analysis** — Reverse DNS hostname patterns

| Icon | Device Type |
|------|------------|
| 📷 | IP Camera (Hikvision, Dahua, Axis, etc.) |
| 💻 | PC / Laptop |
| 📱 | Android Smartphone |
| 🍎 | Apple Device (iPhone, iPad, MacBook) |
| 📺 | Smart TV |
| 🔌 | Router / Gateway |
| 🖨 | Printer |
| 🏠 | IoT / Smart Device |

---

## ⚠ Legal Disclaimer

> This tool is created by **Ankush** for **educational purposes** and **authorized penetration testing only**.
> 
> ❌ Do NOT use on networks you don't own or have explicit permission to test.
> ✅ Always get written authorization before pentesting any network.
> 
> The author (Ankush) is not responsible for any misuse of this tool.

---

## 📄 License

MIT License — Free to use, modify, and distribute with attribution.

---

<p align="center">Made with ❤ by <b>Ankush</b> | cybersecurity Researcher</p>
