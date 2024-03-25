prepare:
	poetry config virtualenvs.prefer-active-python true
	poetry config virtualenvs.in-project true
	poetry install --no-root

run:
	poetry run streamlit run app.py

check:
	poetry run vulture ./
	poetry run isort .
	poetry run black .
	poetry run mypy .

build:
	docker build -t docker.io/limulesempai/mlops:1.0 .

push:
	docker push docker.io/limulesempai/mlops:1.0

deploy:
	# Here you would typically deploy the Docker image to your chosen environment
	# For example, Kubernetes, Docker Swarm, AWS ECS, etc.
