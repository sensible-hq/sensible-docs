# check broken links
rm logs.csv
touch logs.csv

# npx linkinator https://docs.sensible.so/changelog --verbosity ERROR --recurse --format CSV >> logs.csv 
# npx linkinator https://docs.sensible.so/reference --verbosity ERROR --recurse --format CSV >> logs.csv 

npx linkinator https://docs.sensible.so/docs --verbosity ERROR --recurse --format CSV >> logs.csv 

cat logs.csv
