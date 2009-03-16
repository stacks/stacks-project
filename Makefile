# Known suffixes.
.SUFFIXES: .aux .bbl .bib .blg .dvi .htm .html .css .log .out .pdf .ps .tex \
	.toc .funny

# Master list of stems of tex files in the project.
# This should be in order.
LIJST = introduction conventions sets categories topology sheaves algebra \
	sites homology simplicial modules injectives cohomology hypercovering \
	schemes constructions properties morphisms limits varieties \
	topologies groupoids fpqc-descent etale spaces stacks \
	stacks-groupoids algebraic flat exercises desirables coding

# Add index and fdl to get index and license latexed as well.
LIJST_FDL = $(LIJST) fdl index

# Different extensions.
PDFS = $(patsubst %,%.pdf,$(LIJST_FDL))
DVIS = $(patsubst %,%.dvi,$(LIJST_FDL))
FUNNYS = $(patsubst %,%.funny,$(LIJST_FDL))
AUXS = $(patsubst %,%.aux,$(LIJST))

# Files in INSTALLDIR will be overwritten.
INSTALLDIR=/home/dejong/html/algebraic_geometry/stacks-git

# Change this into pdflatex if you want the default target to produce pdf
LATEX=latex

# Currently the default target runs latex once for each updated tex file.
# This is what you want if you are just editing a single tex file and want
# to look at the resulting dvi file. It does latex the license of the index.
# We use the aux file to keep track of whether the tex file has been updated.
.PHONY: default
default: $(AUXS)
	@echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	@echo "% This target latexs each updated tex file just once. %"
	@echo "% See the file documentation/make-project for others. %"
	@echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"

%.aux: %.tex
	$(LATEX) -src $<

# Target which creates all dvi files of chapters
.PHONY: dvis
dvis: $(DVIS)

# Target which creates all pdf files of chapters
.PHONY: pdfs
pdfs: $(PDFS)

# We need the following to cancel the built-in rule for
# dvi files (which uses tex not latex).
%.dvi : %.tex

# Automatically generated tex files
tmp/index.tex: *.tex
	python ./scripts/make_index.py $(PWD) > tmp/index.tex

tmp/book.tex: *.tex tmp/index.tex
	python ./scripts/make_book.py $(PWD) > tmp/book.tex

# fld.funny is different because there is no bibliography
# nor is there a table of contents...
fdl.funny: fdl.tex
	latex fdl.tex
	touch fdl.funny

# index.funny is different too.
index.funny: tmp/index.tex
	latex tmp/index.tex
	touch index.funny

# book.funny is different too.
book.funny: tmp/book.tex
	latex tmp/book.tex
	bibtex book
	latex tmp/book.tex
	touch book.funny

# Funny target to prepare %.aux, %.toc and %.bbl.
# The latex command creates %.aux and %.toc,
# the bibtex command creates %.bbl, and finally
# the touch command creates %.funny with a newer
# modification time then any of %.dvi, %.aux, %.toc,
# %.bbl, %.blg, %.log and %.out.
%.funny: %.tex
	latex $<
	bibtex $*
	latex $<
	touch $@

# Pdf file creation
# index.pdf is different
index.pdf: tmp/index.tex $(FUNNYS)
	pdflatex tmp/index.tex
	pdflatex tmp/index.tex

# book.pdf is different
book.pdf: tmp/book.tex book.funny
	pdflatex tmp/book.tex
	pdflatex tmp/book.tex

# Generic rule
%.pdf: %.tex $(FUNNYS)
	pdflatex $<
	pdflatex $<

# Dvi file creation
# index.dvi is different
index.dvi: tmp/index.tex $(FUNNYS)
	latex tmp/index.tex
	latex tmp/index.tex

# book.dvi is different
book.dvi: tmp/book.tex book.funny
	latex tmp/book.tex
	latex tmp/book.tex

# Generic rule
%.dvi : %.tex $(FUNNYS)
	latex $<
	latex -src $<

.PHONY: book
book: book.dvi book.pdf

.PHONY: clean
clean:
	rm -f *.aux *.bbl *.blg *.dvi *.log *.pdf *.ps *.out *.toc *.html \
		*.funny
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
	cat .git/refs/heads/master > $(INSTALLDIR)/VERSION
