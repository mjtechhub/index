import socket
import ssl
import http.client
from urllib.parse import urlparse

domains = ['themjtechhub.site', 'www.themjtechhub.site']

print("=== DNS RESOLUTION ===")
for d in domains:
    print(f"\nHost: {d}")
    try:
        addr_info = socket.getaddrinfo(d, 80, proto=socket.IPPROTO_TCP)
        unique_ips = set(item[4][0] for item in addr_info)
        for ip in sorted(unique_ips):
            print(f"  A/AAAA IP: {ip}")
    except Exception as e:
        print(f"  DNS resolution error: {e}")

print("\n=== HTTP / HTTPS NORMALIZATION & REDIRECTS ===")
test_urls = [
    'http://themjtechhub.site/',
    'https://themjtechhub.site/',
    'http://www.themjtechhub.site/',
    'https://www.themjtechhub.site/',
]

for u in test_urls:
    parsed = urlparse(u)
    scheme = parsed.scheme
    host = parsed.netloc
    path = parsed.path or '/'

    print(f"\nProbing: {u}")
    try:
        if scheme == 'https':
            conn = http.client.HTTPSConnection(host, timeout=10, context=ssl.create_default_context())
        else:
            conn = http.client.HTTPConnection(host, timeout=10)

        conn.request('GET', path, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        res = conn.getresponse()
        print(f"  Status: {res.status} {res.reason}")
        print(f"  Location header: {res.getheader('Location')}")
        print("  Key Response Headers:")
        for h in ['Server', 'Strict-Transport-Security', 'Content-Security-Policy', 'X-Content-Type-Options', 'Referrer-Policy', 'Permissions-Policy', 'Cache-Control', 'ETag', 'Last-Modified']:
            val = res.getheader(h)
            if val:
                print(f"    {h}: {val}")
            else:
                print(f"    {h}: [NOT PRESENT]")
        conn.close()
    except Exception as e:
        print(f"  Request error: {e}")
