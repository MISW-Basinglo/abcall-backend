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

.PHONY: deploy_ingress
deploy_ingress:
	kubectl apply -f deployment/${INGRESS_FILE}
