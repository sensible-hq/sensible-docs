require 'html-proofer'
require 'html/pipeline'
require 'find'
require 'open3'
require 'faraday'
require 'json'

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

response_json = JSON.parse(response.body)
#puts JSON.pretty_generate(response_json)

# script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

rel_path = "out_changelogs"

Dir.mkdir(rel_path) unless File.exist?(rel_path)


# puts "FILE PATH: "
# puts  file_path
#print("PATHS: current:", os.getcwd())
#print("PATHS: intended dest:", file_path)
# left off TODO: make an out dir?
for page in response_json do
  file_path = File.join(rel_path + "/" + page['slug'] + ".html")
  File.open(file_path, 'a+') {|f| f.write(page['html']) }
end


# puts "in out_changelogs dir:"
# puts (Dir.entries(rel_path))






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
}

# puts "contents of Out:"
# Dir.chdir("out") do
#   system "pwd"
#   system "ls"
# end

# check the guides

# make sure that any "internal" '(ref:' links syntax is resolved to full URLs (note: '(doc:' syntax links auto-checked by readme-sync tool anyway, no need to resolve here)
Dir.each_child('./out') do |file_name|
  text = File.read(file_name)
  new_contents = text.gsub(/\(ref\:/, "https://docs.sensible.so/reference/")
  puts new_contents
  File.open(file_name, "w") {|file| file.puts new_contents }
end

HTMLProofer.check_directory("./out", options).run

# check the changelog HTML pulled from ReadmeAPI in a previous step
HTMLProofer.check_directory("./out_changelogs", options).run
