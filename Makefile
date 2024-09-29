# =====================================================================================
#  V A R I A B L E S

# =====================================================================================
# D E V  E N V I R O N M E N T  C O M M A N D S
git_hooks:
	docker build -f ./config/Dockerfile.base -t git-hooks:latest .
	docker run -it git-hooks /bin/bash -c "cd /app && pre-commit install"

# ====================================================================================
# D O C K E R  C O M M A N D S

.PHONY: build
build:
	docker-compose build --no-cache

.PHONY: build_cache
build_cache:
	docker-compose build

.PHONY: run
run:
	docker-compose up

.PHONYY: run_recreate
run_recreate:
	docker-compose up --force-recreate

.PHONY: down
down:
	docker-compose down

.PHONY: restart
restart:
	docker-compose down
	docker-compose up

.PHONY: clean
clean:
	docker-compose down --volumes --rmi all

.PHONY: run_auth
run_auth:
	docker-compose up auth

.PHONY: re_up
re_up:
	docker-compose down
	docker-compose up --build

# ====================================================================================
# T E S T I N G  C O M M A N D S

.PHONY: test_auth
test_auth:
	docker-compose run auth pytest --cov-report term --cov=src tests/ -c pytest.ini --cov-fail-under=80

.PHONY: test_all
test_all:
	test_auth

# ====================================================================================
# D E P L O Y M E N T  C O M M A N D S
