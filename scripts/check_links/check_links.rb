require 'html-proofer'
require 'html/pipeline'
require 'find'
require 'open3'
require 'faraday'
require 'json'
require 'pathname'
require 'fileutils'

# excludes API ref links checking b/c it's tough to parse the downloaded HTML to get the actual documentation part...maybe if I saved the 'body' part??
# another alternative would be to take the yamls, turn them into markdown, convert internal link syntax to fully expanded URLs, and THEN check that.

# edit this in https://github.com/sensible-hq/sensible-docs/settings/secrets/actions
README_API_KEY = ENV['README_API_KEY']

# #################
# get changelogs
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


# these two lines are probably redudant, just need the json string really
# to hash
response_json = JSON.parse(response.body)
# to json string
json_string = response_json.to_json

# remove relative links from the response
# and convert to absolute URL links

# Array of replacements
replacements = [
  { "(doc:" => "(https://docs.sensible.so/docs/" },
  { "(ref:" => "(https://docs.sensible.so/reference/" },
  { "(changelog:" => "(https://docs.sensible.so/changelog/" }
]


# Replace all instances of the strings in the hash
replacements.each do |replacement|
  replacement.each do |old, new_value|
    json_string = JSON.parse(json_string.to_json.gsub(old, new_value))
  end
end

#print(json_string)

response_json = JSON.parse(json_string)

#puts JSON.pretty_generate(response_json)

# script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

rel_path = "out_changelogs"

# Delete the directory if it exists
FileUtils.rm_rf(rel_path) if File.exist?(rel_path)

# Create the directory
Dir.mkdir(rel_path)


# puts "FILE PATH: "
# puts  file_path
#print("PATHS: current:", os.getcwd())
#print("PATHS: intended dest:", file_path)
# left off TODO: make an out dir?
for page in response_json do
  print page
  file_path = File.join(rel_path + "/" + page['slug'] + ".html")
  File.open(file_path, 'a+') {|f| f.write(page['html']) }
end


# puts "in out_changelogs dir:"
# puts (Dir.entries(rel_path))

# troubleshoot: did the changelogs print correctly?

# List the files in the directory
Dir.entries(rel_path).each do |file_name|
  # Skip "." and ".."
  next if file_name == "." || file_name == ".."

  # Construct the full path to the file
  file_path = File.join(rel_path, file_name)

  # Print the file name
  puts "File: #{file_name}"

  # # Print the file content
  # if File.file?(file_path)
  #   file_content = File.read(file_path)
  #   puts "Content:\n#{file_content}\n\n"
  # else
  #   puts "The path #{file_path} is not a file."
  # end
end





# #################
# Convert existing local MD files to HTML
# #################

# make an out dir

Dir.mkdir("out") unless File.exist?("out")





pipeline = HTML::Pipeline.new [
  HTML::Pipeline::MarkdownFilter,
  HTML::Pipeline::TableOfContentsFilter
], :gfm => true

# iterate over files, and generate HTML from Markdown
Find.find("./readme-sync/v0") do |path|
  if File.extname(path) == ".md"
    contents = File.read(path)
    # only check published files ("hidden: true" are unpublished)
    if not contents.match(/hidden\:\s*true/)
      result = pipeline.call(contents)
      # puts "converting file: #{File.basename(path)}"
      File.open("out/#{path.split("/").pop.sub('.md', '.html')}", 'w') { |file| file.write(result[:output].to_s) }
    end
  end
end




# #################
# test your out dir's links!
# #################

options = {
  :log_level => :info,
  :url_ignore => ["https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api","https://platform.openai.com/tokenizer","https://platform.openai.com/docs/guides/prompt-engineering","https://beta.openai.com/docs/"],
  # ignore internal links like doc:color
  :check_internal_links => false
}





# check the guides
HTMLProofer.check_directory("./out", options).run

# check the changelog HTML pulled from ReadmeAPI in a previous step
## HTMLProofer.check_directory("./out_changelogs", options).run
