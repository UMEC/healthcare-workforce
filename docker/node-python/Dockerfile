FROM circleci/node:7.10
RUN sudo apt-get update && sudo apt-get install python3-dev && sudo apt-get install python3-pip
RUN sudo pip3 install --upgrade pip setuptools wheel
RUN sudo pip3 install pandas
RUN echo "alias python=python3" >> ~/.bashrc