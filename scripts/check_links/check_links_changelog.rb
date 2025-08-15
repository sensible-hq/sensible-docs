require 'html-proofer'
require 'faraday'
require 'json'
require 'fileutils'

# Script to check changelog links
# Edit this in https://github.com/sensible-hq/sensible-docs/settings/secrets/actions
README_API_KEY = ENV['README_API_KEY']

# #################
# Get changelogs
# #################
url = URI("https://dash.readme.com/api/v1/changelogs?perPage=10&page=1")

response = Faraday.get(url) do |req|
  req.headers['Content-Type'] = 'application/json'
  req.headers["Authorization"] = "Basic #{README_API_KEY}"
  req.headers["x-readme-version"] = "v0"
end

if !response.success?
  abort "The request failed: #{response.status} #{response.reason_phrase}"
end

# Parse response
response_json = JSON.parse(response.body)
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