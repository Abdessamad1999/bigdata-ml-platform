.PHONY: demo test lint docker-build terraform-fmt terraform-validate

demo:
	docker compose up --build

test:
	pytest -q

lint:
	ruff check .

docker-build:
	docker build -t bigdata-ml-platform:local .

terraform-fmt:
	terraform -chdir=infra/terraform fmt -recursive

terraform-validate:
	terraform -chdir=infra/terraform init -backend=false
	terraform -chdir=infra/terraform validate

