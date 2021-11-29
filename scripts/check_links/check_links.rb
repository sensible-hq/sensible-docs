require 'html-proofer'
require 'html/pipeline'
require 'find'
require 'open3'

# make an out dir
# puts "current dir in which to make out dir"
# puts Dir.pwd
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

puts "contents of Out:"
Dir.chdir("out") do
  system "pwd"
  system "ls"
end

# check the guides 
HTMLProofer.check_directory("./out", options).run

# check the changelog HTML pulled from ReadmeAPI in a previous step
HTMLProofer.check_directory("./out_changelogs", options).run 