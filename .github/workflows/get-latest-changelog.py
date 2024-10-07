import re
import sys

def get_tag_news_items(tag, filepath):
    """Collet news items after the specified tag until the next version is found."""
    collect = False
    collected_lines = []
    # Regex to match version numbers
    version_pattern = re.compile(r'^\d+\.\d+\.\d+') 
    
    with open(filepath, 'r') as file:
        for line in file:
            if line.strip().startswith(tag):
                collect = True
                continue
            elif collect and version_pattern.match(line.strip()):
                break
            elif collect:
                collected_lines.append(line.rstrip())
    
    return collected_lines

def remove_two_lines(lines):
    """Remove two lines after the tag line."""
    if lines:
        # Remove the first line containing "===="
        if "====" in lines[0]:
            lines.pop(0)
        # Remove the second empty line
        if lines[1] == "":
            lines.pop(1)
    return lines

def save_to_txt_file(lines, filename):
    """Save collected lines to a .txt file used for GH release notes."""
    output = "\n".join(lines)
    with open(filename, 'w') as file:
        file.write(output)
    return output


if __name__ == "__main__":
    if len(sys.argv) < 2:
        assert False, "No tag has been provided. Please provide a tag by running python get-latest-changelog.py <tag>"
    
    tag = sys.argv[1]
    CHANGELOG_PATH = "CHANGELOG.rst"
    LATEST_CHANGELOG_PATH = "CHANGELOG.txt"
    
    collected_lines = get_tag_news_items(tag, CHANGELOG_PATH)
    cleaned_lines = remove_two_lines(collected_lines)
    latest_changelog_output = save_to_txt_file(cleaned_lines, LATEST_CHANGELOG_PATH)
    print(f"CHANGELOG for {tag}:\n{latest_changelog_output}")
