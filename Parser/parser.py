import markdown
import argparse
import sys
import requests

extensions = [
    "meta",
    "pymdownx.arithmatex",
    "pymdownx.caret",
    "pymdownx.details",
    "pymdownx.emoji",
    "pymdownx.extra",
    "pymdownx.highlight",
    "pymdownx.inlinehilite",
    "pymdownx.keys",
    "pymdownx.mark",
    "pymdownx.smartsymbols",
    "pymdownx.superfences",
    "pymdownx.tabbed",
]

HTML_HEADERS = """
<html>
<head>
<link rel="stylesheet" href="style.css">
    </head>
<body>
"""

HTML_FOOTERS = """
</body>
</html>
"""


def parse_markdown(md_file, headers=False):
    with open("sample.md", "r") as f:
        text = f.read()
        html = markdown.markdown(text, extensions=extensions)

    if headers is True:
        html = f"{HTML_HEADERS}{html}{HTML_FOOTERS}"

    return html


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Markdown to HTML parser with Gretel custom Markdown"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--file", help="Markdown file to convert to HTML string")
    group.add_argument(
        "-fl", "--file-list", help="List of Markdown files to convert to HTML strings"
    )
    parser.add_argument(
        "-hh",
        "--headers",
        action="store_true",
        help="Include HTML body, styles, and headers",
    )
    parser.add_argument(
        "-o", "--output", action="store_true", help="Output to .html files"
    )

    args = parser.parse_args()
    if args.file is None and args.file_list is None:
        print("Markdown file(s) to convert required.")
        sys.exit(1)

    if args.file is not None:
        html_output = parse_markdown(args.file, headers=args.headers)

        if args.output is True:
            with open(f"{args.file}.html", "w") as fh:
                fh.write(html_output)
        else:
            print(html_output)
    else:
        markdown_files = []
        input_files = args.file_list.split(",")
        for fyle in input_files:
            if fyle[-3:] == ".md" and fyle != "README.md":
                markdown_files.append(fyle)

        for f in markdown_files:
            html_output = parse_markdown(f, headers=args.headers)

            if args.output is True:
                with open(f"{f}.html", "w") as fh:
                    fh.write(html_output)
            else:
                print(html_output)

        r = requests.get('https://pokeapi.co/api/v2/pokemon/ditto')
        print(r.status_code)

            
