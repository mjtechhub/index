import json
import os

path = r'c:\xampp\htdocs\index\data\topics.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

net_sec = next(c for c in data['categories'] if c['id'] == 'networking')['sections']

def add_to_section(section_name, tut_id, name, level):
    # Find section
    sec = next((s for s in net_sec if s['name'] == section_name), None)
    if not sec:
        sec = {"name": section_name, "subtopics": []}
        net_sec.append(sec)
    
    # Check if exists
    if not any(t['id'] == tut_id for t in sec['subtopics']):
        sec['subtopics'].append({
            "id": tut_id,
            "name": name,
            "level": level,
            "url": f"tutorials/networking/{tut_id}.html"
        })

add_to_section("Networking Fundamentals", "osi-model-explained", "OSI Model Explained", "Intermediate")
add_to_section("Networking Fundamentals", "tcp-ip-model-explained", "TCP/IP Model Explained", "Intermediate")
add_to_section("Networking Fundamentals", "hub-vs-switch", "Hub vs Switch", "Beginner")
add_to_section("Networking Fundamentals", "router-vs-switch", "Router vs Switch", "Beginner")
add_to_section("Networking Fundamentals", "what-is-a-mac-address", "What Is a MAC Address?", "Beginner")

add_to_section("IP Addressing", "what-is-a-subnet-mask", "What Is a Subnet Mask?", "Beginner")
add_to_section("IP Addressing", "subnetting-basics", "Subnetting Basics", "Intermediate")

add_to_section("Routing", "what-is-arp", "What Is ARP?", "Intermediate")
add_to_section("Routing", "what-is-nat", "What Is NAT?", "Intermediate")

# We will create a Ports & Protocols section
add_to_section("Ports & Protocols", "common-network-ports", "Common Network Ports", "Beginner")
add_to_section("Ports & Protocols", "tcp-vs-udp", "TCP vs UDP", "Intermediate")

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

print("Updated topics.json")
