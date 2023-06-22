.PHONY: build publish-test install-dev

clean:
	-@rm -dr build dist

install-dev:
	@pip install -r requirements-dev.txt

build:
	@python setup.py sdist
	@python setup.py bdist_wheel

publish-test: clean build
	@twine upload --repository testpypi dist/*

publish: clean build
	@twine upload --repository pypi dist/*