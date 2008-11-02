# Known suffixes.
.SUFFIXES: .aux .bbl .bib .blg .dvi .html .log .out .pdf .ps .tex .toc .funny

# Master list of stems of tex files in the project.
# This should be in order.
LIJST = introduction conventions sets categories topology sheaves algebra sites homology injectives simplicial schemes etale spaces stacks stacks-groupoids algebraic flat desirables hypercovering coding

# Add fdl to get license latexed as well.
LIJST_FDL = $(LIJST) fdl

# Different extensions.
PDFS = $(patsubst %,%.pdf,$(LIJST_FDL))
DVIS = $(patsubst %,%.dvi,$(LIJST_FDL))
PSS = $(patsubst %,%.ps,$(LIJST_FDL))
FUNNYS = $(patsubst %,%.funny,$(LIJST_FDL))
HTMLS = stacks.html contents.html downloads.html

# Files in INSTALLDIR will be overwritten.
INSTALLDIR=/home/dejong/html/algebraic_geometry/stacks-git

# Make all the funny targets first so crossreferences work.
.PHONY: all
all: $(FUNNYS) $(DVIS)

.PHONY: pdfs
pdfs: $(FUNNYS) $(PDFS)

# We need the following to cancel the built-in rule for
# .dvi files (which uses tex not latex).
%.dvi : %.tex

# fld.funny is different because there is no bibliography
# nor is there a table of contents...
fdl.funny : fdl.tex
	echo "latex fdl.tex" >> logfile.log
	latex fdl.tex
	echo "touch fdl.funny" >> logfile.log
	touch fdl.funny

# Other .pdf files do have bibliographies and
# table of contents. But running make file.pdf
# will not correctly insert external crossreferences
# if the other .aux files aren't up to date.
%.pdf : %.tex %.funny
	echo "2x pdflatex $<" >> logfile.log
	pdflatex $<
	pdflatex $<

%.dvi : %.tex %.funny
	echo "2x latex $<" >> logfile.log
	latex $<
	latex -src $<

# Funny target to prepare %.aux, %.toc and %.bbl.
# The latex command creates %.aux and %.toc,
# the bibtex command creates %.bbl, and finally
# the touch command creates %.funny with a newer
# modification time then any of %.dvi, %.aux, %.toc,
# %.bbl, %.blg, %.log and %.out. Actually the modification
# time resolution is not good enough so we remove %.dvi.
%.funny: %.tex
	echo "latex $<" >> logfile.log
	latex $<
	echo "bibtex $*" >> logfile.log
	bibtex $*
	echo "rm $*.dvi" >> logfile.log
	rm $*.dvi
	echo "touch $@" >> logfile.log
	touch $@

.PHONY: clean
clean:
	rm -f *.aux *.bbl *.blg *.dvi *.log *.pdf *.ps *.out *.toc *.html *.funny

.PHONY: backup
backup: clean
	cd .. ; tar -cjvf stacks-git.tar.bz2 stacks-git/

# The script scripts/name_html.sh creates name.html in src directory.
# We do not want an index.html in src! So we concatenate these into
# $(INSTALLDIR)/index.html in the install target.
#
# FIXME: For contents.html We should really do some sanity checking to
# see if the .toc files are up to date.
%.html:
	echo "./scripts/$*_html.sh" >> logfile.log
	./scripts/$*_html.sh

.PHONY: install
install: $(FUNNYS) $(PDFS) $(DVIS)
	cp *.tex *.pdf *.dvi $(INSTALLDIR)
	cp COPYING CONTRIBUTORS my.bib Makefile $(INSTALLDIR)
