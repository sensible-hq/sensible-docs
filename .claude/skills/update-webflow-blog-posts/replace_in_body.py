"""
Apply a string replacement to a saved post body HTML file.

Usage:
    python3 replace_in_body.py <body-file> <old-string-file> <new-string-file> [--output <out-file>]

If --output is omitted, prints the result to stdout.
Exits non-zero if the old string is not found in the body.

Example:
    python3 replace_in_body.py /tmp/body.html /tmp/old.html /tmp/new.html --output /tmp/updated-body.html
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="Replace a string in a post body file.")
    parser.add_argument("body_file", help="HTML file containing the post body")
    parser.add_argument("old_file", help="File containing the exact string to replace")
    parser.add_argument("new_file", help="File containing the replacement string")
    parser.add_argument("--output", help="Output file path (default: stdout)")
    args = parser.parse_args()

    body = open(args.body_file).read()
    old = open(args.old_file).read()
    new = open(args.new_file).read()

    count = body.count(old)
    if count == 0:
        print("ERROR: old string not found in body", file=sys.stderr)
        sys.exit(1)
    if count > 1:
        print(f"WARNING: old string found {count} times — replacing all occurrences", file=sys.stderr)

    updated = body.replace(old, new)

    if args.output:
        with open(args.output, "w") as f:
            f.write(updated)
        print(f"Wrote {len(updated)} chars to {args.output} ({count} replacement(s))")
    else:
        print(updated)


if __name__ == "__main__":
    main()
