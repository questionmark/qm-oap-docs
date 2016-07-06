
clean: clean-docs
	

clean-docs:
	rm -fr htmldocs/

docs:
	rm -fr htmldocs/
	sphinx-build -b html doc htmldocs/
	open htmldocs/index.html
