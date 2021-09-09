#!/bin/bash
direnv allow .
echo "updating from Github"
git pull
echo "applying drop shadows to screenshots if any were recently committed"
# for any PNG that exists in ./readme-sync/assets/v0/images/ but not ./readme-sync/assets/v0/images/final, convert to drop shadow
# and write to final dir

mkdir -p ./readme-sync/assets/v0/images/final

for file in ./readme-sync/assets/v0/images/screenshots/*.png
do
  # regex replacment: ${baseString/patternToMatch/replacePatternWithThis}
  finalFile="${file/images\/screenshots/images\/final}"
  lastCommit=$(git log -n 1 --date=relative --format=%cd $file)
  #if [ -f "$file" ] && [ ! -f "$finalFile" ]
  # if the image was committed in the last 2 days, update it. this should catch all updates as long as you sync docs soon after modifying images
  if [[ "$lastCommit" =~ .*+(second|minute|hour).* ]] 
  then
  echo "processing $file and writing to $finalFile because it was last committed $lastCommit" 
  convert "$file" -bordercolor white -border 0 \( +clone -background black -shadow 80x3+2+2 \) +swap -background white -layers merge +repage "$finalFile"
  fi
done



echo "syncing to Readme "
npx ts-node ~/Github/readme-sync/sync/index.ts --apiKey $README_API_KEY --version v0 --docs ~/Github/sensible-docs/readme-sync/v0


# if there are local uncommitted changes, commit them (for example as output of imagemagick)
if ! git diff-index --quiet HEAD --; then
    echo "REMEMBER TO COMMIT LOCAL UNTRACKED CHANGES"
fi