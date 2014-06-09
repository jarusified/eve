RM	= rm -f
PYTHON	= python

all: test

test::
	$(PYTHON) dumper.py extract.pdf
	$(PYTHON) extractor.py extract.pdf extract.txt
	$(PYTHON) fontfilter.py extract.pdf
	$(PYTHON) image_extractor.py extract.pdf
	$(PYTHON) image_resources.py extract.pdf
	$(PYTHON) tetml.py extract.pdf extract.tetml

test-python2: test
	$(PYTHON) glyphinfo.py extract.pdf extract.info.txt

test-python3: test
	$(PYTHON) glyphinfo.py extract.pdf extract.info.txt

#clean::
#	$(RM) extract.pdf dumper.txt extract.txt fontfilter.txt
#	$(RM) extract.tetml extract*.tif attachments.txt m.out
#	$(RM) extract.info.txt
