import re
import sys

tag = sys.argv[1]
changelog_path = "CHANGELOG.rst"
output_file = "CHANGELOG.txt"  # Output file

# Prepare to collect the relevant section of the changelog
collect = False
collected_lines = []

# Regular expression to match version patterns like 0.1.2
version_pattern = re.compile(r'^\d+\.\d+\.\d+')

# Open the file and read line by line
with open(changelog_path, 'r') as file:
    for line in file:
        # Check if the line starts with the tag
        if line.strip().startswith(tag):
            collect = True
            collected_lines.append(line.strip())  # Add the starting line
            continue

        # Check if a line matches another version pattern and we're already collecting
        if collect and version_pattern.match(line.strip()):
            break

        if collect:
            collected_lines.append(line.rstrip())  # Use rstrip to maintain empty lines as truly empty

if __name__ == "__main__":
    # Join collected lines with newline characters to keep the formatting
    output = "\n".join(collected_lines)

    # Write the collected lines to CHANGELOG.md
    with open(output_file, 'w') as out_file:
        out_file.write(output)
