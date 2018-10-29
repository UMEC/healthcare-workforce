FROM circleci/node:7.10
RUN sudo apt-get update && sudo apt-get install python3-dev && sudo apt-get install python3-pip
RUN sudo pip3 install --upgrade pip setuptools wheel
RUN sudo pip3 install pandas
RUN echo "alias python=python3" >> ~/.bashrc
# requirements for cvxopt
RUN sudo apt-get install libopenblas-dev
RUN sudo apt-get install libsuitesparse-dev
RUN sudo pip3 install cvxopt
RUN sudo pip3 install numpy
RUN sudo pip3 install pulp
# requirements for pulp/glpk
RUN sudo apt-get install glpk-utils libglpk-dev glpk-doc libdsdp-dev libfftw3-dev