# =====================================================================================
#  V A R I A B L E S
DOCKER_COMPOSE_LOCAL=docker-compose.yaml
INGRESS_FILE=k8s-ingress-deloyment.yaml
# =====================================================================================
# D E V  E N V I R O N M E N T  C O M M A N D S
git_hooks:
	docker build -f ./config/Dockerfile.base -t git-hooks:latest .
	docker run -it git-hooks /bin/bash -c "cd /app && pre-commit install"

# ====================================================================================
# D O C K E R  C O M M A N D S

.PHONY: build
build:
	docker-compose -f $(DOCKER_COMPOSE_LOCAL) build

.PHONY: run
run:
	docker-compose -f $(DOCKER_COMPOSE_LOCAL) up

.PHONYY: run_recreate
run_recreate:
	docker-compose -f $(DOCKER_COMPOSE_LOCAL) up --force-recreate

.PHONY: rerun
rerun:
	docker-compose -f $(DOCKER_COMPOSE_LOCAL) down
	docker-compose -f $(DOCKER_COMPOSE_LOCAL) up --build

.PHONY: stop
stop:
	docker-compose -f $(DOCKER_COMPOSE_LOCAL) down

.PHONY: restart
restart:
	docker-compose -f $(DOCKER_COMPOSE_LOCAL) down
	docker-compose -f $(DOCKER_COMPOSE_LOCAL) up

.PHONY: clean
clean:
	docker-compose -f $(DOCKER_COMPOSE_LOCAL) down --volumes --rmi all

.PHONY: run_auth
run_auth:
	docker-compose -f $(DOCKER_COMPOSE_LOCAL) up auth

.PHONY: run_user
run_user:
	docker-compose -f $(DOCKER_COMPOSE_LOCAL) up user

.PHONY: run_issues
run_issues:
	docker-compose -f $(DOCKER_COMPOSE_LOCAL) up issues_management

.PHONY: run_email_daemon
run_email_daemon:
	docker-compose -f $(DOCKER_COMPOSE_LOCAL) up email_daemon

# ====================================================================================
# T E S T I N G  C O M M A N D S

.PHONY: test_auth
test_auth:
	docker-compose -f $(DOCKER_COMPOSE_LOCAL) run --rm auth pytest --cov-report=term-missing --cov=src tests/ -c pytest.ini --cov-fail-under=80

.PHONY: test_user
test_user:
	docker-compose -f $(DOCKER_COMPOSE_LOCAL) run --build --rm user pytest --cov-report=term-missing --cov=src tests/ -c pytest.ini --cov-fail-under=80

.PHONY: test_issues
test_issues:
	docker-compose -f $(DOCKER_COMPOSE_LOCAL) run --rm issues_management pytest --cov-report=term-missing --cov=src tests/ -c pytest.ini --cov-fail-under=80

.PHONY: test_email_daemon
test_email_daemon:
	docker-compose -f $(DOCKER_COMPOSE_LOCAL) run --rm email_daemon pytest --cov-report=term-missing --cov=src tests/ -c pytest.ini --cov-fail-under=80

.PHONY: test_all
test_all: build test_auth test_user test_issues test_email_daemon

.PHONY: load_fixtures
load_fixtures:
	docker-compose -f $(DOCKER_COMPOSE_LOCAL) run --rm auth flask load-fixtures
	docker-compose -f $(DOCKER_COMPOSE_LOCAL) run --rm user flask load-fixtures
	docker-compose -f $(DOCKER_COMPOSE_LOCAL) run --rm issues_management flask load-fixtures

# ====================================================================================
# D E P L O Y M E N T  C O M M A N D S

.PHONY: deploy_services
deploy_services:
	kubectl apply -f deployment/services

.PHONY: deploy_sa
deploy_sa:
	kubectl apply -f deployment/service-accounts

.PHONY: deploy_cert_manager
deploy_certificate:
	kubectl apply -f deployment/k8s-managed-certificate.yaml

.PHONY: deploy_db
deploy_db:
	kubectl apply -f deployment/db

.PHONY: deploy_ingress
deploy_ingress:
	kubectl apply -f deployment/${INGRESS_FILE}

.PHONY: deploy_all
deploy_all: deploy_sa deploy_db deploy_services deploy_certificate deploy_ingress

.PHONY: delete_services
delete_services:
	kubectl delete -f deployment/services

.PHONY: delete_sa
delete_sa:
	kubectl delete -f deployment/service-accounts

.PHONY: delete_cert_manager
delete_certificate:
	kubectl delete -f deployment/k8s-managed-certificate.yaml

.PHONY: delete_db
delete_db:
	kubectl delete -f deployment/db

.PHONY: delete_ingress
delete_ingress:
	kubectl delete -f deployment/${INGRESS_FILE}

.PHONY: delete_all
delete_all: delete_sa delete_db delete_services delete_certificate delete_ingress

.PHONY: describe_cert_manager
describe_cert_manager:
	kubectl describe managedcertificate abcall-cert

# ====================================================================================
# H E L P E R  C O M M A N D S
# ====================================================================================
.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  build               Build the docker images"
	@echo "  run                 Run the docker containers"
	@echo "  rerun               Stop and run the docker containers"
	@echo "  stop                Stop the docker containers"
	@echo "  restart             Restart the docker containers"
	@echo "  clean               Stop and remove the docker containers"
	@echo "  run_auth            Run the auth service"
	@echo "  run_user            Run the user service"
	@echo "  run_issues          Run the issues management service"
	@echo "  run_email_daemon    Run the email daemon service"
	@echo "  test_auth           Run the tests for the auth service"
	@echo "  test_user           Run the tests for the user service"
	@echo "  test_issues         Run the tests for the issues management service"
	@echo "  test_email_daemon   Run the tests for the email daemon service"
	@echo "  test_all            Run the tests for all services"
	@echo "  load_fixtures       Load the fixtures for all services"
	@echo "  deploy_services     Deploy the services"
	@echo "  deploy_sa           Deploy the service accounts"
	@echo "  deploy_cert_manager Deploy the certificate manager"
	@echo "  deploy_db           Deploy the database"
	@echo "  deploy_ingress      Deploy the ingress"
	@echo "  deploy_all          Deploy all resources"
	@echo "  delete_services     Delete the services"
	@echo "  delete_sa           Delete the service accounts"
	@echo "  delete_cert_manager Delete the certificate manager"
	@echo "  delete_db           Delete the database"
	@echo "  delete_ingress      Delete the ingress"
	@echo "  delete_all          Delete all resources"
	@echo "  git_hooks           Install git hooks"
	@echo "  help                Show this help message"
