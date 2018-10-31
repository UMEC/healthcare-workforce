#!/bin/bash
cd /healthcare-workforce-master
echo Installing server NPM..
sudo npm install > /tmp/server-install.txt
echo Finished, starting server API application.. (Likely still waiting for the UI to start)
sudo npm start
