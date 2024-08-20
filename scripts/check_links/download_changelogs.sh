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
if [ $? -ne 0 ] || [ -z "$response" ]; then
  echo "The request failed or returned no data."
  exit 1
fi

# Remove relative links from the response and convert to absolute URL links
# This time, we handle the JSON properly, without converting it to a string
response_json=$(echo "$response" | jq 'map_values(gsub("\\(doc:"; "(https://docs.sensible.so/docs/")) | map_values(gsub("\\(ref:"; "(https://docs.sensible.so/reference/")) | map_values(gsub("\\(changelog:"; "(https://docs.sensible.so/changelog/"))')

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
