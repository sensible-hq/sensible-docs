import json
import urllib.request

data = json.load(open("/home/franc/GitHub/sensible-docs/.claude/webflow-update/find-replace-key-config-library.json"))

cdn_links = set()
for entry in data:
    for link in entry.get("new_links", []):
        url = link.get("url", "")
        if "cdn.prod.website-files.com" in url:
            cdn_links.add(url)

for url in sorted(cdn_links):
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=10) as r:
            print(f"  {r.status}  {url}")
    except Exception as e:
        print(f"  ERR  {url}  ({e})")
