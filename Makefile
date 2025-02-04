# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* CMPWeb/*.py

black:
	@black scripts/* CMPWeb/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr CMPWeb-*.dist-info
	@rm -fr CMPWeb.egg-info

install:
	@pip install . -U

all: clean install test black check_code

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#         HEROKU COMMANDS
# ----------------------------------

streamlit:
	-@streamlit run app.py

heroku_login:
	-@heroku login

heroku_upload_public_key:
	-@heroku keys:add ~/.ssh/id_ed25519.pub

heroku_create_app:
	-@heroku create --ssh-git ${APP_NAME}

deploy_heroku:
	-@git push heroku master
	-@heroku ps:scale web=1

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
PYPI_USERNAME=<AUTHOR>
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)

pypi:
	@twine upload dist/* -u $(PYPI_USERNAME)

#----------streamlit-----------
run_streamlit:
	@streamlit run melodywriter.py

#----------docker stuf----------
PROJECT_ID=wagon-bootcamp-342202
DOCKER_IMAGE_NAME=minimozart_web

set_project:
	@gcloud config set project ${PROJECT_ID}

build_container:
	@docker build -t eu.gcr.io/${PROJECT_ID}/${DOCKER_IMAGE_NAME} .

build_push_deploy_container:
	@docker build -t eu.gcr.io/${PROJECT_ID}/${DOCKER_IMAGE_NAME} .
	@docker push eu.gcr.io/${PROJECT_ID}/${DOCKER_IMAGE_NAME}
	@gcloud run deploy --image eu.gcr.io/${PROJECT_ID}/${DOCKER_IMAGE_NAME} --platform managed --region europe-west1
