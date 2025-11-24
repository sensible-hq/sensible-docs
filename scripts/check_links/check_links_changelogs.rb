require 'html-proofer'
require 'faraday'
require 'json'
require 'fileutils'
require 'digest'
require 'html/pipeline'
require 'find'

# Script to check changelog links with change detection
# Edit this in https://github.com/sensible-hq/sensible-docs/settings/secrets/actions
README_API_KEY = ENV['README_API_KEY']

# Cache file to track changes
CACHE_FILE = '.changelog_cache'

# #################
# Get ALL changelogs with pagination
# #################
puts "Fetching all changelogs from API v2..."

def fetch_changelog_page(page_num, per_page = 100)
  url = URI("https://api.readme.com/v2/changelogs?per_page=#{per_page}&page=#{page_num}")
  
  response = Faraday.get(url) do |req|
    req.headers['Content-Type'] = 'application/json'
    req.headers['Authorization'] = "Bearer #{README_API_KEY}"
  end

  if !response.success?
    abort "The request failed: #{response.status} #{response.reason_phrase}\nBody: #{response.body}"
  end

  JSON.parse(response.body)
end

# Fetch all pages
all_changelogs = []
page = 1
per_page = 100  # Maximum allowed by README API

loop do
  puts "Fetching page #{page}..."
  response_data = fetch_changelog_page(page, per_page)
  
  # v2 returns data wrapped in a 'data' object
  changelogs_page = response_data['data'] || []
  
  # Break if no more results
  break if changelogs_page.empty?
  
  all_changelogs.concat(changelogs_page)
  puts "  Retrieved #{changelogs_page.length} changelogs from page #{page}"
  puts "  Total so far: #{all_changelogs.length} of #{response_data['total']}" if response_data['total']
  
  # Break if we got fewer results than requested (last page) or if paging.next is null
  break if changelogs_page.length < per_page
  break if response_data.dig('paging', 'next').nil?
  
  page += 1
end

puts "Total changelogs fetched: #{all_changelogs.length}"

# Use all_changelogs for the rest of the script
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

# #################
# Process URL replacements with tracking
# #################
puts "\nProcessing URL replacements..."

replacements = [
  # Markdown link format: [text](doc:slug) or [text](ref:slug)
  { "](doc:" => "](https://docs.sensible.so/docs/" },
  { "](ref:" => "](https://docs.sensible.so/reference/" },
  { "](changelog:" => "](https://docs.sensible.so/changelog/" },
]

# Track replacements for each changelog
replacement_count = 0
total_replacements = 0

# Process each changelog individually to track replacements
all_changelogs.each_with_index do |changelog, index|
  changelog_slug = changelog['slug'] || "changelog_#{index}"
  changelog_replacements = []
  
  # v2 API: content is in 'content.body' field (MDX/Markdown format)
  # Get the markdown content for processing
  markdown_content = changelog.dig('content', 'body') || ''
  
  # Apply each replacement and track changes
  replacements.each do |replacement|
    replacement.each do |old_pattern, new_pattern|
      # Count occurrences before replacement
      before_count = markdown_content.scan(old_pattern).length
      
      if before_count > 0
        # Perform replacement (gsub with string argument = literal replacement)
        markdown_content = markdown_content.gsub(old_pattern, new_pattern)
        changelog_replacements << {
          pattern: old_pattern,
          replacement: new_pattern,
          count: before_count
        }
        total_replacements += before_count
      end
    end
  end
  
  # Convert JSX Image components to standard img tags for link checking
  # <Image src="url" /> -> <img src="url" />
  image_before_count = markdown_content.scan(/<Image\s+/).length
  if image_before_count > 0
    markdown_content = markdown_content.gsub(/<Image\s+([^>]*?)\/?>/, '<img \1/>')
    changelog_replacements << {
      pattern: "<Image ... />",
      replacement: "<img ... />",
      count: image_before_count
    }
    total_replacements += image_before_count
  end
  
  # Update the changelog object with processed markdown content
  all_changelogs[index]['content'] ||= {}
  all_changelogs[index]['content']['body'] = markdown_content
  
  # Print replacement summary for this changelog
  if changelog_replacements.any?
    puts "📝 Changelog: #{changelog_slug}"
    changelog_replacements.each do |repl|
      puts "  └─ Replaced #{repl[:count]}x: #{repl[:pattern]} → #{repl[:replacement]}"
    end
    replacement_count += 1
  end
end

puts "\n📊 Replacement Summary:"
puts "  Changelogs with replacements: #{replacement_count}/#{all_changelogs.length}"
puts "  Total URL replacements made: #{total_replacements}"

# Update response_json to use the processed changelogs
response_json = all_changelogs

# Create output directory for changelogs
rel_path = "out_changelogs"

# Delete the directory if it exists
FileUtils.rm_rf(rel_path) if File.exist?(rel_path)

# Create the directory
Dir.mkdir(rel_path)

# Write changelog markdown files
for page in response_json do
  file_path = File.join(rel_path + "/" + page['slug'] + ".md")
  # Use the processed markdown content
  markdown_content = page.dig('content', 'body') || ''
  File.open(file_path, 'w') {|f| f.write(markdown_content) }
end

# List created files
puts "\nCreated changelog markdown files:"
Dir.entries(rel_path).select { |f| f.end_with?('.md') }.each do |file_name|
  puts "  #{file_name}"
end

# #################
# Convert Markdown to HTML for link checking
# #################
puts "\nConverting Markdown files to HTML..."

# Create output directory for HTML files
html_output_dir = "out_changelogs_html"
Dir.mkdir(html_output_dir) unless File.exist?(html_output_dir)

# Set up HTML pipeline for Markdown conversion
pipeline = HTML::Pipeline.new [
  HTML::Pipeline::MarkdownFilter,
  HTML::Pipeline::TableOfContentsFilter
], :gfm => true

# Iterate over markdown files and generate HTML
html_file_count = 0
Find.find(rel_path) do |path|
  if File.extname(path) == ".md"
    contents = File.read(path)
    # Only check published files ("hidden: true" are unpublished)
    if not contents.match(/hidden\:\s*true/)
      # Convert JSX Image components to standard img tags for link checking
      # <Image src="url" /> -> <img src="url" />
      contents_for_checking = contents
      
      result = pipeline.call(contents_for_checking)
      output_filename = "#{html_output_dir}/#{File.basename(path).sub('.md', '.html')}"
      File.open(output_filename, 'w') { |file| file.write(result[:output].to_s) }
      puts "  Converted: #{File.basename(path)}"
      # print file contents
      puts "file contents:"
      puts File.read(path)

      html_file_count += 1
    else
      puts "  Skipped (hidden): #{File.basename(path)}"
    end
  end
end

puts "Converted #{html_file_count} markdown files to HTML"

# #################
# Test changelog links
# #################

options = {
  # https://github.com/gjtorikian/html-proofer for options
  :log_level => :info,
  :ignore_missing_alt => true,
  :url_ignore => [
    "https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api",
    "https://platform.openai.com/tokenizer",
    "https://platform.openai.com/docs/guides/prompt-engineering",
    "https://beta.openai.com/docs/"
  ]
}

puts "\nChecking changelog links..."
HTMLProofer.check_directory("./#{html_output_dir}", options).run
puts "Changelog link checking complete!"

# Update cache with current hash only after successful completion
File.write(CACHE_FILE, current_hash)
puts "Cache updated with hash: #{current_hash}"