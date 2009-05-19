# Known suffixes.
.SUFFIXES: .aux .bbl .bib .blg .dvi .htm .html .css .log .out .pdf .ps .tex \
	.toc

# Master list of stems of tex files in the project.
# This should be in order.
LIJST = introduction conventions sets categories topology sheaves algebra \
	sites homology simplicial modules injectives cohomology \
	sites-cohomology hypercovering schemes constructions properties \
	morphisms divisors coherent limits varieties topologies groupoids \
	fpqc-descent etale spaces stacks stacks-groupoids algebraic flat \
	examples exercises desirables coding

# Add index and fdl to get index and license latexed as well.
LIJST_FDL = $(LIJST) index fdl

# Add book and long to get all stems of tex files needed for tags
LIJST_TAGS = $(LIJST_FDL) book long

# Different extensions
SOURCES = $(patsubst %,%.tex,$(LIJST))
TEXS = $(SOURCES) tmp/index.tex fdl.tex
TAGS = $(patsubst %,tags/tmp/%.tex,$(LIJST_TAGS))
TAG_EXTRAS = tags/tmp/my.bib tags/tmp/hyperref.cfg tags/tmp/amsart.cls \
	tags/tmp/amsbook.cls tags/tmp/Makefile tags/tmp/chapters.tex \
	tags/tmp/preamble.tex
AUX_SOURCES = $(patsubst %,%.aux,$(LIJST))
AUXS = $(patsubst %,%.aux,$(LIJST_FDL))
BBLS = $(patsubst %,%.bbl,$(LIJST_FDL))
PDFS = $(patsubst %,%.pdf,$(LIJST_FDL))
DVIS = $(patsubst %,%.dvi,$(LIJST_FDL))

# Files in INSTALLDIR will be overwritten.
INSTALLDIR=/home/dejong/html/algebraic_geometry/stacks-git

# Change this into pdflatex if you want the default target to produce pdf
LATEX=latex -src

# Currently the default target runs latex once for each updated tex file.
# This is what you want if you are just editing a single tex file and want
# to look at the resulting dvi file. It does latex the license of the index.
# We use the aux file to keep track of whether the tex file has been updated.
.PHONY: default
default: $(AUX_SOURCES)
	@echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	@echo "% This target latexs each updated tex file just once. %"
	@echo "% See the file documentation/make-project for others. %"
	@echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"

# Target which creates all dvi files of chapters
.PHONY: dvis
dvis: $(AUXS) $(BBLS) $(DVIS)

# Target which creates all pdf files of chapters
.PHONY: pdfs
pdfs: $(AUXS) $(BBLS) $(PDFS)

# We need the following to cancel the built-in rule for
# dvi files (which uses tex not latex).
%.dvi : %.tex

# Automatically generated tex files
tmp/index.tex: *.tex
	python ./scripts/make_index.py $(PWD) > tmp/index.tex

tmp/book.tex: *.tex tmp/index.tex
	python ./scripts/make_book.py $(PWD) > tmp/book.tex

# Creating aux files
index.aux: tmp/index.tex
	$(LATEX) tmp/index.tex

book.aux: tmp/book.tex
	$(LATEX) tmp/book.tex

%.aux: %.tex
	$(LATEX) $<

# Creating bbl files
index.bbl: tmp/index.tex index.aux
	@echo "Do not need to bibtex index.tex"
	touch index.bbl

fdl.bbl: fdl.tex fdl.aux
	@echo "Do not need to bibtex fdl.tex"
	touch fdl.bbl

book.bbl: tmp/book.tex book.aux
	bibtex book

%.bbl: %.tex %.aux
	bibtex $*

# Creating pdf files
index.pdf: tmp/index.tex index.aux index.bbl
	pdflatex tmp/index.tex
	pdflatex tmp/index.tex

book.pdf: tmp/book.tex book.aux book.bbl
	pdflatex tmp/book.tex
	pdflatex tmp/book.tex

%.pdf: %.tex %.bbl $(AUXS)
	pdflatex $<
	pdflatex $<

# Creating dvi files
index.dvi: tmp/index.tex index.aux index.bbl
	latex tmp/index.tex
	latex tmp/index.tex

book.dvi: tmp/book.tex book.aux book.bbl
	latex tmp/book.tex
	latex tmp/book.tex

%.dvi : %.tex %.bbl $(AUXS)
	latex -src $<
	latex -src $<

#
#
# Tags stuff
#
#
tags/tmp/book.tex: tmp/book.tex
	python ./scripts/tag_up.py $(PWD) book > tags/tmp/book.tex
	patch -i tags/book.patch tags/tmp/book.tex

tags/tmp/index.tex: tmp/index.tex
	cp tmp/index.tex tags/tmp/index.tex

tags/tmp/long.tex: tags/tags
	python ./scripts/make_tags.py $(PWD) > tags/tmp/long.tex

tags/tmp/preamble.tex: preamble.tex
	cp preamble.tex tags/tmp/preamble.tex
	patch -i tags/preamble.patch tags/tmp/preamble.tex

tags/tmp/chapters.tex: chapters.tex
	cp chapters.tex tags/tmp/chapters.tex

tags/tmp/%.tex: %.tex
	python ./scripts/tag_up.py $(PWD) $* > tags/tmp/$*.tex

tags/tmp/amsart.cls: amsart.cls
	cp amsart.cls tags/tmp/amsart.cls

tags/tmp/amsbook.cls: amsbook.cls
	cp amsbook.cls tags/tmp/amsbook.cls

tags/tmp/hyperref.cfg: hyperref.cfg
	cp hyperref.cfg tags/tmp/hyperref.cfg

tags/tmp/my.bib: my.bib
	cp my.bib tags/tmp/my.bib

tags/tmp/Makefile: tags/Makefile
	cp tags/Makefile tags/tmp/Makefile

# Target dealing with tags
.PHONY: tags
tags: $(TAGS) $(TAG_EXTRAS)
	@echo "TAGS TARGET"
	make -C tags/tmp

# Additional targets
.PHONY: book
book: book.dvi book.pdf

.PHONY: clean
clean:
	rm -f *.aux *.bbl *.blg *.dvi *.log *.pdf *.ps *.out *.toc *.html
	rm -f tmp/book.tex tmp/index.tex
	rm -f stacks-git.tar.bz2

.PHONY: backup
backup:
	git archive --prefix=stacks-git/ HEAD | bzip2 > \
		../stacks-git_backup.tar.bz2

.PHONY: tarball
tarball:
	git archive --prefix=stacks-git/ HEAD | bzip2 > stacks-git.tar.bz2

# Target which forces everything to rebuild in the correct order to
# make sure crossreferences work when installing
.PHONY: all
all: dvis pdfs book tarball

.PHONY: install
install: all
	git archive --format=tar HEAD | (cd $(INSTALLDIR) && tar xf -)
	cp *.pdf *.dvi $(INSTALLDIR)
	cp stacks-git.htm $(INSTALLDIR)/index.html
	mv stacks-git.tar.bz2 $(INSTALLDIR)
	git log --pretty=oneline -1 > $(INSTALLDIR)/VERSION
