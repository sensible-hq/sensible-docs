require 'html-proofer'
require 'html/pipeline'
require 'find'

# make an out dir
puts "current dir in which to make out dir"
puts Dir.pwd
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
      puts "checking file:" #{File}
      File.open("out/#{path.split("/").pop.sub('.md', '.html')}", 'w') { |file| file.write(result[:output].to_s) }
    end  
  end
end

# test your out dir's links!
HTMLProofer.check_directory("./out").run
#HTMLProofer.check_directory("./out", {log_level: debug}).run