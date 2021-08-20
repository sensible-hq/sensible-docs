direnv allow .
echo "updating from Github"
git pull
echo "applying drop shadows to new images" 
find ./readme-sync/assets/v0/images/ -maxdepth 1 -type f -execdir convert {} -bordercolor white -border 0 \( +clone -background black -shadow 80x3+2+2 \) +swap -background white -layers merge +repage borders/{} \;
echo "syncing to Readme "
npx ts-node ~/Github/readme-sync/sync/index.ts --apiKey $README_API_KEY --version v0 --docs ~/Github/sensible-docs/readme-sync/v0