import requests
import os
import sys
import argparse
from parser import parse_markdown

bearer_token = os.getenv("BEARER_TOKEN", None)
collection_id = os.getenv("COLLECTION_ID", None)

if bearer_token in (None, "") or collection_id in (None, ""):
    print("Bearer Token and Collection ID must be set via env vars")
    sys.exit(1)

headers = {
    "Accept-Version": "1.0.0",
    "Authorization": f"Bearer {bearer_token}",
    "content-type": "application/json",
}

data = {
    "fields": {
        "name": "",
        "slug": "",
        "_draft": False,
        "_archived": False,
        "document": "",
    }
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Gretel Markdown to Webflow processor. Converts MD to HTML and uploads via the Webflow API"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-c", "--create", action="store_true", help="Publish a new document"
    )
    group.add_argument(
        "-u", "--update", action="store_true", help="Update an existing document"
    )
    parser.add_argument(
        "-f", "--files", required=True, help="Comma separated list of files to process"
    )

    parser.add_argument(
        "-hh",
        "--headers",
        action="store_true",
        help="Include sample HTML body, styles, and headers",
    )
    args = parser.parse_args()

    for md_file in [x for x in args.files.split(",") if x[-3:] == ".md"]:
        metadata, html = parse_markdown(md_file)

        data["name"] = metadata["title"]
        data["slug"] = metadata["slug"]
        data["document"] = html

        r = requests.post(
            f"https://api.webflow.com/collections/{collection_id}/items",
            headers=headers,
            json=data,
        )
        # print(r.request.url)
        # print(r.request.body)
        # print(r.request.headers)
        print(r.status_code)
        print(r.text)
