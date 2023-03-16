run:
	source ./venv/bin/activate && uvicorn --reload --log-config logging_dev.conf services_backend.routes.base:app

configure: venv
	source ./venv/bin/activate && pip install -r requirements.dev.txt -r requirements.txt

venv:
	python3.11 -m venv venv

format:
	autoflake -r --in-place --remove-all-unused-imports ./services_backend
	isort ./services_backend
	black ./services_backend

db:
	docker run -d -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust --name db-services-backend postgres:15

migrate:
	alembic upgrade head
