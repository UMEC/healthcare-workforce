FROM node:11.1-slim
RUN apt-get update 
RUN apt-get install sudo
RUN sudo apt-get -y install python python3-dev && sudo apt-get -y install python3-pip
RUN sudo pip3 install --upgrade pip setuptools wheel
RUN sudo pip3 install pandas
RUN echo "alias python=python3" >> ~/.bashrc
# requirements for cvxopt
RUN sudo apt-get install -y libopenblas-dev
RUN sudo apt-get install -y libsuitesparse-dev
RUN sudo pip3 install cvxopt
RUN sudo pip3 install numpy
RUN sudo pip3 install pulp
# requirements for pulp/glpk
RUN sudo apt-get -y install glpk-utils libglpk-dev glpk-doc libdsdp-dev libfftw3-dev