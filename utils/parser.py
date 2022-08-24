import markdown
import argparse
import sys
import requests
import frontmatter

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
    metadata = ""
    with open(md_file, "r") as f:
        text = frontmatter.loads(f.read())
        if len(text.keys()) > 0:
            metadata = text.metadata
        html = markdown.markdown(text.content, extensions=extensions)

    if headers is True:
        html = f"{HTML_HEADERS}{html}{HTML_FOOTERS}"

    return metadata, html


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Markdown to HTML parser with Gretel custom Markdown"
    )
    parser.add_argument(
        "-f", "--file", required=True, help="Markdown file to convert to HTML string"
    )
    parser.add_argument(
        "-hh",
        "--headers",
        action="store_true",
        help="Include sample HTML body, styles, and headers",
    )
    parser.add_argument(
        "-md", "--metadata", action="store_true", help="Include metadata in output"
    )

    args = parser.parse_args()

    html_output = parse_markdown(args.file, headers=args.headers)

    if args.metadata is True:
        print(html_output[0])
    print(html_output[1])
