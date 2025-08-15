require 'html-proofer'
require 'html/pipeline'
require 'find'
require 'fileutils'

# Script to check documentation guides links

# #################
# Convert existing local MD files to HTML
# #################

# Create output directory
Dir.mkdir("out") unless File.exist?("out")

# Set up HTML pipeline for Markdown conversion
pipeline = HTML::Pipeline.new [
  HTML::Pipeline::MarkdownFilter,
  HTML::Pipeline::TableOfContentsFilter
], :gfm => true

# Iterate over files and generate HTML from Markdown
puts "Converting Markdown files to HTML..."
Find.find("./readme-sync/v0") do |path|
  if File.extname(path) == ".md"
    contents = File.read(path)
    # Only check published files ("hidden: true" are unpublished)
    if not contents.match(/hidden\:\s*true/)
      result = pipeline.call(contents)
      output_filename = "out/#{path.split("/").pop.sub('.md', '.html')}"
      File.open(output_filename, 'w') { |file| file.write(result[:output].to_s) }
      puts "  Converted: #{File.basename(path)}"
    else
      puts "  Skipped (hidden): #{File.basename(path)}"
    end
  end
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
HTMLProofer.check_directory("./out", options).run
puts "Guide link checking complete!"