
clean: clean-docs
	

clean-docs:
	rm -fr docs/

docs:	FORCE
	rm -fr docs/
	sphinx-build -b html src docs/
	touch docs/.nojekyll
	open docs/index.html

FORCE:
