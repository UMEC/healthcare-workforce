#!/bin/bash
zip_url="https://github.com/UMEC/healthcare-workforce/archive/master.zip"
set +e
echo Downloading latest application zip: $zip_url
sudo curl -qLO $zip_url .
set -e
echo Unzipping..
#Overwrite everything except the data folder
sudo unzip -qo master.zip -x "healthcare-workforce-master/models/test/data_input_component_csv/*.*"
cd healthcare-workforce-master
echo Installing NPM..
sudo npm install
echo Starting application..
sudo npm start
