"""
Grep blog post bodies from a saved Webflow CMS API response.

Usage:
    python3 grep_posts.py <api-response.txt> <search-term> [--field <field-slug>]

Arguments:
    api-response.txt   Path to saved list_collection_items JSON response
    search-term        String or regex pattern to search for
    --field            CMS field to search (default: post-body)
    --regex            Treat search-term as a regex (default: substring match)
    --context N        Print N characters of surrounding context per match (default: 200)
    --links-only       Extract and deduplicate all URLs containing the search term

The API response file has structure:
    [{"type": "text", "text": "<JSON string of list_collection_items result>"}]

Examples:
    python3 grep_posts.py posts.txt "sensible-configuration-library"
    python3 grep_posts.py posts.txt "sensible-configuration-library" --links-only
    python3 grep_posts.py posts.txt "raw.githubusercontent.com" --context 300
    python3 grep_posts.py posts.txt "download" --field post-summary
    python3 grep_posts.py posts.txt "\\.pdf\"" --regex
"""

import argparse
import json
import re
import sys


def load_items(path):
    with open(path) as f:
        outer = json.load(f)
    # Handle both raw list_collection_items result and the tool-result envelope
    if isinstance(outer, list) and outer and "text" in outer[0]:
        inner = json.loads(outer[0]["text"])
        return inner["result"]["items"]
    elif isinstance(outer, dict) and "items" in outer:
        return outer["items"]
    elif isinstance(outer, dict) and "result" in outer:
        return outer["result"]["items"]
    raise ValueError(f"Unrecognized response format in {path}")


def extract_links(text, pattern):
    """Return deduplicated URLs in text that contain the pattern."""
    url_re = re.compile(r'https?://[^\s"\'<>]+', re.IGNORECASE)
    return sorted(set(u for u in url_re.findall(text) if pattern.search(u)))


def print_context(text, pattern, context_chars):
    for m in pattern.finditer(text):
        start = max(0, m.start() - context_chars)
        end = min(len(text), m.end() + context_chars)
        snippet = text[start:end]
        if start > 0:
            snippet = "…" + snippet
        if end < len(text):
            snippet = snippet + "…"
        print(f"  [{snippet}]")


def main():
    parser = argparse.ArgumentParser(description="Grep Webflow blog post bodies.")
    parser.add_argument("response_file", help="Path to saved API response JSON")
    parser.add_argument("search_term", help="Substring or regex to search for")
    parser.add_argument("--field", default="post-body", help="Field slug to search")
    parser.add_argument("--regex", action="store_true", help="Treat search-term as regex")
    parser.add_argument("--context", type=int, default=200, metavar="N",
                        help="Characters of surrounding context to print (default: 200)")
    parser.add_argument("--links-only", action="store_true",
                        help="Extract and print only URLs containing the search term")
    args = parser.parse_args()

    items = load_items(args.response_file)

    flags = re.IGNORECASE
    pattern_str = args.search_term if args.regex else re.escape(args.search_term)
    pattern = re.compile(pattern_str, flags)

    matches = []
    for item in items:
        text = item.get("fieldData", {}).get(args.field, "")
        if not pattern.search(text):
            continue
        matches.append((item, text))

    print(f"Matches in --field '{args.field}': {len(matches)} / {len(items)} posts\n")

    for i, (item, text) in enumerate(matches, 1):
        fd = item.get("fieldData", {})
        print(f"[{i}/{len(matches)}] {fd.get('name', '(no name)')}")
        print(f"  ID:   {item['id']}")
        print(f"  Slug: {fd.get('slug', '')}")

        if args.links_only:
            links = extract_links(text, pattern)
            print(f"  Matching URLs ({len(links)}):")
            for l in links:
                print(f"    {l}")
        else:
            print_context(text, pattern, args.context)
        print()


if __name__ == "__main__":
    main()
