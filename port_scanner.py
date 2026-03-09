#!/usr/bin/env python3
"""
NetProbe - Port Scanner Module
Author: Ankush (cybersecurity)
TCP/UDP Port Scanning with service detection
"""
import socket, threading, time
from datetime import datetime
from queue import Queue

class C:
    RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"; CYAN="\033[96m"
    MAGENTA="\033[95m"; WHITE="\033[97m"; BOLD="\033[1m"; DIM="\033[2m"; RESET="\033[0m"

# Common port → service name
PORT_SERVICES = {
    21:"FTP", 22:"SSH", 23:"Telnet (⚠ Insecure)", 25:"SMTP", 53:"DNS",
    80:"HTTP", 110:"POP3", 143:"IMAP", 443:"HTTPS", 445:"SMB (File Share)",
    554:"RTSP (IP Camera)", 993:"IMAPS", 995:"POP3S", 1080:"SOCKS Proxy",
    1433:"MSSQL", 1883:"MQTT (IoT)", 3306:"MySQL", 3389:"RDP (Remote Desktop)",
    5432:"PostgreSQL", 5900:"VNC (Remote Desktop)", 6379:"Redis",
    7547:"TR-069 (Router)", 8080:"HTTP Alt", 8443:"HTTPS Alt",
    8554:"RTSP Alt (Camera)", 8888:"HTTP Dev", 9200:"Elasticsearch",
    27017:"MongoDB", 37777:"Dahua Camera", 34567:"DVR Camera",
    62078:"iPhone Sync", 5555:"Android Debug (ADB)",
}

RISK_PORTS = {23, 21, 3389, 5900, 5555, 27017, 9200, 6379, 1080}  # High risk if open

class PortScanner:
    def __init__(self, threads=100, timeout=0.8, verbose=False):
        self.threads  = threads
        self.timeout  = timeout
        self.verbose  = verbose
        self.open_ports = []
        self.lock     = threading.Lock()
        self.queue    = Queue()

    def _worker(self):
        while True:
            port = self.queue.get()
            if port is None:
                break
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(self.timeout)
                if s.connect_ex((self._target_ip, port)) == 0:
                    service = PORT_SERVICES.get(port, "Unknown")
                    risk    = "🔴 HIGH RISK" if port in RISK_PORTS else ""
                    with self.lock:
                        self.open_ports.append((port, service, risk))
                s.close()
            except:
                pass
            finally:
                self.queue.task_done()

    def scan_ip(self, ip, start=1, end=1024):
        """Scan ports on a single IP"""
        self._target_ip = ip
        self.open_ports = []

        print(f"\n  {C.CYAN}{C.BOLD}[*] Port Scan: {ip} | Range: {start}-{end}{C.RESET}")
        print(f"  {C.DIM}NetProbe by Ankush (cybersecurity){C.RESET}\n")

        start_time = time.time()

        # Start threads
        thread_list = []
        for _ in range(min(self.threads, 200)):
            t = threading.Thread(target=self._worker, daemon=True)
            t.start()
            thread_list.append(t)

        # Fill queue
        total = end - start + 1
        for port in range(start, end + 1):
            self.queue.put(port)

        # Progress display
        done = 0
        while not self.queue.empty():
            current = total - self.queue.qsize()
            pct = (current / total) * 100
            bar = "█" * int(pct // 4) + "░" * (25 - int(pct // 4))
            sys.stdout.write(f"\r  {C.CYAN}[{bar}] {pct:.1f}%  Scanned: {current}/{total}{C.RESET}")
            sys.stdout.flush()
            time.sleep(0.2)

        # Stop threads
        for _ in thread_list:
            self.queue.put(None)
        for t in thread_list:
            t.join()

        elapsed = time.time() - start_time
        print(f"\r  {C.GREEN}[✓] Scan complete in {elapsed:.1f}s{' '*30}{C.RESET}\n")

        self.open_ports.sort(key=lambda x: x[0])
        self._display_results(ip, start, end)
        return self.open_ports

    def _display_results(self, ip, start, end):
        """Display port scan results"""
        print(f"  {C.CYAN}{'─'*60}{C.RESET}")
        print(f"  {C.BOLD}PORT SCAN RESULTS — {ip}{C.RESET}")
        print(f"  {C.CYAN}{'─'*60}{C.RESET}")

        if not self.open_ports:
            print(f"  {C.YELLOW}  No open ports found in range {start}-{end}{C.RESET}")
        else:
            print(f"  {C.BOLD}{'PORT':<8} {'SERVICE':<30} {'STATUS':<10} {'RISK'}{C.RESET}")
            print(f"  {'─'*58}")
            for port, service, risk in self.open_ports:
                risk_color = C.RED if risk else C.GREEN
                status_color = C.GREEN
                print(f"  {C.YELLOW}{port:<8}{C.RESET} {C.WHITE}{service:<30}{C.RESET} {status_color}OPEN{C.RESET}       {risk_color}{risk}{C.RESET}")

        print(f"  {C.CYAN}{'─'*60}{C.RESET}")
        print(f"  {C.DIM}Total open: {len(self.open_ports)} | Scanned: {start}-{end} | By Ankush{C.RESET}\n")

import sys
