#!/usr/bin/env python3
"""
NetProbe - Device Fingerprinter & Classifier
Author: Ankush (cybersecurity)
Classifies: Camera | PC/Laptop | Phone | Router | IoT | Smart TV
"""
import socket

class C:
    RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"; CYAN="\033[96m"
    MAGENTA="\033[95m"; WHITE="\033[97m"; BOLD="\033[1m"; DIM="\033[2m"; RESET="\033[0m"

# ── Device Classification Rules ───────────────────────────────────────────
DEVICE_PROFILES = {
    "📷 IP Camera": {
        "mac_vendors": ["hikvision", "dahua", "axis", "vivotek", "foscam", "amcrest",
                        "reolink", "epiphan", "camera", "hanwha", "bosch security"],
        "open_ports":  [80, 443, 554, 8080, 8554, 37777, 34567],
        "hostnames":   ["camera", "cam", "ipcam", "dvr", "nvr", "cctv"],
    },
    "💻 PC / Laptop": {
        "mac_vendors": ["intel", "realtek", "dell", "hp", "lenovo", "asus", "acer",
                        "microsoft surface", "gigabyte", "msi"],
        "open_ports":  [135, 139, 445, 3389, 22, 5900],
        "hostnames":   ["desktop", "laptop", "pc", "workstation", "windows"],
    },
    "📱 Smartphone": {
        "mac_vendors": ["samsung", "xiaomi", "oneplus", "oppo", "vivo", "realme",
                        "huawei", "motorola", "lg mobile", "google"],
        "open_ports":  [5555, 62078],
        "hostnames":   ["android", "phone", "mobile", "iphone", "pixel"],
    },
    "🍎 Apple Device": {
        "mac_vendors": ["apple"],
        "open_ports":  [62078, 7000, 7100, 5000],
        "hostnames":   ["iphone", "ipad", "macbook", "imac", "apple"],
    },
    "📺 Smart TV": {
        "mac_vendors": ["samsung", "lg electronics", "sony", "tcl", "hisense", "philips",
                        "vizio", "sharp"],
        "open_ports":  [8001, 8002, 1925, 7676, 9197],
        "hostnames":   ["tv", "smarttv", "bravia", "tizen", "webos"],
    },
    "🔌 Router / Gateway": {
        "mac_vendors": ["tp-link", "netgear", "asus", "d-link", "linksys", "cisco",
                        "mikrotik", "ubiquiti", "tenda", "huawei", "zyxel"],
        "open_ports":  [80, 443, 23, 22, 8080, 8443, 53],
        "hostnames":   ["router", "gateway", "dlink", "tplink", "netgear", "asus"],
    },
    "🖨 Printer": {
        "mac_vendors": ["hp", "canon", "epson", "brother", "lexmark", "xerox", "ricoh"],
        "open_ports":  [9100, 515, 631],
        "hostnames":   ["printer", "print", "hp", "canon", "epson"],
    },
    "🏠 IoT / Smart Device": {
        "mac_vendors": ["espressif", "raspberry pi", "arduino", "tuya", "shelly",
                        "sonoff", "wemos", "belkin"],
        "open_ports":  [1883, 8883, 4840, 102, 502],
        "hostnames":   ["esp", "iot", "smart", "sensor", "bulb", "plug"],
    },
}

def quick_port_check(ip, ports, timeout=0.5):
    """Fast port probe for classification"""
    open_ports = []
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            if s.connect_ex((ip, port)) == 0:
                open_ports.append(port)
            s.close()
        except:
            pass
    return open_ports

def classify_device(ip, mac, vendor, hostname):
    """
    Classify device type using MAC vendor + open ports + hostname hints.
    Returns (device_type, confidence, open_ports)
    """
    vendor_lower   = vendor.lower()
    hostname_lower = hostname.lower()
    scores         = {}
    found_ports    = []

    for device_type, profile in DEVICE_PROFILES.items():
        score = 0

        # MAC vendor match
        for v in profile["mac_vendors"]:
            if v in vendor_lower:
                score += 50
                break

        # Hostname match
        for h in profile["hostnames"]:
            if h in hostname_lower:
                score += 30
                break

        if score > 0:
            scores[device_type] = score

    # Port-based classification (only if no strong match yet)
    if not scores or max(scores.values(), default=0) < 50:
        # Check common ports
        all_ports = []
        for profile in DEVICE_PROFILES.values():
            all_ports.extend(profile["open_ports"])
        all_ports = list(set(all_ports))

        found_ports = quick_port_check(ip, all_ports[:15])  # check top 15 ports

        for device_type, profile in DEVICE_PROFILES.items():
            port_hits = len(set(found_ports) & set(profile["open_ports"]))
            if port_hits > 0:
                scores[device_type] = scores.get(device_type, 0) + (port_hits * 20)

    if not scores:
        return "❓ Unknown Device", "Low", found_ports

    best = max(scores, key=scores.get)
    conf_val = scores[best]
    confidence = "High" if conf_val >= 50 else "Medium" if conf_val >= 20 else "Low"

    return best, confidence, found_ports

class DeviceFingerprinter:
    def __init__(self):
        pass

    def classify_and_display(self, devices):
        """Classify all devices and display grouped by type"""
        if not devices:
            print(f"\n  {C.RED}[-] No devices to classify.{C.RESET}")
            return

        print(f"\n  {C.YELLOW}[*] Classifying {len(devices)} device(s)...{C.RESET}")
        print(f"  {C.DIM}(Using MAC OUI + Port Probing + Hostname Analysis){C.RESET}\n")

        classified = {}

        for i, d in enumerate(devices):
            ip       = d.get("ip", "N/A")
            mac      = d.get("mac", "N/A")
            vendor   = d.get("vendor", "Unknown")
            hostname = d.get("hostname", "")

            print(f"  {C.DIM}[{i+1}/{len(devices)}] Fingerprinting {ip}...{C.RESET}", end="\r")

            dtype, confidence, ports = classify_device(ip, mac, vendor, hostname)
            d["device_type"]  = dtype
            d["confidence"]   = confidence
            d["probed_ports"] = ports

            if dtype not in classified:
                classified[dtype] = []
            classified[dtype].append(d)

        print(" " * 60)  # clear line

        # ── Grouped Display ───────────────────────────────────────────────
        print(f"\n  {C.CYAN}{C.BOLD}{'═'*70}{C.RESET}")
        print(f"  {C.BOLD}         DEVICE CLASSIFICATION REPORT — by Ankush (cybersecurity){C.RESET}")
        print(f"  {C.CYAN}{'═'*70}{C.RESET}\n")

        for dtype, devs in classified.items():
            print(f"  {C.BOLD}{C.YELLOW}{dtype}  ({len(devs)} found){C.RESET}")
            print(f"  {C.DIM}{'─'*65}{C.RESET}")
            for d in devs:
                ip       = d.get("ip","N/A")
                mac      = d.get("mac","N/A")
                vendor   = d.get("vendor","?")[:15]
                conf     = d.get("confidence","?")
                ports    = d.get("probed_ports",[])
                hostname = d.get("hostname","?")[:20]

                conf_color = C.GREEN if conf=="High" else C.YELLOW if conf=="Medium" else C.RED
                print(f"  {C.WHITE}  IP: {ip:<17}{C.RESET} MAC: {C.YELLOW}{mac:<20}{C.RESET} Vendor: {C.MAGENTA}{vendor:<16}{C.RESET}")
                print(f"              Hostname: {C.CYAN}{hostname:<22}{C.RESET} Confidence: {conf_color}{conf}{C.RESET}", end="")
                if ports:
                    print(f"  Open Ports: {C.GREEN}{ports}{C.RESET}")
                else:
                    print()
                print()
            print()

        print(f"  {C.CYAN}{'═'*70}{C.RESET}")
        print(f"  {C.DIM}Total: {len(devices)} devices | Types: {len(classified)} | Tool: NetProbe by Ankush{C.RESET}\n")

        return classified
