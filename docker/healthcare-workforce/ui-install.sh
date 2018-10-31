#!/bin/bash
cd /healthcare-workforce-master/ui
echo "Installing UI NPM.."
sudo npm install > /tmp/ui-install.txt
echo "Finished, starting UI application.."
sudo npm start
