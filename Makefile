
clean: clean-docs
	

clean-docs:
	rm -fr docs/

docs:
	rm -fr htmldocs/
	sphinx-build -b html src docs/
	open docs/index.html
