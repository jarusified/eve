RM	= rm -f
PYTHON	= python

all: test

test::
	$(PYTHON) src/question.py  'what are zone rules and what are the 4 effects affecting them '
	$(PYTHON) src/dumper.py data/extract.pdf
	$(PYTHON) src/extractor.py data/extract.pdf output/extract.txt
	$(PYTHON) src/fontfilter.py data/extract.pdf
	$(PYTHON) src/image_extractor.py data/extract.pdf
	$(PYTHON) src/image_resources.py data/extract.pdf
	$(PYTHON) src/tetml.py data/extract.pdf output/extract.tetml
	$(PYTHON) src/answers.py 
test-python2: test
	$(PYTHON) src/glyphinfo.py data/extract.pdf output/extract.info.txt

test-python3: test
	$(PYTHON) src/glyphinfo.py data/extract.pdf output/extract.info.txt

#clean::
#	$(RM) extract.pdf dumper.txt extract.txt fontfilter.txt
#	$(RM) extract.tetml extract*.tif attachments.txt m.out
#	$(RM) extract.info.txt
