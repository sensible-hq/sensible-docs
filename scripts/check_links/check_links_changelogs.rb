require 'html-proofer'
require 'faraday'
require 'json'
require 'fileutils'
require 'digest'

# Script to check changelog links with change detection
# Edit this in https://github.com/sensible-hq/sensible-docs/settings/secrets/actions
README_API_KEY = ENV['README_API_KEY']

# Cache file to track changes
CACHE_FILE = '.changelog_cache'

# #################
# Get ALL changelogs with pagination
# #################
puts "Fetching all changelogs from API..."

def fetch_changelog_page(page_num, per_page = 100)
  url = URI("https://dash.readme.com/api/v1/changelogs?perPage=#{per_page}&page=#{page_num}")
  
  response = Faraday.get(url) do |req|
    req.headers['Content-Type'] = 'application/json'
    req.headers["Authorization"] = "Basic #{README_API_KEY}"
    req.headers["x-readme-version"] = "v0"
  end

  if !response.success?
    abort "The request failed: #{response.status} #{response.reason_phrase}"
  end

  JSON.parse(response.body)
end

# Fetch all pages
all_changelogs = []
page = 1
per_page = 100  # Maximum allowed by README API

loop do
  puts "Fetching page #{page}..."
  changelogs_page = fetch_changelog_page(page, per_page)
  
  # Break if no more results
  break if changelogs_page.empty?
  
  all_changelogs.concat(changelogs_page)
  puts "  Retrieved #{changelogs_page.length} changelogs from page #{page}"
  
  # Break if we got fewer results than requested (last page)
  break if changelogs_page.length < per_page
  
  page += 1
end

puts "Total changelogs fetched: #{all_changelogs.length}"

# Use all_changelogs instead of response_json for the rest of the script
response_json = all_changelogs

# Parse response and create content hash
# Create hash of all changelogs to detect changes
current_hash = Digest::MD5.hexdigest(all_changelogs.to_json)

# Check if content has changed since last run
if File.exist?(CACHE_FILE)
  cached_hash = File.read(CACHE_FILE).strip
  if cached_hash == current_hash
    puts "No changes detected in changelogs since last run. Skipping link check."
    puts "Cached hash: #{cached_hash}"
    puts "Current hash: #{current_hash}"
    exit 0
  else
    puts "Changes detected in changelogs!"
    puts "Cached hash: #{cached_hash}"
    puts "Current hash: #{current_hash}"
  end
else
  puts "No cache file found. This appears to be the first run."
end

json_string = response_json.to_json

# Remove relative links from the response and convert to absolute URL links
replacements = [
  { "(doc:" => "(https://docs.sensible.so/docs/" },
  { "(ref:" => "(https://docs.sensible.so/reference/" },
  { "(changelog:" => "(https://docs.sensible.so/changelog/" }
]

# Replace all instances of the strings
replacements.each do |replacement|
  replacement.each do |old, new_value|
    json_string = JSON.parse(json_string.to_json.gsub(old, new_value))
  end
end

response_json = JSON.parse(json_string)

# Create output directory for changelogs
rel_path = "out_changelogs"

# Delete the directory if it exists
FileUtils.rm_rf(rel_path) if File.exist?(rel_path)

# Create the directory
Dir.mkdir(rel_path)

# Write changelog HTML files
for page in response_json do
  file_path = File.join(rel_path + "/" + page['slug'] + ".html")
  File.open(file_path, 'a+') {|f| f.write(page['html']) }
end

# List created files
puts "Created changelog files:"
Dir.entries(rel_path).each do |file_name|
  next if file_name == "." || file_name == ".."
  puts "  #{file_name}"
end

# #################
# Test changelog links
# #################

options = {
  :log_level => :info,
  :url_ignore => [
    "https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api",
    "https://platform.openai.com/tokenizer",
    "https://platform.openai.com/docs/guides/prompt-engineering",
    "https://beta.openai.com/docs/"
  ]
}

puts "\nChecking changelog links..."
HTMLProofer.check_directory("./out_changelogs", options).run
puts "Changelog link checking complete!"

# Update cache with current hash only after successful completion
File.write(CACHE_FILE, current_hash)
puts "Cache updated with hash: #{current_hash}"