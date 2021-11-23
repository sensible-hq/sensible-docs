require 'html-proofer'
require 'html/pipeline'
require 'find'

# make an out dir
Dir.mkdir("out") unless File.exist?("out")
p "current working dir in which /out is made:"
p File.expand_path(File.dirname(File))
pipeline = HTML::Pipeline.new [
  HTML::Pipeline::MarkdownFilter,
  HTML::Pipeline::TableOfContentsFilter
], :gfm => true

# iterate over files, and generate HTML from Markdown
Find.find("./readme-sync/v0") do |path| 
  if File.extname(path) == ".md" 
    contents = File.read(path)
    # only check published files ("hidden: false")
    if contents.match(/hidden\:\s*false/)  
      result = pipeline.call(contents)
      File.open("out/#{path.split("/").pop.sub('.md', '.html')}", 'w') { |file| file.write(result[:output].to_s) }
    end  
  end
end

# test your out dir's links!
HTMLProofer.check_directory("./out").run
#HTMLProofer.check_directory("./out", {log_level: debug}).run