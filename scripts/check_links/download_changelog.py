import os
import json
import requests
import shutil

# Exclude API ref links checking

# Set up the environment variable for the API key
README_API_KEY = os.getenv('README_API_KEY')

# #################
# Get changelogs
# #################
url = "https://dash.readme.com/api/v1/changelogs?perPage=10&page=1"

# Make the request to the API
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {README_API_KEY}',
    'x-readme-version': 'v0'
}

response = requests.get(url, headers=headers)

if not response.ok:
    raise Exception(f"The request failed: {response.status_code} {response.reason}")

# Convert response body to a JSON string
json_string = response.text

print("response.text")
print(json_string)

# Array of replacements for relative links to absolute URLs
replacements = {
    "(doc:": "(https://docs.sensible.so/docs/",
    "(ref:": "(https://docs.sensible.so/reference/",
    "(changelog:": "(https://docs.sensible.so/changelog/"
}

# Replace all instances of the strings in the JSON string
for old, new_value in replacements.items():
    json_string = json_string.replace(old, new_value)

# Parse the modified JSON string back to a Python object
response_json = json.loads(json_string)

print("response json:")
print(response_json)

# Directory for output
rel_path = "out_changelogs"

# Delete the directory if it exists
if os.path.exists(rel_path):
    shutil.rmtree(rel_path)

# Create the directory
os.mkdir(rel_path)

# Save each page's content as a separate HTML file
for page in response_json:
    file_path = os.path.join(rel_path, f"{page['slug']}.html")
    with open(file_path, 'w') as file:
        file.write(page['html'])

# List the files in the directory
for file_name in os.listdir(rel_path):
    # Skip "." and ".."
    if file_name not in [".", ".."]:
        file_path = os.path.join(rel_path, file_name)
        # Print the file name
        print(f"File: {file_name}")

        # If you want to print the file content, uncomment below:
        # if os.path.isfile(file_path):
        #     with open(file_path, 'r') as file:
        #         file_content = file.read()
        #         print(f"Content:\n{file_content}\n\n")
        # else:
        #     print(f"The path {file_path} is not a file.")
