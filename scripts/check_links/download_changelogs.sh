#!/bin/bash

# Exclude API ref links checking

# Edit this in https://github.com/sensible-hq/sensible-docs/settings/secrets/actions
README_API_KEY=$README_API_KEY

# #################
# Get changelogs
# #################
url="https://dash.readme.com/api/v1/changelogs?perPage=10&page=1"

# Make the request to the API
response=$(curl -s -H "Content-Type: application/json" -H "Authorization: Basic $README_API_KEY" -H "x-readme-version: v0" "$url")

# Check if the request was successful
if [ $? -ne 0 ]; then
  echo "The request failed."
  exit 1
fi

# Remove relative links from the response and convert to absolute URL links
response_json=$(echo "$response" | jq -r '. | tostring' | sed -e 's/(doc:/\(https:\/\/docs.sensible.so\/docs\//g' -e 's/(ref:/\(https:\/\/docs.sensible.so\/reference\//g' -e 's/(changelog:/\(https:\/\/docs.sensible.so\/changelog\//g')

# Create the output directory
rel_path="out_changelogs"
rm -rf "$rel_path"
mkdir "$rel_path"

# Loop through the response and save each page as a file
echo "$response_json" | jq -c '.[]' | while read -r page; do
  slug=$(echo "$page" | jq -r '.slug')
  html=$(echo "$page" | jq -r '.html')
  file_path="$rel_path/$slug.html"
  echo "$html" > "$file_path"
done

# List the files in the directory
for file_name in "$rel_path"/*; do
  if [ -f "$file_name" ]; then
    echo "File: $(basename "$file_name")"
  fi
done