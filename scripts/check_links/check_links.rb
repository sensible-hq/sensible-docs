require 'html-proofer'
require 'html/pipeline'
require 'find'
require 'fileutils'
require 'net/http'

# Script to check documentation guides links

# #################
# Process markdown files with URL replacements
# #################
puts "Processing Markdown files..."

replacements = [
  # Markdown link format: [text](doc:slug) or [text](ref:slug)
  { "](doc:" => "](https://docs.sensible.so/docs/" },
  { "](ref:" => "](https://docs.sensible.so/reference/" },
  { "](changelog:" => "](https://docs.sensible.so/changelog/" },
]

# Track replacements
total_replacements = 0
jsx_urls = []  # Collect all URLs from JSX elements
processed_files = []

# Process each markdown file
Find.find("./docs", "./reference") do |path|
  if File.extname(path) == ".md"
    markdown_content = File.read(path)
    
    # Only process published files ("hidden: true" are unpublished)
    if not markdown_content.match(/hidden\:\s*true/)
      file_replacements = []
      
      # Extract URLs from any JSX elements (components starting with capital letters)
      # This catches both self-closing tags and tags with content
      
      # Method 1: Find self-closing JSX tags like <Image src="..." />
      markdown_content.scan(/<([A-Z]\w*)\s+([^>]*?)\/?>/).each do |match|
        component_name = match[0]
        attributes = match[1]
        
        # Extract any URL-like attributes (src, href, url, etc.)
        attributes.scan(/(?:src|href|url)="([^"]*)"/).each do |url_match|
          jsx_urls << { 
            url: url_match[0], 
            file: File.basename(path), 
            element: component_name,
            attribute: url_match[0].match(/^(src|href|url)=/i) ? $1 : 'unknown'
          }
        end
      end
      
      # Method 2: Find JSX tags with closing tags like <HTMLBlock>...</HTMLBlock>
      markdown_content.scan(/<([A-Z]\w*)[^>]*?>(.*?)<\/\1>/m).each do |match|
        component_name = match[0]
        content = match[1]
        
        # Extract URLs from within the content
        content.scan(/(?:src|href|url)="([^"]*)"/).each do |url_match|
          jsx_urls << { 
            url: url_match[0], 
            file: File.basename(path), 
            element: component_name,
            attribute: 'content'
          }
        end
      end
      
      # Apply each replacement and track changes
      replacements.each do |replacement|
        replacement.each do |old_pattern, new_pattern|
          # Count occurrences before replacement
          before_count = markdown_content.scan(old_pattern).length
          
          if before_count > 0
            # Perform replacement (gsub with string argument = literal replacement)
            markdown_content = markdown_content.gsub(old_pattern, new_pattern)
            file_replacements << {
              pattern: old_pattern,
              replacement: new_pattern,
              count: before_count
            }
            total_replacements += before_count
          end
        end
      end
      
      # Store processed content
      processed_files << {
        path: path,
        content: markdown_content,
        replacements: file_replacements
      }
      
      # Print replacement summary for this file
      if file_replacements.any?
        puts "📝 File: #{File.basename(path)}"
        file_replacements.each do |repl|
          puts "  └─ Replaced #{repl[:count]}x: #{repl[:pattern]} → #{repl[:replacement]}"
        end
      end
    else
      puts "  Skipped (hidden): #{File.basename(path)}"
    end
  end
end

puts "\n📊 Processing Summary:"
puts "  Files processed: #{processed_files.length}"
puts "  Total URL replacements made: #{total_replacements}"
puts "  JSX URLs found: #{jsx_urls.length}"

# Show breakdown by JSX element type
jsx_by_element = jsx_urls.group_by { |item| item[:element] }
jsx_by_element.each do |element, urls|
  puts "    - #{element}: #{urls.length} URL(s)"
end

# #################
# Convert processed Markdown files to HTML
# #################
puts "\nConverting Markdown files to HTML..."

# Create output directory
Dir.mkdir("out") unless File.exist?("out")

# Set up HTML pipeline for Markdown conversion
pipeline = HTML::Pipeline.new [
  HTML::Pipeline::MarkdownFilter,
  HTML::Pipeline::TableOfContentsFilter
], :gfm => true

# Iterate over processed files and generate HTML
processed_files.each do |file_data|
  result = pipeline.call(file_data[:content])
  output_filename = "out/#{file_data[:path].split("/").pop.sub('.md', '.html')}"
  File.open(output_filename, 'w') { |file| file.write(result[:output].to_s) }
  puts "  Converted: #{File.basename(file_data[:path])}"
end

# #################
# Test guide links
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

puts "\nChecking guide links..."
html_proofer_failed = false
begin
  HTMLProofer.check_directory("./out", options).run
  puts "✅ Guide link checking complete - no errors found!"
rescue SystemExit => e
  if e.status != 0
    puts "❌ HTMLProofer found errors (exit status: #{e.status})"
    html_proofer_failed = true
  end
rescue => e
  puts "❌ HTMLProofer encountered an error: #{e.message}"
  html_proofer_failed = true
end

# #################
# Check JSX URLs
# #################
puts "\nChecking JSX URLs..."
jsx_failures = []

jsx_urls.each do |item|
  begin
    uri = URI.parse(item[:url])
    response = Net::HTTP.get_response(uri)
    if response.code.to_i >= 400
      error_msg = "❌ BROKEN URL in <#{item[:element]}> in #{item[:file]}: #{item[:url]} (#{response.code})"
      puts error_msg
      jsx_failures << error_msg
    else
      puts "✅ <#{item[:element]}> #{item[:url]}"
    end
  rescue => e
    error_msg = "❌ ERROR checking #{item[:url]} from <#{item[:element]}>: #{e.message}"
    puts error_msg
    jsx_failures << error_msg
  end
end

# #################
# Final status report
# #################
puts "\n" + "="*80
puts "FINAL STATUS REPORT"
puts "="*80

has_errors = false

if html_proofer_failed
  puts "❌ HTMLProofer: FAILED"
  has_errors = true
else
  puts "✅ HTMLProofer: PASSED"
end

if jsx_failures.any?
  puts "❌ JSX URLs: FAILED (#{jsx_failures.length} error(s))"
  has_errors = true
else
  puts "✅ JSX URLs: PASSED"
end

if has_errors
  puts "\n❌ Link checking failed - see errors above"
  abort "Link checking failed"
else
  puts "\n✅ All link checks passed!"
end