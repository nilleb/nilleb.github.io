import glob
import logging
import os
from datetime import datetime

import markdown
import yaml
from slugify import slugify


def split_markdown_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    parts_lines, current_part_lines = [], []
    for line in content.split("\n"):
        if line.startswith("---"):
            current_parts_lines = []
            parts_lines.append(current_parts_lines)
        else:
            current_parts_lines.append(line)

    parts = ["\n".join(part_lines) for part_lines in parts_lines]

    try:
        yaml_section, markdown_text = parts
    except ValueError:
        logging.exception(f"while parsing {file_path}")
        raise

    yaml_section = yaml.safe_load(yaml_section)
    if not yaml_section:
        raise ValueError(f"No YAML section found in {file_path}, {parts}")

    return yaml_section, markdown_text


class MarkdownFile:
    def __init__(self, filepath):
        yaml_section, markdown_text = split_markdown_file(filepath)
        self.__dict__.update(yaml_section)
        self.text = markdown_text
        self.html = markdown.markdown(markdown_text)
        self.parsed_date = (
            datetime.strptime(self.date, "%Y-%m-%d")
            if isinstance(self.date, str)
            else self.date
        )
        self.title = getattr(self, "title", "")
        if not self.title:
            self.title = self.text[:100]
        self.slug = slugify(self.title)


md_files = glob.glob("content/**/*.md", recursive=True)
print(f"{len(md_files)} files to process")

data = {}
for md_file in md_files:
    mf = MarkdownFile(md_file)
    data[mf.parsed_date] = mf


def sort_data(data):
    return {k: data[k] for k in sorted(data.keys(), reverse=True)}


print(sort_data(data).keys())
print(len(data))


def gen_anchor(mf: MarkdownFile):
    dt = datetime.strftime(mf.parsed_date, "%Y-%m-%d")
    return f"<li>{dt}: <a href='{dt}-{mf.slug}.html'>{mf.title}</a></li>"


index_lines = []
os.makedirs("output", exist_ok=True)
for dt, mf in sort_data(data).items():
    index_lines.append(gen_anchor(mf))
    with open(f"output/{dt.isoformat()}-{mf.slug}.html", "w") as file:
        file.write(
            f"""
        <html>
        <head>
            <title>{mf.title}</title>
        </head>
        <body>
            <h1>{mf.title}</h1>
            <p>{dt}</p>
            {mf.html}
        </body>
        </html>
        """
        )

with open("output/index.html", "w") as file:
    file.write(
        f"""
    <html>
    <head>
        <title>Amazed by the noise</title>
    </head>
    <body>
        <h1>Amazed by the noise</h1>
        <p>Blog posts from Ivo Bellin Salarin, aka `nilleb`</p>
        <ul>
            {''.join(index_lines)}
        </ul>
    </body>
    </html>
    """
    )
