import os
from glob import glob
import sys

# Get the GitHub reference passed as an argument
tag = sys.argv[1]

# Store section data
news_items = {
    "Added": [],
    "Changed": [],
    "Deprecated": [],
    "Removed": [],
    "Fixed": [],
    "Security": [],
}

# Parse a single .rst file
def parse_each_header(file_path):
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            
            # Check if the line is a section header
            if line.startswith("**") and line.endswith(":**"):
                current_section = line.strip("**:").strip()
            
            # Only add if the line is not empty and not a section header
            elif current_section and line and not line.startswith("* <news item>"):
                news_items[current_section].append(line)
            

# Function to process all .rst files in the directory
def process_news_files(news_dir_path):
    rst_files = glob(os.path.join(news_dir_path, "*.rst"))
    
    for rst_file in rst_files:
        parse_each_header(rst_file)

def write_merged_file():
    CHANGELOG_PATH = "CHANGELOG.rst"
    CHANGELOG_HEADER = ".. current developments"

    # Insert news
    new_news_content = f"\n{tag}\n=====\n\n"
    for section_name in sorted(news_items.keys()):
        items = news_items[section_name]
        if items:
            # Add section name e.g. Added, Changed, etc.
            new_news_content += f"**{section_name}:**\n\n"
            for item in items:
                # Add each item in the section
                new_news_content += f"{item}\n"
            new_news_content += "\n"

    # Read the file
    with open(CHANGELOG_PATH, "r") as file:
        current_content = file.read()

    # Find the position to insert news after ".. current developments"
    insert_position = current_content.find(CHANGELOG_HEADER) + len(CHANGELOG_HEADER) + 1
    final_content = current_content[:insert_position] + new_news_content + current_content[insert_position:]

    # Write the updated content back to the file
    with open(CHANGELOG_PATH, "w") as file:
        file.write(final_content)

def cleanup_rst_files(news_dir_path):
    # List all files in the directory
    rst_files = os.listdir(news_dir_path)
    for file_name in rst_files:
        rst_file_path = os.path.join(news_dir_path, file_name)
        if file_name.endswith('.rst') and file_name != "TEMPLATE.rst":
            os.remove(rst_file_path)


if __name__ == "__main__":
    news_dir_path = "news"
    # Process each .rst file
    process_news_files(news_dir_path)  
    # Write new news under "".. current developments"
    write_merged_file()      
    # Remove .rst files except TEMPLATE.rst
    cleanup_rst_files(news_dir_path)
