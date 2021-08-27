#!/bin/bash
direnv allow .
echo "updating from Github"
git pull
echo "applying drop shadows to any new filenames in screenshots but not in final"
# for any PNG that exists in ./readme-sync/assets/v0/images/ but not ./readme-sync/assets/v0/images/final, convert to drop shadow
# and write to final dir

mkdir -p ./readme-sync/assets/v0/images/final

for file in ./readme-sync/assets/v0/images/screenshots/*.png
do
  # regex replacment: ${baseString/patternToMatch/replacePatternWithThis}
  finalFile="${file/images\/screenshots/images\/final}"
  if [ -f "$file" ] && [ ! -f "$finalFile" ]
  then
    echo "processing $file and writing to $finalFile" 
    convert "$file" -bordercolor white -border 0 \( +clone -background black -shadow 80x3+2+2 \) +swap -background white -layers merge +repage "$finalFile"
  fi
done
echo "syncing to Readme "
npx ts-node ~/Github/readme-sync/sync/index.ts --apiKey $README_API_KEY --version v0 --docs ~/Github/sensible-docs/readme-sync/v0

