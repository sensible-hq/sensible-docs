

for file in ./readme-guides/assets/v0/images/screenshots/*.png #TODO add *.jpeg
do
  # regex replacment: ${baseString/patternToMatch/replacePatternWithThis}
  finalFile="${file/images\/screenshots/images\/final}"
  lastCommit=$(git log -n 1 --date=relative --format=%cd $file)
  # any commits in the last 24 hrs (upper limit? unsure. less than 47 hrs?), OR if file exists in screenshots but not final dir

  if [[ "$lastCommit" =~ .*+(second|minute).* ]] || ([ -f "$file" ] && [ ! -f "$finalFile" ])
  then
  echo "updating $finalFile because it doesn't exist in /final or its source was last committed $lastCommit"
  # apply a drop shadow to screenshots
  convert "$file" -bordercolor white -border 0 \( +clone -background black -shadow 80x3+2+2 \) +swap -background white -layers merge +repage "$finalFile"
  fi
done
