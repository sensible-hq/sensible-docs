for file in ./readme-sync/assets/v0/images/callouts/*.png
do
  # regex replacment: ${baseString/patternToMatch/replacePatternWithThis}
  borderFile="${file/images\/callouts/images\/borders}"
  if [ -f "$file" ] && [ ! -f "$borderFile" ]
  then
    echo "processing $file and writing to $borderFile" 
    convert "$file" -bordercolor white -border 0 \( +clone -background black -shadow 80x3+2+2 \) +swap -background white -layers merge +repage "$borderFile"
  fi
done
