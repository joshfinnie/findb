.DEFAULT_GOAL := test

test:
	pytest -v --cov=findb --cov-report term-missing

dtest:
	docker build -t findb-test .
	docker run findb make test
