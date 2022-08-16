import markdown
import argparse
import sys

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
    parser.add_argument("-f", "--file", help="Markdown file to convert to HTML string")
    parser.add_argument("-fs", "--file-list", help="List of Markdown files to convert to HTML strings")
    parser.add_argument(
        "-hh",
        "--headers",
        action="store_true",
        help="Include HTML body, styles, and headers",
    )
    parser.add_argument("-o", "--output", help="File location to store HTML output")

    args = parser.parse_args()
    if args.file is None and args.file_list is None:
        print("Markdown file(s) to convert required.")
        sys.exit(1)

    
    html_output = parse_markdown(args.file, headers=args.headers)

    if args.output is not None:
        with open(args.output, "w") as fh:
            fh.write(html_output)
    else:
        print(html_output)
