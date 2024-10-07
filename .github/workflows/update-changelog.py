import os
from glob import glob
import sys

# Get the GitHub reference passed as an argument
tag = sys.argv[1]

# Store category data
news_items = {
    "Added": [],
    "Changed": [],
    "Deprecated": [],
    "Removed": [],
    "Fixed": [],
    "Security": [],
}

def extract_news_items(file_path):
    """Extract news bullet points under each category for each .rst file."""
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            
            # Check if the line is a category header
            if line.startswith("**") and line.endswith(":**"):
                current_category = line.strip("**:").strip()
            
            # Only add if the line is not empty and not a category header
            elif current_category and line and not line.startswith("* <news item>"):
                news_items[current_category].append(line)
            

def write_merged_file():
    """Add the news items under the ".. current developments" section."""
    CHANGELOG_PATH = "CHANGELOG.rst"
    CHANGELOG_HEADER = ".. current developments"

    # Insert news
    new_news_content = f"\n{tag}\n=====\n\n"
    for category_name in sorted(news_items.keys()):
        items = news_items[category_name]
        if items:
            # Add category name e.g. Added, Changed, etc.
            new_news_content += f"**{category_name}:**\n\n"
            for item in items:
                # Add each item in the category
                new_news_content += f"{item}\n"
            new_news_content += "\n"

    # Read CHANGELOG.rst
    with open(CHANGELOG_PATH, "r") as file:
        current_content = file.read()

    # Find the position to insert news after ".. current developments"
    insert_position = current_content.find(CHANGELOG_HEADER) + len(CHANGELOG_HEADER) + 1
    final_content = current_content[:insert_position] + new_news_content + current_content[insert_position:]

    # Write the updated content back to the file
    with open(CHANGELOG_PATH, "w") as file:
        file.write(final_content)

    return new_news_content

def remove_news_rst_files(news_dir_path):
    """Remove .rst files in the news directory except TEMPLATE.rst"""
    rst_files = os.listdir(news_dir_path)
    for file_name in rst_files:
        rst_file_path = os.path.join(news_dir_path, file_name)
        if file_name.endswith('.rst') and file_name != "TEMPLATE.rst":
            os.remove(rst_file_path)


if __name__ == "__main__":
    NEWS_DIR_PATH = "news"
    
    # Get all news .rst files
    news_rst_files = glob(os.path.join(NEWS_DIR_PATH, "*.rst"))
    
    # Extract and store news items into a single dictionary
    for rst_file in news_rst_files:
        extract_news_items(rst_file)

    # Add news under ".. current developments"
    new_news_content = write_merged_file()
    
    # Remove all .rst files in the news directory except TEMPLATE.rst
    remove_news_rst_files(NEWS_DIR_PATH)

    # Print for debugging
    print(new_news_content)