#!/bin/bash
direnv allow .
echo "updating from Github"
git pull
echo "applying drop shadows to any new images"
# for any PNG that exists in ./readme-sync/assets/v0/images/ but not ./readme-sync/assets/v0/images/borders, convert to drop shadow
# and write to borders dir
for file in ./readme-sync/assets/v0/images/*.png
do
  # regex replacment: ${baseString/patternToMatch/replacePatternWithThis}
  borderFile="${file/images/images/borders}"
  if [ -f "$file" ] && [ ! -f "$borderFile" ]
  then
    echo "processing $file and writing to $borderFile" 
    convert "$file" -bordercolor white -border 0 \( +clone -background black -shadow 80x3+2+2 \) +swap -background white -layers merge +repage "$borderFile"
  fi
done
echo "syncing to Readme "
npx ts-node ~/Github/readme-sync/sync/index.ts --apiKey $README_API_KEY --version v0 --docs ~/Github/sensible-docs/readme-sync/v0