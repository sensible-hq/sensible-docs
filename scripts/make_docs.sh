#!/bin/bash
direnv allow .
echo "updating from Github"
git pull
echo "applying drop shadows to screenshots if any were recently committed"
# for any PNG that was recently committed in ./readme-sync/assets/v0/images/screenshots, process and write to ./readme-sync/assets/v0/images/final, convert to drop shadow
# this saves image processing time and should catch any updates you make to screenshots as long as you're running make_docs regularly

cd ../

mkdir -p ./readme-sync/assets/v0/images/final

for file in ./readme-sync/assets/v0/images/screenshots/*.png
do
  # regex replacment: ${baseString/patternToMatch/replacePatternWithThis}
  finalFile="${file/images\/screenshots/images\/final}"
  lastCommit=$(git log -n 1 --date=relative --format=%cd $file)
  # if [ -f "$file" ] && [ ! -f "$finalFile" ] 
  # any commits in the last 24 hrs (upper limit? unsure. less than 47 hrs?), OR if file exists in screenshots but not final dir

  if [[ "$lastCommit" =~ .*+(second|minute).* ]] || ([ -f "$file" ] && [ ! -f "$finalFile" ])
  then
  echo "updating $finalFile because it doesn't exist in /final or its source was last committed $lastCommit" 
  # apply a drop shadow to screenshots
  convert "$file" -bordercolor white -border 0 \( +clone -background black -shadow 80x3+2+2 \) +swap -background white -layers merge +repage "$finalFile"
  fi
done



echo "syncing to Readme "

	
npx ts-node ~/Github/readme-sync/sync/index.ts --apiKey $README_API_KEY --version v0 --docs ~/Github/sensible-docs/readme-sync/v0 #npx ts-node ~/Github/readme-sync/sync/index.ts --apiKey $README_API_KEY --version v0 --docs ~/Github/sensible-docs/readme-sync/v0


# if there are local uncommitted changes, commit them. for example as output of imagemagick.
# https://newbedev.com/checking-for-a-dirty-index-or-untracked-files-with-git
git ls-files --others --error-unmatch . >/dev/null 2>&1; ec=$?
if test "$ec" = 0; then
    echo some untracked files
    git add -A 
    echo "git status:"
    git status
    git commit -m "updating local style changes to images"
    git push
elif test "$ec" = 1; then
    echo no untracked files
else
    echo error from ls-files
fi

if ! git diff-index --quiet HEAD --; then
    echo "local staged changes exist"
fi    



# check broken links
rm logs.csv
touch logs.csv

# npx linkinator https://docs.sensible.so/changelog --verbosity ERROR --recurse --format CSV >> logs.csv 
# npx linkinator https://docs.sensible.so/reference --verbosity ERROR --recurse --format CSV >> logs.csv 

npx linkinator https://docs.sensible.so/docs --verbosity ERROR --recurse --format CSV >> logs.csv 

cat logs.csv


