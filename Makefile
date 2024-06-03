# Known suffixes.
.SUFFIXES: .aux .bbl .bib .blg .dvi .htm .html .css .log .out .pdf .ps .tex \
	.toc .foo .bar

# Master list of stems of tex files in the project.
# This should be in order.
LIJST = introduction conventions sets categories \
	topology sheaves sites stacks \
	fields algebra brauer \
	homology derived simplicial \
	more-algebra smoothing \
	modules sites-modules \
	injectives cohomology sites-cohomology dga dpa sdga hypercovering \
	schemes constructions properties morphisms coherent divisors limits \
	varieties topologies descent perfect more-morphisms flat groupoids \
	more-groupoids etale \
	chow intersection pic weil \
	adequate dualizing duality discriminant derham local-cohomology \
	algebraization curves resolve models functors equiv \
	pione etale-cohomology \
	crystalline proetale relative-cycles more-etale trace \
	spaces spaces-properties spaces-morphisms decent-spaces \
	spaces-cohomology spaces-limits spaces-divisors spaces-over-fields \
	spaces-topologies \
	spaces-descent spaces-perfect spaces-more-morphisms \
	spaces-flat spaces-groupoids spaces-more-groupoids bootstrap \
	spaces-pushouts spaces-chow \
	groupoids-quotients spaces-more-cohomology spaces-simplicial \
	spaces-duality formal-spaces restricted spaces-resolve \
	formal-defos defos cotangent examples-defos \
	algebraic examples-stacks stacks-sheaves criteria artin quot \
	stacks-properties stacks-morphisms stacks-limits \
	stacks-cohomology stacks-perfect \
	stacks-introduction stacks-more-morphisms stacks-geometry \
	moduli moduli-curves \
	examples exercises guide \
	desirables coding obsolete

# Add index and fdl to get index and license latexed as well.
LIJST_FDL = $(LIJST) fdl index

# Add book to get all stems of tex files needed for tags
LIJST_TAGS = $(LIJST_FDL) book

# Different extensions
SOURCES = $(patsubst %,%.tex,$(LIJST))
TAGS = $(patsubst %,tags/tmp/%.tex,$(LIJST_TAGS))
TAG_EXTRAS = tags/tmp/my.bib tags/tmp/hyperref.cfg \
	tags/tmp/stacks-project.cls tags/tmp/stacks-project-book.cls \
	tags/tmp/Makefile tags/tmp/chapters.tex \
	tags/tmp/preamble.tex tags/tmp/bibliography.tex
FOO_SOURCES = $(patsubst %,%.foo,$(LIJST))
FOOS = $(patsubst %,%.foo,$(LIJST_FDL))
BARS = $(patsubst %,%.bar,$(LIJST_FDL))
PDFS = $(patsubst %,%.pdf,$(LIJST_FDL))
DVIS = $(patsubst %,%.dvi,$(LIJST_FDL))

# Be careful. Files in INSTALLDIR will be overwritten!
INSTALLDIR=

# Default latex commands
LATEX := latex -src
#LATEX := ./scripts/latex.sh "$(CURDIR)" "latex -src"

PDFLATEX := pdflatex
#PDFLATEX := ./scripts/latex.sh "$(CURDIR)" pdflatex

FOO_LATEX := $(LATEX)
#FOO_LATEX := $(PDFLATEX)

# Currently the default target runs latex once for each updated tex file.
# This is what you want if you are just editing a single tex file and want
# to look at the resulting dvi file. It does latex the license of the index.
# We use the aux file to keep track of whether the tex file has been updated.
.PHONY: default
default: $(FOO_SOURCES)
	@echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	@echo "% This target latexs each updated tex file just once. %"
	@echo "% See the file documentation/make-project for others. %"
	@echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"

# Target which creates all dvi files of chapters
.PHONY: dvis
dvis: $(FOOS) $(BARS) $(DVIS)

# Target which creates all pdf files of chapters
.PHONY: pdfs
pdfs: $(FOOS) $(BARS) $(PDFS)

# We need the following to cancel the built-in rule for
# dvi files (which uses tex not latex).
%.dvi : %.tex

# Automatically generated tex files
tmp/index.tex: *.tex
	python3 ./scripts/make_index.py "$(CURDIR)" > tmp/index.tex

tmp/book.tex: *.tex tmp/index.tex
	python3 ./scripts/make_book.py "$(CURDIR)" > tmp/book.tex

# Creating aux files
index.foo: tmp/index.tex
	$(FOO_LATEX) tmp/index
	touch index.foo

book.foo: tmp/book.tex
	$(FOO_LATEX) tmp/book
	touch book.foo

%.foo: %.tex
	$(FOO_LATEX) $*
	touch $*.foo

# Creating bbl files
index.bar: tmp/index.tex index.foo
	@echo "Do not need to bibtex index.tex"
	touch index.bar

fdl.bar: fdl.tex fdl.foo
	@echo "Do not need to bibtex fdl.tex"
	touch fdl.bar

book.bar: tmp/book.tex book.foo
	bibtex book
	touch book.bar

%.bar: %.tex %.foo
	bibtex $*
	touch $*.bar

# Creating pdf files
index.pdf: tmp/index.tex index.bar $(FOOS)
	$(PDFLATEX) tmp/index
	$(PDFLATEX) tmp/index

book.pdf: tmp/book.tex book.bar
	$(PDFLATEX) tmp/book
	$(PDFLATEX) tmp/book

%.pdf: %.tex %.bar $(FOOS)
	$(PDFLATEX) $*
	$(PDFLATEX) $*

# Creating dvi files
index.dvi: tmp/index.tex index.bar $(FOOS)
	$(LATEX) tmp/index
	$(LATEX) tmp/index

book.dvi: tmp/book.tex book.bar
	$(LATEX) tmp/book
	$(LATEX) tmp/book

%.dvi : %.tex %.bar $(FOOS)
	$(LATEX) $*
	$(LATEX) $*

#
#
# Tags stuff
#
#
tags/tmp/book.tex: tmp/book.tex tags/tags
	python3 ./scripts/tag_up.py "$(CURDIR)" book > tags/tmp/book.tex

tags/tmp/index.tex: tmp/index.tex
	cp tmp/index.tex tags/tmp/index.tex

tags/tmp/preamble.tex: preamble.tex tags/tags
	python3 ./scripts/tag_up.py "$(CURDIR)" preamble > tags/tmp/preamble.tex

tags/tmp/chapters.tex: chapters.tex
	cp chapters.tex tags/tmp/chapters.tex

tags/tmp/%.tex: %.tex tags/tags
	python3 ./scripts/tag_up.py "$(CURDIR)" $* > tags/tmp/$*.tex

tags/tmp/stacks-project.cls: stacks-project.cls
	cp stacks-project.cls tags/tmp/stacks-project.cls

tags/tmp/stacks-project-book.cls: stacks-project-book.cls
	cp stacks-project-book.cls tags/tmp/stacks-project-book.cls

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
	$(MAKE) -C tags/tmp

.PHONY: tags_install
tags_install: tags tarball
ifndef INSTALLDIR
	@echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	@echo "% Set INSTALLDIR value in the Makefile!               %"
	@echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
else
	cp tags/tmp/*.pdf $(INSTALLDIR)
	tar -c -f $(INSTALLDIR)/stacks-pdfs.tar --exclude book.pdf --transform=s@tags/tmp@stacks-pdfs@ tags/tmp/*.pdf
	git archive --format=tar HEAD | (cd $(INSTALLDIR) && tar xf -)
	cp stacks-project.tar.bz2 $(INSTALLDIR)
	git log --pretty=oneline -1 > $(INSTALLDIR)/VERSION
endif

.PHONY: tags_clean
tags_clean:
	rm -f tags/tmp/*
	rm -f tmp/book.tex tmp/index.tex
	rm -f stacks-project.tar.bz2

# Additional targets
.PHONY: book
book: book.foo book.bar book.dvi book.pdf

.PHONY: clean
clean:
	rm -f *.aux *.bbl *.blg *.dvi *.log *.pdf *.ps *.out *.toc *.foo *.bar
	rm -f tmp/book.tex tmp/index.tex
	rm -f stacks-project.tar.bz2

.PHONY: distclean
distclean: clean tags_clean

.PHONY: backup
backup:
	git archive --prefix=stacks-project/ HEAD | bzip2 > \
		../stacks-project_backup.tar.bz2

.PHONY: tarball
tarball:
	git archive --prefix=stacks-project/ HEAD | bzip2 > stacks-project.tar.bz2

# Target which makes all dvis and all pdfs, as well as the tarball
.PHONY: all
all: dvis pdfs book tarball

.PHONY: install
install:
	@echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	@echo "% To install the project, use the tags_install target %"
	@echo "% Be sure to change INSTALLDIR value in the Makefile! %"
	@echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"

WEBDIR=../WEB
.PHONY: web
web: tmp/index.tex
	@echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	@echo "% Stuff in WEBDIR will be overwritten!!!!!!!!!        %"
	@echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	cp my.bib $(WEBDIR)/my.bib
	cp tags/tags $(WEBDIR)/tags
	python3 ./scripts/web_book.py "$(CURDIR)" > $(WEBDIR)/book.tex
