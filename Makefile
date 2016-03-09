all: clean check-manifest viewdoc
clean:
	if [ -e .long-description.html ]; then rm .long-description.html ; fi
check-manifest:
	check-manifest
viewdoc:
	viewdoc
release:
	#python setup.py register -r pypitest
	#python setup.py sdist upload -r pypitest
	python setup.py register -r pypi
	python setup.py sdist upload -r pypi
