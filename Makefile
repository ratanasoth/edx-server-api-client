ROOT = $(shell echo "$$PWD")
COVERAGE = $(ROOT)/build/coverage
PACKAGE = edx_api_client

validate: test.requirements test quality

test.requirements:
	pip install -q -r requirements.txt

clean:
	find . -name '*.pyc' -delete
	coverage erase

test: clean
	nosetests --with-coverage --cover-inclusive --cover-branches \
		--cover-html --cover-html-dir=$(COVERAGE)/html/ \
		--cover-xml --cover-xml-file=$(COVERAGE)/coverage.xml \
		--cover-package=$(PACKAGE) $(PACKAGE)/

quality:
	pep8 --config=.pep8 $(PACKAGE)
	pylint --rcfile=.pylintrc $(PACKAGE)
	pep257 --ignore=D100,D203 --match='(?!test).*py' $(PACKAGE)
