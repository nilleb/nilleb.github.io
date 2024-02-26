import glob
import re
from datetime import datetime

# Get all markdown files in the content folder
md_files = glob.glob("**/*.md", recursive=True)
print(f"{len(md_files)} files to process")
# Regular expression to match the date line
date_line_re = re.compile(r'^date: "(?P<date>\d{4}-\d{2}-\d{2})"$')

for md_file in md_files:
    if not md_file.startswith("content/"):
        continue
    print(md_file)
    with open(md_file, "r") as file:
        lines = file.readlines()

    # Iterate over lines and find the date line
    for i, line in enumerate(lines):
        match = date_line_re.match(line)
        if match:
            print(line)
            # Parse the date and replace it with the isoformat
            date = datetime.strptime(match.group("date"), "%Y-%m-%d").date()
            lines[i] = f"date: {date.isoformat()}\n"

    # Write the modified lines back to the file
    with open(md_file, "w") as file:
        file.writelines(lines)
