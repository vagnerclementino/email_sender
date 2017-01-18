HOST=127.0.0.1
TEST_PATH=./
SRC_DIR=$(shell pwd) 

help:
	@echo "    clean"
	@echo "        Remove python artifacts."
	@echo "    clean-build"
	@echo "        Remove build artifacts."
	@echo "    isort"
	@echo "        Sort import statements."
	@echo "    lint"
	@echo "        Check style with flake8."
	@echo "    test"
	@echo "        Run py.test"
	@echo '    run'
	@echo '        Run the `my_project` service on your local machine.'
	@echo '    docker-run'
	@echo '        Build and run the `my_project` service in a Docker container.'

clean:
	@find . -name '*.pyc' -exec rm --force {} +
	@find . -name '*.pyo' -exec rm --force {} +
	@find . -name '*~' -exec rm --force  {} +
	@echo 'Arquivos removidos com sucesso'

isort:
	sh -c "isort --skip-glob=.tox --recursive . "

lint:
	flake8 --exclude=.tox

test: clean-pyc
	py.test --verbose --color=yes $(TEST_PATH)

run:
	@python email_sender.py docs/email_template.html

deploy: clean
	@echo "Copiando de " $(SRC_DIR)
	@rsync -arPvzh --exclude={'.*','*.log','*con.py'} -e 'ssh -i /run/media/vagner/Dados/Vagner/Dropbox/AWS/keys/aws-s01-dev-key.pem' $(pwd) ec2-52-67-130-34.sa-east-1.compute.amazonaws.com:/home/vagner/projects






.PHONY: clean
