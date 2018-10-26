# healthcare-workforce

A source code repository for UMEC healthcare workforce needs, such as modelling, data transformation and visualization.

## Documentation
A readme for the UI is available [here](ui/README.md).
A readme for the server is available [here](server/README.md).
A readme for the model is available [here](models/README.md).

## Getting Started - Running the Application
This application is built on React (UI), NodeJS (server) and Python (model).
It can be started via the following steps:
1. Download npm
2. `npm install` and `npm start` from the root (this) directory
3. `npm install` and `npm start` from the ui directory
4. Install the python environment as described below
5. The application will be available on http://localhost:3000/

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
