EDITOR =	emacs
PYTHON =	/usr/bin/python2.2

.PHONY:	all clean test run editor doc dist distclean site

# Build the tests and documentation
all:	doc test

# Clean everything
clean:	distclean
	$(MAKE) -C doc/ clean

# Run the unittests
test:	
	PYTHONPATH=src $(PYTHON) scripts/test.py

# Run the shell
run:
	clear
	PYTHONPATH=src $(PYTHON) scripts/psyche

# Build the documentation
doc:
	$(MAKE) -C doc/

# Useful for starting emacs :)
editor:
	find src doc -name \*py -or -name \*tex | xargs $(EDITOR) &


# Since first time online == 0.4.0
changelog:
	cvs2cl --prune --log-opts '-d"2002-08-04<" ' \
		src/psyche doc scripts/psyche*
	@rm -f ChangeLog.bak


# Cleaning all garbage so it's fit for distribution
distclean:
	@find . -name '*.pyc' | xargs rm -f
	@find . -name '*.pyo' | xargs rm -f
	@find . -name '*~' | xargs rm -f
	@rm -rf build/ dist/ MANIFEST site/
	$(MAKE) -C doc/ distclean


# Creating the distributions
dist:	doc distclean changelog
	$(PYTHON) setup.py build
	$(PYTHON) setup.py sdist --formats=gztar,zip
	$(PYTHON) setup.py bdist 



# Creates the manual directory and the archives
sitedist:	all distclean changelog
	@rm -rf site
	@mkdir site

	echo Creating distribution
	@$(PYTHON) setup.py sdist --formats=gztar,zip > /dev/null

	echo Copying distributions
	@cp dist/* site/

	echo Copying documentation
	@mkdir -p site/doc/manual
	@cp doc/manual/*.* site/doc/manual
	@cp doc/manual.pdf site/doc


# Creates the required DocBook for downloading
site:	XML = site/psyche_download.xml
	TAR = $(wildcard site/*tar.gz)
	TARSIZE = $(shell ls -sh $(TAR) | cut -d' ' -f1)
	TARHASH = $(shell gpg --print-md md5 $(TAR) | cut -d':' -f2)
	TARNAME = $(shell echo $(TAR) | cut -d'/' -f2)
	ZIP = $(wildcard site/*zip)
	ZIPSIZE = $(shell ls -sh $(ZIP) | cut -d' ' -f1)
	ZIPHASH = $(shell gpg --print-md md5 $(ZIP) | cut -d':' -f2)
	ZIPNAME = $(shell echo $(ZIP) | cut -d'/' -f2)



site:	sitedist
	@echo Creating download text
	@echo $(XML)
	@echo "<variablelist>" > $(XML)
	@echo " <varlistentry>" >> $(XML)
	@echo "  <term>Linux</term>" >> $(XML)
	@echo "  <listitem>" >> $(XML)
	@echo "  <para>" >> $(XML)
	@echo "  <ulink url=\"../psyche/$(TARNAME)\">$(TARNAME)</ulink>"\
	      >>$(XML)
	@echo "  ($(TARSIZE))" >> $(XML)
	@echo "  </para>" >>$(XML)
	@echo "  <para>" >> $(XML)
	@echo "	 MD5: <literal>$(TARHASH)</literal>" >> $(XML)
	@echo "  </para>" >> $(XML)
	@echo "  </listitem>" >> $(XML)
	@echo " </varlistentry>" >> $(XML)
	@echo " <varlistentry>" >> $(XML)
	@echo "  <term>Windows</term>" >> $(XML)
	@echo "  <listitem>" >> $(XML)
	@echo "  <para>" >> $(XML)
	@echo "  <ulink url=\"../psyche/$(ZIPNAME)\">$(ZIPNAME)</ulink>"\
	      >>$(XML)
	@echo "  ($(ZIPSIZE))" >> $(XML)
	@echo "  </para>" >>$(XML)
	@echo "  <para>" >> $(XML)
	@echo "	 MD5: <literal>$(ZIPHASH)</literal>" >> $(XML)
	@echo "  </para>" >> $(XML)
	@echo "  </listitem>" >> $(XML)
	@echo " </varlistentry>" >> $(XML)
	@echo "</variablelist>" >> $(XML)


