import json
import os
import re
from datetime import datetime

# Read header and footer from what-is-dns.html
html_path = r'c:\xampp\htdocs\index\tutorials\networking\what-is-dns.html'
with open(html_path, 'r', encoding='utf-8') as f:
    dns_html = f.read()

header_match = re.search(r'(<!-- Header -->.*?</header>)', dns_html, re.DOTALL)
header = header_match.group(1) if header_match else ''

footer_match = re.search(r'(<!-- Footer -->.*?</footer>)', dns_html, re.DOTALL)
footer = footer_match.group(1) if footer_match else ''

def generate_lesson(slug, title, category, level, readTime, html_content):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | {category} | MJ Tech Hub</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="../../css/themes.css">
    <link rel="stylesheet" href="../../css/main.css">
    <link rel="stylesheet" href="../../css/responsive.css">
    <script src="../../js/theme.js"></script>
    <script src="../../js/main.js" defer></script>
</head>
<body>
    {header}
    <main class="lesson-container py-4">
        <!-- Breadcrumb -->
        <div style="margin-bottom: 1rem; font-size: 0.85rem; color: var(--text-muted);">
            <a href="../../index.html" style="color: var(--text-secondary);">Home</a> &gt; 
            <a href="../../topics.html" style="color: var(--text-secondary);">Topics</a> &gt; 
            <a href="../../{category.lower()}.html" style="color: var(--text-secondary);">{category}</a> &gt; 
            <span style="color: var(--brand-primary);">{title}</span>
        </div>
        
        <span style="font-size: 0.8rem; background: var(--bg-tertiary); color: var(--brand-primary); padding: 4px 10px; border-radius: 4px; font-weight: 600; text-transform: uppercase;">{category}</span>
        <h1 style="font-size: 2.5rem; margin: 1rem 0; color: var(--text-primary);">{title}</h1>
        
        <div style="display: flex; gap: 1rem; margin-bottom: 2rem; font-size: 0.85rem; color: var(--text-muted);">
            <span><i class="fas fa-signal" style="color: var(--success);"></i> {level}</span>
            <span><i class="fas fa-clock"></i> {readTime}</span>
        </div>
        
        <div class="content lesson-content" style="font-size: 1.05rem; line-height: 1.7; color: var(--text-secondary);">
{html_content}
        </div>
        
        <!-- Navigation -->
        <div style="display: flex; justify-content: space-between; border-top: 1px solid var(--border-color); padding-top: 1.5rem; margin-top: 3rem;">
            <span></span>
            <span></span>
        </div>
    </main>
    {footer}
</body>
</html>"""

tutorials = [
    {
        "id": "what-is-a-mac-address",
        "title": "What Is a MAC Address?",
        "description": "Learn about the 48-bit physical address used in Layer 2 networks.",
        "category": "Networking",
        "level": "Beginner",
        "readTime": "6 min read",
        "keywords": "mac, address, physical, layer 2, hardware, unicast",
        "html": """<p>A <strong>Media Access Control (MAC) address</strong> is a unique identifier assigned to a network interface controller (NIC) for communications at the data link layer (Layer 2) of a network segment.</p>
<h2>Format</h2>
<p>MAC addresses are typically 48-bit (6-byte) numbers represented as six groups of two hexadecimal digits, separated by hyphens, colons, or without a separator.</p>
<pre><code>Example: 00:1A:2B:3C:4D:5E</code></pre>
<h2>How It Works</h2>
<p>Unlike IP addresses which are used to route traffic across the Internet (Layer 3), MAC addresses are primarily used to send data within the local network (LAN). When data reaches your local network, the switch uses MAC addresses to forward frames to the correct device.</p>
<h3>Unicast vs Multicast</h3>
<p>The first octet of a MAC address determines whether it is a unicast (single destination) or multicast (group) address. The exact organizational unique identifier (OUI) is defined by the first three bytes, mapping to the hardware manufacturer.</p>
<h3>Practical Command</h3>
<p>In Windows, you can view your physical MAC address using:</p>
<pre><code>ipconfig /all</code></pre>
<p>In Linux, you can use:</p>
<pre><code>ip link</code></pre>"""
    },
    {
        "id": "what-is-arp",
        "title": "What Is ARP?",
        "description": "Understand how the Address Resolution Protocol maps IP addresses to MAC addresses.",
        "category": "Networking",
        "level": "Intermediate",
        "readTime": "7 min read",
        "keywords": "arp, address resolution, layer 2, layer 3, mapping",
        "html": """<p>The <strong>Address Resolution Protocol (ARP)</strong> maps a known IPv4 address to an unknown Layer 2 MAC address on the local network.</p>
<h2>The ARP Flow</h2>
<p>When a host wants to send an IP packet to a destination on the same subnet, it must encapsulate it in a Layer 2 frame addressed to the destination's MAC address.</p>
<ol>
<li><strong>Host needs destination MAC:</strong> It checks its local ARP cache.</li>
<li><strong>ARP Request:</strong> If missing, it broadcasts an ARP Request ("Who has IP 192.168.1.5? Tell 192.168.1.10").</li>
<li><strong>ARP Reply:</strong> The device with that IP sends a unicast ARP Reply containing its MAC address.</li>
<li><strong>ARP Cache:</strong> The requesting host stores this mapping in its ARP cache for future use.</li>
</ol>
<h3>Note on IPv6</h3>
<p>ARP is strictly for IPv4. IPv6 uses the <em>Neighbor Discovery Protocol (NDP)</em> over ICMPv6 to accomplish the same goal.</p>
<h3>Practical Command</h3>
<p>To view your system's current ARP cache in Windows or Linux, run:</p>
<pre><code>arp -a</code></pre>"""
    },
    {
        "id": "what-is-a-subnet-mask",
        "title": "What Is a Subnet Mask?",
        "description": "Learn how subnet masks divide IP addresses into network and host portions.",
        "category": "Networking",
        "level": "Beginner",
        "readTime": "6 min read",
        "keywords": "subnet mask, network, host, ip, cidr",
        "html": """<p>A <strong>Subnet Mask</strong> is a 32-bit number that accompanies an IPv4 address. It separates the IP address into two distinct portions: the <em>Network portion</em> and the <em>Host portion</em>.</p>
<h2>Why is it necessary?</h2>
<p>Computers need a way to determine if a destination IP address is on their local network (meaning they can talk to it directly) or on a remote network (meaning they must send traffic to the Default Gateway). The subnet mask provides this boundary.</p>
<h2>Examples</h2>
<p>Consider the IP address <code>192.168.1.50</code> with a subnet mask of <code>255.255.255.0</code>.</p>
<ul>
<li>The <strong>255</strong> sections mean "Network".</li>
<li>The <strong>0</strong> section means "Host".</li>
</ul>
<p>Therefore, the network is <code>192.168.1.0</code>, and this specific host is number <code>50</code>.</p>
<h3>CIDR Notation</h3>
<p>Subnet masks are often written in <strong>CIDR (Classless Inter-Domain Routing)</strong> notation, representing the number of "1" bits in the mask. For example, <code>255.255.255.0</code> is commonly written as <strong>/24</strong>.</p>
<h3>Practical Command</h3>
<p>You can see your subnet mask in Windows by running:</p>
<pre><code>ipconfig</code></pre>"""
    },
    {
        "id": "subnetting-basics",
        "title": "Subnetting Basics",
        "description": "Learn how to divide a single network into multiple smaller subnets.",
        "category": "Networking",
        "level": "Intermediate",
        "readTime": "10 min read",
        "keywords": "subnetting, cidr, vlsm, broadcast, network address",
        "html": """<p><strong>Subnetting</strong> is the process of taking a single large network and dividing it into multiple smaller, more efficient networks (subnets).</p>
<h2>Why Subnet?</h2>
<ul>
<li><strong>Security:</strong> Isolate sensitive devices (e.g., placing servers in a different subnet than guest Wi-Fi).</li>
<li><strong>Performance:</strong> Reduce the size of broadcast domains, preventing excessive broadcast traffic from slowing down the network.</li>
<li><strong>Organization:</strong> Group devices by department or physical location.</li>
</ul>
<h2>Subnetting Example using CIDR</h2>
<p>Consider the common network: <code>192.168.1.0/24</code>. This provides 256 total IP addresses.</p>
<p>If we borrow one bit from the host portion, we split the network into two smaller <strong>/25</strong> subnets, each with 128 addresses.</p>
<h3>Subnet 1: 192.168.1.0/25</h3>
<ul>
<li><strong>Network Address:</strong> 192.168.1.0</li>
<li><strong>Usable Hosts:</strong> 192.168.1.1 to 192.168.1.126</li>
<li><strong>Broadcast Address:</strong> 192.168.1.127</li>
</ul>
<h3>Subnet 2: 192.168.1.128/25</h3>
<ul>
<li><strong>Network Address:</strong> 192.168.1.128</li>
<li><strong>Usable Hosts:</strong> 192.168.1.129 to 192.168.1.254</li>
<li><strong>Broadcast Address:</strong> 192.168.1.255</li>
</ul>
<p><em>Note:</em> In every subnet, the first address is reserved as the Network Address, and the last address is reserved as the Broadcast Address. They cannot be assigned to devices.</p>"""
    },
    {
        "id": "osi-model-explained",
        "title": "OSI Model Explained",
        "description": "Understand the 7 layers of the OSI model for network troubleshooting.",
        "category": "Networking",
        "level": "Intermediate",
        "readTime": "12 min read",
        "keywords": "osi, model, layers, troubleshooting, application, physical",
        "html": """<p>The <strong>Open Systems Interconnection (OSI) model</strong> is a conceptual framework used to understand how different network protocols and technologies interact. It divides network communication into seven distinct layers.</p>
<h2>The 7 Layers</h2>
<ol>
<li><strong>Physical (Layer 1):</strong> Deals with physical hardware—cables, switches, electrical signals, light, and radio frequencies.</li>
<li><strong>Data Link (Layer 2):</strong> Transfers data between adjacent network nodes. MAC addresses and basic switches operate here.</li>
<li><strong>Network (Layer 3):</strong> Handles routing data across multiple networks. IP addresses and routers operate here.</li>
<li><strong>Transport (Layer 4):</strong> Ensures reliable data delivery and handles flow control. TCP and UDP operate here.</li>
<li><strong>Session (Layer 5):</strong> Manages establishing, maintaining, and terminating sessions between applications.</li>
<li><strong>Presentation (Layer 6):</strong> Formats, encrypts, and compresses data so it can be understood by the application.</li>
<li><strong>Application (Layer 7):</strong> The interface used by network applications. HTTP, FTP, and DNS operate here.</li>
</ol>
<h2>Using the OSI Model for Troubleshooting</h2>
<p>IT professionals use the OSI model to isolate problems. A common strategy is to work "bottom-up":</p>
<ul>
<li><em>Layer 1 check:</em> Is the cable plugged in? Is there power?</li>
<li><em>Layer 2 check:</em> Is the switch port active? Is the MAC address learned?</li>
<li><em>Layer 3 check:</em> Can you ping the Default Gateway? (IP routing)</li>
<li><em>Layer 4 check:</em> Is a firewall blocking TCP port 443?</li>
<li><em>Layer 7 check:</em> Is the web server software actually running?</li>
</ul>
<p>By logically checking each layer, you can avoid wasting time fixing a web server (Layer 7) when the actual problem is a broken cable (Layer 1).</p>"""
    },
    {
        "id": "tcp-ip-model-explained",
        "title": "TCP/IP Model Explained",
        "description": "Learn the practical 4-layer network model that drives the Internet.",
        "category": "Networking",
        "level": "Intermediate",
        "readTime": "8 min read",
        "keywords": "tcp/ip, model, layers, internet, network access",
        "html": """<p>While the OSI model is heavily used for theoretical understanding and troubleshooting, the <strong>TCP/IP Model</strong> is a more practical framework that closely maps to how the modern Internet actually functions.</p>
<h2>The 4 Layers of TCP/IP</h2>
<ol>
<li><strong>Network Access (or Link) Layer:</strong> Roughly corresponds to OSI Layers 1 and 2. It handles the physical transmission of data across a single link (e.g., Ethernet, Wi-Fi).</li>
<li><strong>Internet Layer:</strong> Corresponds to OSI Layer 3. It uses IP addresses to route packets across multiple interconnected networks.</li>
<li><strong>Transport Layer:</strong> Corresponds to OSI Layer 4. It provides host-to-host communication services using protocols like TCP (reliable) and UDP (unreliable).</li>
<li><strong>Application Layer:</strong> Corresponds to OSI Layers 5, 6, and 7 combined. It represents the protocols that end-user applications use to interact, such as HTTP, DNS, and SSH.</li>
</ol>
<h2>TCP/IP vs OSI</h2>
<p>It is important to remember that these models are just frameworks. They do not dictate how software <em>must</em> be written, but rather help us categorize how it works. The TCP/IP model is simpler because it groups presentation, session, and application logic into one broad Application Layer, which accurately reflects how most modern software is developed.</p>"""
    },
    {
        "id": "common-network-ports",
        "title": "Common Network Ports",
        "description": "A quick reference guide for essential TCP and UDP ports.",
        "category": "Networking",
        "level": "Beginner",
        "readTime": "5 min read",
        "keywords": "ports, tcp, udp, list, reference, firewall",
        "html": """<p>A <strong>Network Port</strong> is a logical endpoint for communication, allowing a single IP address to host multiple different services simultaneously. Ports range from 1 to 65,535.</p>
<h2>Essential Ports Quick Reference</h2>
<p>As an IT professional, you should memorize these common ports, as you will frequently configure them in firewalls and routers.</p>
<table border="1" style="width:100%; border-collapse: collapse; margin-top: 1rem; border-color: var(--border-color);">
    <tr style="background: var(--bg-tertiary); text-align: left;">
        <th style="padding: 0.75rem;">Port</th>
        <th style="padding: 0.75rem;">Protocol</th>
        <th style="padding: 0.75rem;">Service</th>
    </tr>
    <tr><td style="padding: 0.75rem;">20 / 21</td><td style="padding: 0.75rem;">TCP</td><td style="padding: 0.75rem;">FTP (File Transfer Protocol)</td></tr>
    <tr><td style="padding: 0.75rem;">22</td><td style="padding: 0.75rem;">TCP</td><td style="padding: 0.75rem;">SSH (Secure Shell)</td></tr>
    <tr><td style="padding: 0.75rem;">23</td><td style="padding: 0.75rem;">TCP</td><td style="padding: 0.75rem;">Telnet (Unencrypted)</td></tr>
    <tr><td style="padding: 0.75rem;">25</td><td style="padding: 0.75rem;">TCP</td><td style="padding: 0.75rem;">SMTP (Email Routing)</td></tr>
    <tr><td style="padding: 0.75rem;">53</td><td style="padding: 0.75rem;">UDP / TCP</td><td style="padding: 0.75rem;">DNS (Domain Name System)</td></tr>
    <tr><td style="padding: 0.75rem;">67 / 68</td><td style="padding: 0.75rem;">UDP</td><td style="padding: 0.75rem;">DHCP (Dynamic Host Configuration)</td></tr>
    <tr><td style="padding: 0.75rem;">80</td><td style="padding: 0.75rem;">TCP</td><td style="padding: 0.75rem;">HTTP (Web Traffic)</td></tr>
    <tr><td style="padding: 0.75rem;">110</td><td style="padding: 0.75rem;">TCP</td><td style="padding: 0.75rem;">POP3 (Email Retrieval)</td></tr>
    <tr><td style="padding: 0.75rem;">123</td><td style="padding: 0.75rem;">UDP</td><td style="padding: 0.75rem;">NTP (Network Time Protocol)</td></tr>
    <tr><td style="padding: 0.75rem;">143</td><td style="padding: 0.75rem;">TCP</td><td style="padding: 0.75rem;">IMAP (Email Retrieval)</td></tr>
    <tr><td style="padding: 0.75rem;">389</td><td style="padding: 0.75rem;">TCP / UDP</td><td style="padding: 0.75rem;">LDAP (Directory Services)</td></tr>
    <tr><td style="padding: 0.75rem;">443</td><td style="padding: 0.75rem;">TCP</td><td style="padding: 0.75rem;">HTTPS (Secure Web Traffic)</td></tr>
    <tr><td style="padding: 0.75rem;">445</td><td style="padding: 0.75rem;">TCP</td><td style="padding: 0.75rem;">SMB (Windows File Sharing)</td></tr>
    <tr><td style="padding: 0.75rem;">3389</td><td style="padding: 0.75rem;">TCP / UDP</td><td style="padding: 0.75rem;">RDP (Remote Desktop Protocol)</td></tr>
</table>
<p><em>Note:</em> While many protocols strictly use TCP or UDP, some (like DNS) primarily use UDP for queries, but can fall back to TCP for large transfers (like zone transfers).</p>"""
    },
    {
        "id": "what-is-nat",
        "title": "What Is NAT?",
        "description": "Learn how Network Address Translation allows private IP addresses to access the Internet.",
        "category": "Networking",
        "level": "Intermediate",
        "readTime": "8 min read",
        "keywords": "nat, network address translation, pat, public ip, private ip",
        "html": """<p><strong>Network Address Translation (NAT)</strong> is a process used by routers to modify the source or destination IP addresses in packet headers while they are in transit.</p>
<h2>Why is NAT used?</h2>
<p>The primary reason NAT exists is IPv4 address exhaustion. There are simply not enough public IPv4 addresses for every device on Earth. NAT allows an entire private network to share a single public IP address to access the internet.</p>
<h2>Example Scenario</h2>
<p>Imagine your laptop on a home network:</p>
<ul>
<li><strong>Private Client IP:</strong> 192.168.1.10</li>
<li><strong>Router Public IP:</strong> 203.0.113.5 (from your ISP)</li>
</ul>
<p>When your laptop requests a web page, the packet leaves the laptop with a source IP of 192.168.1.10. When it hits the router, the router uses NAT to change the source IP to its own public IP (203.0.113.5) before sending it to the Internet. When the web server replies to 203.0.113.5, the router remembers the connection, translates the destination IP back to 192.168.1.10, and forwards it to your laptop.</p>
<h3>Port Address Translation (PAT)</h3>
<p>To keep track of multiple devices sharing one public IP simultaneously, the router translates both the IP address and the source port. This specific type of NAT is called <strong>PAT (Port Address Translation)</strong> or NAT Overloading, and it is what virtually all home and office routers use today.</p>"""
    },
    {
        "id": "router-vs-switch",
        "title": "Router vs Switch",
        "description": "Understand the critical differences between Layer 2 Switches and Layer 3 Routers.",
        "category": "Networking",
        "level": "Beginner",
        "readTime": "6 min read",
        "keywords": "router, switch, layer 2, layer 3, routing, switching",
        "html": """<p>Routers and Switches are the two most fundamental pieces of networking hardware, but they serve very different purposes.</p>
<h2>The Switch</h2>
<p>A <strong>Switch</strong> operates primarily at OSI Layer 2 (Data Link). Its job is to connect multiple devices together within the <em>same</em> network (LAN).</p>
<ul>
<li>Forwards traffic based on <strong>MAC addresses</strong>.</li>
<li>Keeps traffic localized; packets sent between two PCs on the same switch never leave the switch.</li>
<li>Does not understand IP addresses (in traditional Layer 2 deployments).</li>
</ul>
<h2>The Router</h2>
<p>A <strong>Router</strong> operates at OSI Layer 3 (Network). Its job is to connect <em>different</em> networks together.</p>
<ul>
<li>Forwards traffic based on <strong>IP addresses</strong>.</li>
<li>Determines the best path for data to travel across interconnected networks (like the Internet).</li>
<li>Blocks broadcast traffic, preventing local network noise from flooding other networks.</li>
</ul>
<h3>Real-World Summary</h3>
<p>You use a switch to build a network. You use a router to connect networks together.</p>
<p><em>Note: Modern enterprise networks often use "Layer 3 Switches," which are essentially switches that have routing capabilities built into them, allowing them to route traffic between different VLANs extremely fast.</em></p>"""
    },
    {
        "id": "hub-vs-switch",
        "title": "Hub vs Switch",
        "description": "Learn why modern networks use Switches instead of legacy Hubs.",
        "category": "Networking",
        "level": "Beginner",
        "readTime": "4 min read",
        "keywords": "hub, switch, collision domain, legacy, layer 1, layer 2",
        "html": """<p>Both Hubs and Switches are used to connect multiple devices in a local area network (LAN), but they handle data very differently. Today, Hubs are entirely obsolete.</p>
<h2>The Hub (Layer 1)</h2>
<p>A Hub is a "dumb" device. It operates at the Physical layer. When it receives a data signal on one port, it blindly copies and repeats that electrical signal out of <em>every other port</em>.</p>
<ul>
<li><strong>Security:</strong> Poor. Any device connected to the hub can "sniff" traffic meant for other devices.</li>
<li><strong>Performance:</strong> Poor. Because it broadcasts everything, devices frequently talk over each other, causing collisions. Only one device can transmit successfully at a time (Half-Duplex).</li>
</ul>
<h2>The Switch (Layer 2)</h2>
<p>A Switch is intelligent. It learns the MAC addresses of the devices connected to it by analyzing incoming traffic.</p>
<ul>
<li><strong>Targeted Delivery:</strong> When a switch receives data, it looks at the destination MAC address and forwards the data <em>only</em> out of the specific port where that device lives.</li>
<li><strong>Performance:</strong> Excellent. Multiple devices can send and receive data simultaneously at full speed without causing collisions (Full-Duplex).</li>
</ul>"""
    }
]

json_path = r'c:\xampp\htdocs\index\data\tutorials.json'
with open(json_path, 'r', encoding='utf-8') as f:
    tut_data = json.load(f)

existing_ids = {t['id'] for t in tut_data}
today = datetime.today().strftime('%Y-%m-%d')
script_dir = r'c:\xampp\htdocs\index\tutorials\networking'
if not os.path.exists(script_dir):
    os.makedirs(script_dir)

for t in tutorials:
    filename = f"{t['id']}.html"
    filepath = os.path.join(script_dir, filename)
    
    html_out = generate_lesson(t['id'], t['title'], t['category'], t['level'], t['readTime'], t['html'])
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_out)
        
    print(f"Generated {filename}")
    
    if t['id'] not in existing_ids:
        new_entry = {
            "id": t['id'],
            "title": t['title'],
            "description": t['description'],
            "category": t['category'],
            "level": t['level'],
            "readTime": t['readTime'],
            "keywords": t['keywords'],
            "url": f"tutorials/networking/{filename}",
            "publishedAt": today,
            "updatedAt": today
        }
        tut_data.append(new_entry)

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(tut_data, f, indent=4)
print("Updated tutorials.json")
