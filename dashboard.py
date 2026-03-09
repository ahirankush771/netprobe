#!/usr/bin/env python3
"""
NetProbe - Live Web Dashboard
Author: Ankush (cybersecurity)
Flask-based real-time dashboard
"""
import json, os, threading, time
from datetime import datetime

class C:
    GREEN="\033[92m"; YELLOW="\033[93m"; CYAN="\033[96m"; RED="\033[91m"
    BOLD="\033[1m"; DIM="\033[2m"; RESET="\033[0m"

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NetProbe Dashboard | Ankush</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700&display=swap');
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:#040a12;color:#00ff88;font-family:'Share Tech Mono',monospace;overflow-x:hidden}
  .topbar{background:#0a1420;border-bottom:1px solid #00ff8833;padding:15px 30px;
          display:flex;justify-content:space-between;align-items:center}
  .topbar h1{font-family:'Orbitron',monospace;color:#00ff88;font-size:1.4rem;letter-spacing:3px}
  .topbar .author{color:#558866;font-size:0.8rem}
  .stats{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;padding:20px}
  .stat{background:#0a1a0a;border:1px solid #00ff8833;border-radius:8px;padding:20px;text-align:center}
  .stat .num{font-size:2.5rem;color:#00ff88;font-family:'Orbitron',monospace}
  .stat .lbl{color:#448855;font-size:0.75rem;text-transform:uppercase;letter-spacing:2px;margin-top:5px}
  .devices{padding:0 20px 20px}
  .devices h2{color:#00ff88;margin-bottom:15px;font-family:'Orbitron',monospace;font-size:1rem}
  table{width:100%;border-collapse:collapse}
  th{background:#0a1a12;color:#00cc66;padding:12px;text-align:left;font-size:0.75rem;
     text-transform:uppercase;letter-spacing:2px;border-bottom:1px solid #00ff8822}
  td{padding:10px 12px;border-bottom:1px solid #0a1a0a;font-size:0.85rem}
  tr:hover td{background:#0a1a0a}
  .badge{padding:3px 8px;border-radius:4px;font-size:0.7rem}
  .cam{background:#cc000033;color:#ff4444;border:1px solid #cc0000}
  .pc{background:#0000cc33;color:#4488ff;border:1px solid #0044cc}
  .phone{background:#00cc0033;color:#44ff88;border:1px solid #00aa44}
  .unknown{background:#33333333;color:#888;border:1px solid #444}
  .live-dot{width:8px;height:8px;background:#00ff88;border-radius:50%;
             display:inline-block;animation:pulse 1.5s infinite;margin-right:8px}
  @keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:0.4;transform:scale(1.3)}}
  .footer{text-align:center;padding:15px;color:#224433;font-size:0.75rem;border-top:1px solid #00ff8811}
</style>
</head>
<body>
<div class="topbar">
  <h1><span class="live-dot"></span>⚡ NETPROBE DASHBOARD</h1>
  <div class="author">👨‍💻 Ankush (cybersecurity) | NetProbe v2.0 | <span id="clock"></span></div>
</div>
<div class="stats">
  <div class="stat"><div class="num" id="total">0</div><div class="lbl">Total Devices</div></div>
  <div class="stat"><div class="num" id="cameras">0</div><div class="lbl">IP Cameras</div></div>
  <div class="stat"><div class="num" id="pcs">0</div><div class="lbl">PCs / Laptops</div></div>
  <div class="stat"><div class="num" id="phones">0</div><div class="lbl">Smartphones</div></div>
</div>
<div class="devices">
  <h2>📡 CONNECTED DEVICES</h2>
  <table>
    <thead><tr><th>#</th><th>IP Address</th><th>MAC Address</th><th>Vendor</th><th>Device Type</th><th>Hostname</th></tr></thead>
    <tbody id="device-table"><tr><td colspan="6" style="text-align:center;color:#446655">Waiting for scan data...</td></tr></tbody>
  </table>
</div>
<div class="footer">NetProbe v2.0 | Author: Ankush (cybersecurity) | For Authorized Use Only</div>
<script>
function updateClock(){
  document.getElementById('clock').textContent = new Date().toLocaleTimeString();
}
setInterval(updateClock, 1000); updateClock();

function getTypeBadge(type){
  if(!type) return '<span class="badge unknown">Unknown</span>';
  if(type.includes('Camera')) return `<span class="badge cam">${type}</span>`;
  if(type.includes('PC') || type.includes('Laptop')) return `<span class="badge pc">${type}</span>`;
  if(type.includes('Phone') || type.includes('Apple')) return `<span class="badge phone">${type}</span>`;
  return `<span class="badge unknown">${type}</span>`;
}

function fetchDevices(){
  fetch('/api/devices').then(r=>r.json()).then(data=>{
    document.getElementById('total').textContent = data.length;
    document.getElementById('cameras').textContent = data.filter(d=>d.device_type&&d.device_type.includes('Camera')).length;
    document.getElementById('pcs').textContent = data.filter(d=>d.device_type&&(d.device_type.includes('PC')||d.device_type.includes('Laptop'))).length;
    document.getElementById('phones').textContent = data.filter(d=>d.device_type&&(d.device_type.includes('Phone')||d.device_type.includes('Apple'))).length;

    const tbody = document.getElementById('device-table');
    if(data.length === 0){
      tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;color:#446655">No devices found. Run a scan first.</td></tr>';
      return;
    }
    tbody.innerHTML = data.map((d,i)=>`
      <tr>
        <td style="color:#446655">${i+1}</td>
        <td style="color:#00ff88"><strong>${d.ip||'N/A'}</strong></td>
        <td style="color:#ffaa00;font-size:0.75rem">${d.mac||'N/A'}</td>
        <td style="color:#88aacc">${d.vendor||'Unknown'}</td>
        <td>${getTypeBadge(d.device_type)}</td>
        <td style="color:#446655;font-size:0.8rem">${d.hostname||'Unknown'}</td>
      </tr>`).join('');
  }).catch(()=>{
    document.getElementById('device-table').innerHTML =
      '<tr><td colspan="6" style="text-align:center;color:#cc4444">Connection error</td></tr>';
  });
}
fetchDevices();
setInterval(fetchDevices, 5000);
</script>
</body>
</html>"""

class DashboardServer:
    def __init__(self):
        self.devices = []

    def run(self, devices=None):
        if devices:
            self.devices = devices

        try:
            from flask import Flask, jsonify, render_template_string
        except ImportError:
            print(f"\n  {C.RED}[-] Flask not installed. Run: pip install flask{C.RESET}")
            return

        app = Flask(__name__)
        dash = self  # reference

        @app.route("/")
        def index():
            return render_template_string(DASHBOARD_HTML)

        @app.route("/api/devices")
        def api_devices():
            # Also load from history if no live data
            if not dash.devices:
                try:
                    if os.path.exists("reports/scan_history.json"):
                        with open("reports/scan_history.json") as f:
                            history = json.load(f)
                        if history:
                            dash.devices = history[-1]["devices"]
                except:
                    pass
            return jsonify(dash.devices)

        print(f"\n  {C.GREEN}{C.BOLD}[+] Dashboard running at: http://localhost:5000{C.RESET}")
        print(f"  {C.CYAN}[*] Open your browser and go to: http://localhost:5000{C.RESET}")
        print(f"  {C.YELLOW}[!] Press Ctrl+C to stop dashboard{C.RESET}")
        print(f"  {C.DIM}    NetProbe by Ankush (cybersecurity){C.RESET}\n")

        try:
            app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
        except KeyboardInterrupt:
            print(f"\n  {C.YELLOW}[!] Dashboard stopped.{C.RESET}")
        except OSError as e:
            print(f"\n  {C.RED}[-] Port 5000 in use. Try: python3 -m flask run --port 5001{C.RESET}")
