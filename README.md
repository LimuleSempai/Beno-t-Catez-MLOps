# Beno-t-Catez-MLOps

- Read the README in the Moodle in Best Practice section
- Initialize a GitHub/GitLab project named {Firstname Lastname MLOps}.
- Set up a pyenv with Python version 3.11.6
- Install Poetry along with required dependencies.
- Develop a data application using Streamlit to display various statitics and graphs based on the Housing.csv file.
- Create a Dockerfile that install dependencies and run the app.
- Write several Make commands :
    - prepare: Initialize the project with dependencies.
    - run: Run the data app
    - check: Verify formating of the python files with the commands:
        - vulture
        - isort
        - black
        - mypy
    - build: Build the docker image
    - push: push the image
    - deploy: deploy the image
- Add a prometheus client in the project with at least one counter that increment each time we push a specific button
- Create a deployment file for the app



# MLOps

## Pyenv

[Pyenv](https://github.com/pyenv/pyenv) allows developers of a given project to use the same Python version in an attempt of maintaining a reproducible environment including the Python version in an automated manner. You can obtain the latest version using this command. It is highly recommended to visit the project's homepage for more information.

```shell
curl https://pyenv.run | bash
```

Set the wanted python version and install it:
```shell
echo "3.11.6" > .python-version
pyenv install
```

Add the following lines to your ~/.bashrc or ~/.zshrc to initialize pyenv by default.

```shell
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

With a new terminal the command:
```bash
which python
```
Should return
```bash
~/.pyenv/shims/python
```

## Poetry

[Poetry](https://github.com/python-poetry/poetry) helps you declare, manage and install dependencies of Python projects, ensuring you have the right stack everywhere.

```shell
curl -sSL https://install.python-poetry.org | python3 -
```

Check if poetry is installed and with the correct version.

```shell
poetry --version
# If poetry is not recognized then you should investigate your $PATH variable.
export PATH="$PATH:$HOME/.poetry/bin"
```

Now to use the poetry environment (for example with streamlit for example):
```bash
poetry run streamlit run app.py
```

Export the dependencies to be use in a docker file for example:
```bash
poetry export -f requirements.txt --without-hashes --output requirements.txt
```

Here an example of a `pyproject.toml` file
```toml
[tool.poetry]
name = "projet-name"
version = "0.1.0"
description = "Project description."
authors = ["Firstname Lastname <mail>"]

[tool.poetry.dependencies] # Direct prod dependencies
python = ">=3.11,<3.12"
streamlit = "~1"
pandas = "~2"

[tool.poetry.dev-dependencies] # Develop dependencies
coverage = "~7" # Allow to know the part of code covered
black = "~23" # Code formatting
isort = "~5" # Import sort
mypy = "~1" # Type checking
pytest = "~7" # For unit tests
vulture = "~2" # Check dead code
git-cliff = "~1" # Git commit formatting
```

Now to setup the project and install dependencies run these commands:
```bash
poetry config virtualenvs.prefer-active-python true # Use actual python env (here pyenv)
poetry config virtualenvs.in-project true # Generate dependencies in a .venv folder in the project
poetry install --no-root # Install dependencies (without the actual project)
```

You can add a dependencies by adding it in the file with the correct version and use the command `poetry update` or you can use the command `poetry add {LIB}` that will add it in the file with the correct version and install it.

## Makefile

Makefiles are commonly used in software development to automate the build process and ensure that the software is built consistently and efficiently. They can be used for a wide range of tasks, including compiling code, generating documentation, running tests, and deploying software.

Here an example of a `Makefile` for our use case:

```Makefile
prepare:
    poetry config virtualenvs.prefer-active-python true
    poetry config virtualenvs.in-project true
    poetry install --no-root
```
Just run `make prepare` and it will execute each listed commands

## Docker
Docker is a platform designed to help developers build, share, and run container applications.
[Here](https://docs.docker.com/reference/dockerfile/) for more information about how to build a simple Dockerfile

```shell
# To connect to the docker registry
docker login -u "USERNAME" -p "PASSWORD" docker.io
docker build -t docker.io/{USER}/{NAME}:{VERSION} .
docker push ${DOCKER_IMG}
```

Do not forget to copy `requirements.txt`

## Prometheus
Prometheus collects and stores its metrics as time series data, i.e. metrics information is stored with the timestamp at which it was recorded, alongside optional key-value pairs called labels. [Here](https://prometheus.io/docs/introduction/overview/) for more information.

We will use the library `prometheus-client`. An example:
```python
from typing import Optional

import streamlit as st
from prometheus_client import REGISTRY, Counter, start_http_server
from prometheus_client.registry import Collector


@st.cache_resource # It is important to add a cache for streamlit to not load several time the metric server
def init_metrics():
    start_http_server(9090)
    # The counter will create 2 metrics. Here page_loaded_total and page_loaded_created
    # page_loaded_total is the value of the counter
    # page_loaded_created is the unix time of the creation of the counter (https://en.wikipedia.org/wiki/Unix_time)
    Counter("page_loaded", "Number of times the data app is loaded", registry=REGISTRY)
    # TODO: Declare metrics

def get_metric(metric_name: str) -> Optional[Collector]:
    return REGISTRY._names_to_collectors.get(metric_name, None)


def get_metric_value(metric_name: str) -> Optional[float]:
    return REGISTRY.get_sample_value(metric_name)

get_metric("page_loaded").inc()
st.write(get_metric_value("page_loaded_total"))
```

To see the metric locally, go to the url `localhost:9090` after running the app.

## Kubernetes deployment
Here an example of a simple `deployment.yaml` file:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: projet-example-deployment # Tbe deployment name
  namespace: enzo # The namespace of where the deployment will be done
  labels:
    app: projet-example-app # A label to regroup diffent resources
spec:
  replicas: 1 # Number of pods that will be created 
  selector:
    matchLabels:
      app: projet-example-app
  template:
    metadata:
      labels:
        app: projet-example-app
    spec:
      containers:
      - name: projet-example # The name of pods
        image: docker.io/{USER}/{NAME}:{VERSION} # Docker image that will be pulled and used
        imagePullPolicy: Always # This tell the deployment if we want to pull image every time a pod is created
        ports:
        - containerPort: 8501 # The port of the app
          name: http # 
```

Run this command to deploy the app:
```bash
kubectl apply -f deployment.yaml -n {NAMESPACE}
```