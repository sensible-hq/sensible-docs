#!/usr/bin/env python3
"""
Check that all URLs in llms.txt return non-error HTTP status codes.

Uses HEAD requests with a thread pool so the full check completes in a few
seconds rather than making ~150 sequential requests.
"""

import re
import sys
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def find_repo_root() -> Path:
    # scripts/llms_txt/check_links.py → scripts/llms_txt/ → scripts/ → repo root
    candidate = Path(__file__).resolve().parent.parent.parent
    if (candidate / "llms.txt").exists():
        return candidate
    cwd = Path.cwd()
    if (cwd / "llms.txt").exists():
        return cwd
    raise SystemExit("Could not find repo root (expected llms.txt)")


def extract_urls(content: str) -> list[str]:
    return re.findall(r"https?://[^\s)>\"']+", content)


def check_url(url: str) -> tuple[str, int | None, str | None]:
    try:
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", "sensible-llms-txt-checker/1.0")
        with urllib.request.urlopen(req, timeout=10) as resp:
            return url, resp.status, None
    except urllib.error.HTTPError as e:
        return url, e.code, None
    except Exception as e:
        return url, None, str(e)


def main() -> int:
    repo_root = find_repo_root()
    content = (repo_root / "llms.txt").read_text(encoding="utf-8")
    urls = extract_urls(content)

    if not urls:
        print("No URLs found in llms.txt")
        return 0

    print(f"Checking {len(urls)} URLs...")

    failures = []
    # Low concurrency to avoid triggering rate limits on the docs CDN
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(check_url, url): url for url in urls}
        for future in as_completed(futures):
            url, status, error = future.result()
            if error:
                print(f"  ERROR  {url}: {error}")
                failures.append((url, f"error: {error}"))
            elif status == 429:
                # Rate limited — can't confirm existence, skip rather than fail
                print(f"  429    {url} (rate limited, skipped)")
            elif status >= 400:
                print(f"  {status}    {url}")
                failures.append((url, str(status)))
            else:
                print(f"  {status}    {url}")

    print()
    if failures:
        print(f"Found {len(failures)} broken URL(s):")
        for url, reason in failures:
            print(f"  {reason}  {url}")
        return 1

    print(f"All {len(urls)} URLs OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
