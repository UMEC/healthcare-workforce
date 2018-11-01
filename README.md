# healthcare-workforce

A source code repository for UMEC healthcare workforce needs, such as modelling, data transformation and visualization.

## Getting Started - Installing the Application
To install the lastest version:
1. Download [Docker](https://www.docker.com/get-started).
2. Download [this Docker yml file](https://raw.githubusercontent.com/UMEC/healthcare-workforce/master/docker/docker-compose.yml).
3. Open a Docker terminal, change to the directory where you have stored the yml file.
4. Use Docker Compose to start the application via `docker-compose up umec-hw`
5. The application will be available on http://localhost:80/
6. The administration page will be available on http://localhost:5000/api/admin

## Development Documentation
A readme for the UI is available [here](ui/README.md).

A readme for the server is available [here](server/README.md).

A readme for the model is available [here](models/README.md).


## Getting Started - Installing the Application Manually (Developer)
You can make changes to this application. It is built on React (UI), NodeJS (server) and Python (model).
It can be started via the following steps:
1. Download npm
2. `npm install` and `npm start` from the root (this) directory
3. `npm install` and `npm start` from the ui directory
4. Install the python environment as described below
5. The UI application will be available on http://localhost:3000/
6. The server application will be available on http://localhost:5000/

### Python Installation

The analytical model relies upon Python; for simplicity it is best to install a conda environment as this will take care of most of the dependencies.

[Conda Installation](https://conda.io/docs/user-guide/install/index.html)

However the following packages will also need to be installed:
* PuLP (a Linear Program optimization capability)
* GLPK (GNU Linear Programming Kit)

Conveniently these can be installed as part of the conda distribution.

* conda install -c conda-forge pulp
* conda install -c conda-forge glpk

## Contribution Guidelines

1. This project is enabled with Continuous Integration, see [UMEC/healthcare-workforce](https://circleci.com/gh/UMEC/healthcare-workforce). Create a development branch and check your build on CI, before pushing to master.
