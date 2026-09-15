import json
import urllib.request
import ssl
from pathlib import Path

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

with open('data/resources.json', 'r', encoding='utf-8') as f:
    resources = json.load(f)

print(f"Total resources: {len(resources)}")
failures = 0
for r in resources:
    url = r['url']
    if url.startswith('http'):
        assert url.startswith('https://'), f"External URL must use HTTPS: {url}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
                print(f"[PASS HTTP {resp.status}] {r['id']} ({r['provider']}): {url}")
        except urllib.error.HTTPError as e:
            if e.code in [403, 405]:
                print(f"[PASS HTTP {e.code} BLOCKED HEAD/GET] {r['id']}: {url}")
            else:
                print(f"[FAIL HTTP {e.code}] {r['id']}: {url}")
                failures += 1
        except Exception as e:
            print(f"[FAIL ERROR] {r['id']}: {url} -> {e}")
            failures += 1
    else:
        # Internal link check
        if '#' in url:
            page, anchor = url.split('#', 1)
            target_path = Path(page) if page else Path('resources.html')
            assert target_path.exists(), f"Internal file {target_path} does not exist for {url}"
            content = target_path.read_text(encoding='utf-8')
            assert f'id="{anchor}"' in content or f"id='{anchor}'" in content, f"Anchor {anchor} not found in {target_path}"
            print(f"[PASS INTERNAL ANCHOR] {r['id']}: {url}")
        else:
            target_path = Path(url)
            assert target_path.exists(), f"Internal file {target_path} does not exist for {url}"
            print(f"[PASS INTERNAL PAGE] {r['id']}: {url}")

print(f"\nResource Validation Complete. Total Failures: {failures}")
