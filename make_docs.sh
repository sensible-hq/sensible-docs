direnv allow .
echo "updating from Github"
git pull
echo "applying drop shadows to new images"
# find all files in this dir maxdpeth 1, I believe exec opens the currently found file(?) add white border, clone last image in image sequence, add black background and shadow, switch the last 2 images in the sequence,  white background, merge (flatten) image layers, remove the layer offset (+repage),  
find ./readme-sync/assets/v0/images/ -maxdepth 1 -type f -exec convert {} -bordercolor white -border 0 \( +clone -background black -shadow 80x3+2+2 \) +swap -background white -layers merge +repage borders/{} \;
echo "syncing to Readme "
npx ts-node sync/index.ts --apiKey $README_API_KEY --version v0 --docs ~/Github/sensible-docs/readme-sync/v0