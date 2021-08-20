echo "applying drop shadows to new images"
find ./readme-sync/assets/v0/images -maxdepth 1 -type f -exec convert {} -bordercolor white -border 0 \( +clone -background black -shadow 80x3+2+2 \) +swap -background white -layers merge +repage ./readme-sync/assets/v0/images/borders/{} \;
