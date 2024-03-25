prepare:
	poetry config virtualenvs.prefer-active-python true
	poetry config virtualenvs.in-project true
	poetry install --no-root

run:
	poetry run streamlit run app.py

check:
	#poetry run vulture ./
	poetry run isort .
	poetry run black .
	poetry run mypy .

build:
	docker build -t docker.io/limulesempai/mlops:1.0 .

push:
	docker push docker.io/limulesempai/mlops:1.0

deploy:
	kubectl apply -f deployment.yaml -n benoit

prometheus:
	@echo "Initializing Prometheus metrics..."
	poetry run streamlit run prometheus_metrics.py
