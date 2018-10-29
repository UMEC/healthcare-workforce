#!/bin/bash
zip_url="https://github.com/UMEC/healthcare-workforce/archive/master.zip"
set +e
echo Downloading latest application zip: $zip_url
sudo curl -qLO $zip_url .
set -e
echo Unzipping..

if ls healthcare-workforce-master/models/data/data_input_component_csv/* 1> /dev/null 2>&1; then
   echo "Found existing user data, leaving as-is."
   #Overwrite everything except the data folder
   sudo unzip -qo master.zip -x "healthcare-workforce-master/models/data/data_input_component_csv/*.*"
else
   echo "No user data found, extracting sample data."
   sudo unzip -qo master.zip
   
fi

cd healthcare-workforce-master
echo Installing NPM..
sudo npm install
echo Finished, starting application..
sudo npm start
