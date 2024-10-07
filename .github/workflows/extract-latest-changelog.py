changelog_file = "CHANGELOG.rst"

# Read the entire changelog file
with open(changelog_file, "r") as file:
    content = file.read()

# Find the position of '.. current developments'
start_index = content.find('.. current developments')
print(start_index)

# # Start extracting after the '.. current developments'
# start_index = content.find('\n', start_index) + 1
# end_index = content.find('=====', start_index)  # Find the next '=====' line

# if end_index != -1:
#     # Extract the changelog content for the latest version
#     latest_changelog = content[start_index:end_index].strip()

#     # Save the extracted changelog to a file
#     with open("changelog.txt", "w") as output_file:
#         output_file.write(latest_changelog)
# else:
#     print("No '=====' found after the version header.")

