"""
Two-step PDF upload to Webflow CDN.

Step 1: Call Webflow MCP data_assets_tool > create_asset to get presigned S3 envelope.
Step 2 (this script): POST file bytes to S3 via multipart form.

Usage:
    python3 upload_pdf_to_webflow.py <pdf-path> \
        --upload-url <s3-url> \
        --upload-details '<json-string>' \
        [--asset-id <id>] \
        [--hosted-url <url>]

The --upload-url and --upload-details come from the create_asset MCP response.
uploadDetails keys (camelCase) are mapped to the correct S3 form field names.

Prints to stdout:
    Upload status: 201 ✓
    ASSET_ID:   6a57...
    HOSTED_URL: https://cdn.prod.website-files.com/...
"""

import argparse
import hashlib
import json
import subprocess
import sys


FIELD_MAP = {
    "acl": "acl",
    "bucket": "bucket",
    "xAmzAlgorithm": "X-Amz-Algorithm",
    "xAmzCredential": "X-Amz-Credential",
    "xAmzDate": "X-Amz-Date",
    "key": "key",
    "policy": "policy",
    "xAmzSignature": "X-Amz-Signature",
    "successActionStatus": "success_action_status",
    "contentType": "Content-Type",
    "cacheControl": "Cache-Control",
}


def md5_of_file(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def upload_to_s3(pdf_path, upload_url, upload_details):
    form_fields = []
    for json_key, form_key in FIELD_MAP.items():
        if json_key in upload_details:
            form_fields += ["-F", f"{form_key}={upload_details[json_key]}"]
    form_fields += ["-F", f"file=@{pdf_path};type=application/pdf"]

    result = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
         "-X", "POST", upload_url] + form_fields,
        capture_output=True, text=True,
    )
    return result.stdout.strip(), result.stderr


def main():
    parser = argparse.ArgumentParser(description="Upload a PDF to Webflow CDN via S3.")
    parser.add_argument("pdf_path", help="Local path to the PDF file")
    parser.add_argument("--upload-url", required=True, help="S3 presigned URL from create_asset")
    parser.add_argument("--upload-details", required=True,
                        help="JSON string of uploadDetails from create_asset response")
    parser.add_argument("--asset-id", help="Asset ID for confirmation output")
    parser.add_argument("--hosted-url", help="Hosted URL for confirmation output")
    args = parser.parse_args()

    upload_details = json.loads(args.upload_details)
    print(f"MD5:  {md5_of_file(args.pdf_path)}")
    print(f"File: {args.pdf_path}")
    print("Uploading to S3...")

    status, stderr = upload_to_s3(args.pdf_path, args.upload_url, upload_details)

    if status == "201":
        print(f"Upload status: {status} ✓")
        if args.asset_id:
            print(f"ASSET_ID:   {args.asset_id}")
        if args.hosted_url:
            print(f"HOSTED_URL: {args.hosted_url}")
    else:
        print(f"Upload status: {status} ✗", file=sys.stderr)
        if stderr:
            print(f"stderr: {stderr}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
