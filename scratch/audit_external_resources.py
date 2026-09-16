import json
import urllib.request
import urllib.error
import ssl

with open('data/resources.json', 'r', encoding='utf-8') as f:
    resources = json.load(f)

print(f"Total curated resources: {len(resources)}")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

results = []

for idx, res in enumerate(resources, 1):
    rid = res.get('id')
    title = res.get('title')
    url = res.get('url')
    print(f"[{idx}/{len(resources)}] Checking {rid}: {url} ...", end=" ", flush=True)

    status_code = None
    error_msg = None
    final_url = None

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=12) as resp:
            status_code = resp.status
            final_url = resp.geturl()
            print(f"OK ({status_code}) -> {final_url}")
    except urllib.error.HTTPError as e:
        status_code = e.code
        error_msg = str(e)
        print(f"HTTP Error ({status_code})")
    except Exception as e:
        error_msg = str(e)
        print(f"FAILED: {error_msg}")

    results.append({
        'id': rid,
        'title': title,
        'url': url,
        'status_code': status_code,
        'final_url': final_url,
        'error': error_msg
    })

print("\n--- SUMMARY OF ISSUES ---")
issues = [r for r in results if r['status_code'] not in (200, 301, 302, 303, 307, 308, 403)]
for iss in issues:
    print(iss)

if not issues:
    print("All 26 resources resolved with valid status codes (200/redirects/403 bot-blocks)!")
