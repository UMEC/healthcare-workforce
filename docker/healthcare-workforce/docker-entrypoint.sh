#!/bin/bash
zip_url="https://github.com/UMEC/healthcare-workforce/archive/master.zip"
set +e
echo Downloading latest application zip: $zip_url
sudo curl -qLO $zip_url /
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

/usr/local/bin/server-install.sh -D &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start server-install: $status"
  exit $status
fi

# Start the second process
/usr/local/bin/ui-install.sh -D &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start ui-install: $status"
  exit $status
fi

# Start the second process
/usr/local/bin/jupyter-start.sh -D &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start jupyter-start: $status"
  exit $status
fi

while sleep 60; do
  ps aux |grep server-install |grep -q -v grep
  PROCESS_1_STATUS=$?
  ps aux |grep ui-install |grep -q -v grep
  PROCESS_2_STATUS=$?
  ps aux |grep jupyter-start |grep -q -v grep
  PROCESS_3_STATUS=$?
  # If the greps above find anything, they exit with 0 status
  # If they are not all 0, then something is wrong
  if [ $PROCESS_1_STATUS -ne 0 -o $PROCESS_2_STATUS -ne 0 -o $PROCESS_3_STATUS -ne 0 ]; then
    echo "One of the processes has exited unexpectedly. Please restart the container."
    exit 1
  fi
done
