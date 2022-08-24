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


def get_ids_from_slugs(collection):
    ids = {}
    r = requests.get(
        f"https://api.webflow.com/collections/{collection}/items", headers=headers
    )
    raw_json = r.json()

    for item in raw_json["items"]:
        ids[item["slug"]] = item["_id"]

    return ids


def create_learning_path(files):
    for md_file in files:
        metadata, html = parse_markdown(md_file)

        data["fields"]["name"] = metadata["title"]
        data["fields"]["slug"] = metadata["slug"]
        data["fields"]["document"] = html

        r = requests.post(
            f"https://api.webflow.com/collections/{collection_id}/items",
            headers=headers,
            json=data,
        )
        # print(r.request.url)
        # print(r.request.body)
        # print(r.request.headers)
        print(r.status_code)


def update_learning_path(files, slugs, force=False):
    for md_file in files:
        metadata, html = parse_markdown(md_file)

        if metadata["slug"] in slugs is False:
            if force is True:
                create_learning_path([md_file])
                continue
            else:
                print(
                    "WARNING: File to update doesn't exist in Webflow. To force a create use the --force option"
                )
                continue

        data["fields"]["name"] = metadata["title"]
        data["fields"]["slug"] = metadata["slug"]
        data["fields"]["document"] = html

        id = slugs[metadata["slug"]]
        r = requests.put(
            f"https://api.webflow.com/collections/{collection_id}/items/{id}",
            headers=headers,
            json=data,
        )
        # print(r.request.url)
        # print(r.request.body)
        # print(r.request.headers)
        print(r.status_code)


def delete_learning_path(files, slugs):
    for md_file in files:
        file_name = os.path.basename(md_file[:-3])
        if file_name in slugs is False:
            print(
                f"WARNING: {md_file} does not exist in Webflow and therefore can't be deleted"
            )
            continue

        id = slugs[file_name]

        r = requests.delete(
            f"https://api.webflow.com/collections/{collection_id}/items/{id}",
            headers=headers,
        )

        print(f"{md_file} DELETED with code {r.status_code}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Gretel Markdown to Webflow processor. Converts MD to HTML and uploads via the Webflow API"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-c", "--create", action="store_true", help="Publish a new document"
    )
    group.add_argument(
        "-u", "--update", action="store_true", help="Update an existing document"
    )
    group.add_argument(
        "-d", "--delete", action="store_true", help="Delete an existing document"
    )
    parser.add_argument(
        "-f", "--files", required=True, help="Comma separated list of files to process"
    )
    parser.add_argument(
        "-fo",
        "--force",
        action="store_true",
        help="Force create documents on update if they don't exist",
    )

    parser.add_argument(
        "-hh",
        "--headers",
        action="store_true",
        help="Include sample HTML body, styles, and headers",
    )
    args = parser.parse_args()

    files = [x for x in args.files.split(",") if x[-3:] == ".md"]

    slugs = get_ids_from_slugs(collection_id)

    if args.create is True:
        create_learning_path(files)
    elif args.update is True:
        update_learning_path(files, slugs, force=args.force)
    elif args.delete is True:
        delete_learning_path(files, slugs)
