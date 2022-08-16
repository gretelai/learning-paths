# Gretel Learning Paths


## Python Parsing Tool
Python parser for Gretel.ai formatted Markdown files.

Currently we are using base markdown with a few Pymdownx extensions

* [John Gruber's Markdown](https://daringfireball.net/projects/markdown/)
* [PyMdown Extensions](https://facelessuser.github.io/pymdown-extensions/)

For more details on what is supported, check out our [sample page](sample.md)

### Installation
1. `python -m venv venv`
1. `source venv/bin/activate`
1. `pip install -r requirements.txt`

If you are actively developing and want black, pylint, etc. install dev tools.
1. `pip install -r dev-requirements.txt

### Usage
`parser.py` is a command line script that takes a Markdown file as input and
exports HTML, either raw or to a file. You also have the option of including the
basic `<html>` tags and CSS files.

#### Example Usage
Convert a Markdown file to html
```
python parser.py -f my_markdown.md
```

Convert a Markdown file to html and include HTML and CSS (for local viewing)
```
python parser.py -f my_markdown.md -hh
```

Convert a Markdown file to html and output to HTML file
```
python parser.py -f my_markdown.md -o output.html
```

Convert a Markdown file to html, include headers, and output to HTML file
```
python parser.py -f my_markdown.md -hh -o output.html
```

#### Help Text
```bash
python parser.py -h
usage: parser.py [-h] [-f FILE] [-hh] [-o OUTPUT]

Markdown to HTML parser with Gretel custom Markdown

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Markdown file to convert to HTML string
  -hh, --headers        Include HTML body, styles, and headers
  -o OUTPUT, --output OUTPUT
                        File location to store HTML output
```

## Licensing
This repository has two licenses, depending on the content type. 

All written educational content, images, etc. formatted to be a Learning Path is 
licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/) license.

All source code, tooling, etc. found within the Parser directory is licensed under the
[Apache 2.0 License](Parser/LICENSE)