#!/usr/bin/env python3
"""
NetProbe - Network Topology Mapper
Author: Ankush (cybersecurity)
Generates visual network map as HTML
"""
import os, json
from datetime import datetime

class C:
    GREEN="\033[92m"; YELLOW="\033[93m"; CYAN="\033[96m"; RED="\033[91m"
    BOLD="\033[1m"; DIM="\033[2m"; RESET="\033[0m"

DEVICE_ICONS = {
    "📷 IP Camera"      : "📷",
    "💻 PC / Laptop"    : "💻",
    "📱 Smartphone"     : "📱",
    "🍎 Apple Device"   : "🍎",
    "📺 Smart TV"       : "📺",
    "🔌 Router / Gateway": "🔌",
    "🖨 Printer"        : "🖨",
    "🏠 IoT / Smart Device": "🏠",
    "❓ Unknown Device" : "❓",
}

class TopologyMapper:
    def generate(self, devices, output="reports/topology.html"):
        os.makedirs("reports", exist_ok=True)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Build node data for vis.js
        nodes = []
        # Add router/gateway as center
        nodes.append({
            "id": 0, "label": "🔌 Gateway\\n192.168.1.1",
            "color": {"background":"#00d4ff","border":"#0099bb"},
            "shape":"box", "size": 40, "font":{"color":"#000","size":14}
        })

        edges = []
        for i, d in enumerate(devices, 1):
            ip    = d.get("ip","?")
            dtype = d.get("device_type","❓ Unknown Device")
            icon  = next((v for k,v in DEVICE_ICONS.items() if k in dtype), "❓")
            mac   = d.get("mac","?")[:17]
            vendor= d.get("vendor","?")[:12]
            label = f"{icon}\\n{ip}\\n{vendor}"
            color = self._node_color(dtype)

            nodes.append({
                "id": i, "label": label,
                "title": f"IP: {ip}\\nMAC: {mac}\\nType: {dtype}\\nVendor: {d.get('vendor','?')}",
                "color": color, "shape":"box",
                "font":{"color":"#ffffff","size":11}
            })
            edges.append({"from": 0, "to": i, "color":{"color":"#2244aa"}})

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>NetProbe - Network Topology | Ankush</title>
<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
<style>
  body {{ margin:0; background:#060d1a; font-family:'Courier New',monospace; color:#e0e0e0; }}
  #header {{ background:linear-gradient(135deg,#0d1b2a,#1a3a5c); padding:20px 30px;
             border-bottom:1px solid #00d4ff33; display:flex; justify-content:space-between; align-items:center; }}
  #header h1 {{ color:#00d4ff; font-size:1.8rem; letter-spacing:3px; }}
  #header .meta {{ color:#88aacc; font-size:0.85rem; text-align:right; }}
  #network {{ width:100%; height:calc(100vh - 80px); }}
  .legend {{ position:fixed; bottom:20px; left:20px; background:#0d1520ee;
             border:1px solid #1e3a5f; border-radius:10px; padding:15px; font-size:0.8rem; }}
  .legend h3 {{ color:#00d4ff; margin-bottom:10px; }}
  .legend div {{ margin:4px 0; }}
</style>
</head>
<body>
<div id="header">
  <h1>⚡ NETPROBE — Network Topology</h1>
  <div class="meta">
    <div>👨‍💻 Author: <strong>Ankush (cybersecurity)</strong></div>
    <div>🕐 {now} | {len(devices)} Devices</div>
  </div>
</div>
<div id="network"></div>
<div class="legend">
  <h3>Legend</h3>
  <div>🔌 Router/Gateway</div>
  <div>📷 IP Camera</div>
  <div>💻 PC/Laptop</div>
  <div>📱 Smartphone</div>
  <div>📺 Smart TV</div>
  <div>🏠 IoT Device</div>
  <div>❓ Unknown</div>
</div>
<script>
var nodes = new vis.DataSet({json.dumps(nodes)});
var edges = new vis.DataSet({json.dumps(edges)});
var container = document.getElementById('network');
var data = {{ nodes: nodes, edges: edges }};
var options = {{
  nodes: {{ borderWidth:2, shadow:true, font:{{ face:'Courier New' }} }},
  edges: {{ width:2, shadow:true, smooth:{{ type:'curvedCW', roundness:0.2 }} }},
  physics: {{ stabilization:{{ iterations:200 }}, barnesHut:{{ gravitationalConstant:-8000, centralGravity:0.3 }} }},
  interaction: {{ hover:true, tooltipDelay:100 }},
  layout: {{ improvedLayout:true }}
}};
var network = new vis.Network(container, data, options);
</script>
</body>
</html>"""

        with open(output, "w") as f:
            f.write(html)

        print(f"\n  {C.GREEN}[+] Topology map saved: {output}{C.RESET}")
        print(f"  {C.CYAN}[*] Open in browser to view interactive network map!{C.RESET}")

        # Try to auto-open
        try:
            import subprocess, sys
            if sys.platform == "linux":
                subprocess.Popen(["xdg-open", output], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass

    def _node_color(self, dtype):
        colors = {
            "Camera" : {"background":"#cc3300","border":"#ff4400"},
            "PC"     : {"background":"#004488","border":"#0066cc"},
            "Laptop" : {"background":"#004488","border":"#0066cc"},
            "Phone"  : {"background":"#006633","border":"#00aa55"},
            "Apple"  : {"background":"#555555","border":"#888888"},
            "TV"     : {"background":"#663300","border":"#996600"},
            "Router" : {"background":"#004455","border":"#00aacc"},
            "Printer": {"background":"#443300","border":"#886600"},
            "IoT"    : {"background":"#440066","border":"#8800cc"},
        }
        for key, color in colors.items():
            if key.lower() in dtype.lower():
                return color
        return {"background":"#2a2a3a","border":"#4a4a6a"}
