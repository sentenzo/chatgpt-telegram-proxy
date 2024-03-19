PACKAGE_NAME = chatgpt-telegram-proxy
PROJECT_DIR = oaiapi_teleproxy

CODE = ${PROJECT_DIR} tests openai_connect

# https://stackoverflow.com/a/4511164/2493536
ifdef OS # Windows
   PATH_ARG_SEP=;
else
   ifeq ($(shell uname), Linux) # Linux
	  PATH_ARG_SEP=:
   endif
endif

run:
	poetry run python -m ${PROJECT_DIR}

init:
	poetry install --no-root

export_requirements:
	poetry export --without-hashes -f requirements.txt --output requirements.txt
	poetry export --without-hashes --with dev -f requirements.txt --output requirements.dev.txt

lint:
	poetry run isort ${CODE}
	poetry run black ${CODE}
	poetry run flake8 ${CODE} --count --show-source --statistics
	poetry run mypy ${CODE}

test:
	poetry run pytest -vsx -m "not slow"

test-all:
	poetry run pytest -vsx
