require 'html-proofer'
require 'html/pipeline'
require 'find'
require 'open3'
require 'faraday'
require 'json'

README_API_KEY = ENV['README_API_KEY']

# get changelogs
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

# script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

rel_path = "out_changelogs"

Dir.mkdir(rel_path) unless File.exist?(rel_path)


file_path = File.join(rel_path + "all_changelogs.html")  
#print("PATHS: current:", os.getcwd())
#print("PATHS: intended dest:", file_path)
# left off TODO: make an out dir?
for page in response_json do
  #print(json.dumps(page['html'], indent=2))
  # left off: write each html to some ./out dir, same as the ruby one...
  # created if not exists:
  File.open(file_path, 'a+') {|f| f.write(page['html']) }
end  
puts ("ALL CHANGELOGS")
File.open(file_path, 'r') {|f| f.read() }
#with open(file_path, 'r') as fin:
  #print(fin.read())
puts "in out_changelogs dir:"
puts (Dir.entries(rel_path))








# make an out dir
# puts "current dir in which to make out dir"
# puts Dir.pwd
if File.exist?("out") do
  puts ("OUT ALREADY EXISTS!")
end  

Dir.mkdir("out") unless File.exist?("out")

puts "contents of Out (TODO: should include the all_changelogs.html from prev. step):"
Dir.chdir("out") do
  system "pwd"
  system "ls"
end



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

# test your out dir's links!
#HTMLProofer.check_directory("./out").run
options = {
  :log_level => :info,
}

# puts "contents of Out:"
# Dir.chdir("out") do
#   system "pwd"
#   system "ls"
# end

# check the guides 
HTMLProofer.check_directory("./out", options).run

# check the changelog HTML pulled from ReadmeAPI in a previous step
HTMLProofer.check_directory("./out_changelogs", options).run 