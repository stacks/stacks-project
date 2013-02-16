# Known suffixes.
.SUFFIXES: .aux .bbl .bib .blg .dvi .htm .html .css .log .out .pdf .ps .tex \
	.toc .foo .bar

# Master list of stems of tex files in the project.
# Should be the same as in the main Makefile
# except that it includes the bibliography
LIJST = introduction conventions sets categories topology sheaves algebra \
	brauer sites homology derived more-algebra smoothing \
	simplicial modules sites-modules injectives cohomology \
	sites-cohomology hypercovering schemes constructions properties \
	morphisms coherent divisors limits varieties chow topologies \
	descent perfect adequate more-morphisms flat groupoids \
	more-groupoids etale \
	etale-cohomology crystalline spaces spaces-properties \
	spaces-morphisms decent-spaces spaces-cohomology \
	spaces-limits spaces-divisors \
	spaces-topologies spaces-descent spaces-perfect \
	spaces-more-morphisms \
	spaces-over-fields stacks formal-defos defos \
	spaces-groupoids spaces-more-groupoids bootstrap examples-stacks \
	groupoids-quotients algebraic stacks-sheaves criteria artin quot \
	stacks-properties stacks-morphisms stacks-cohomology \
	stacks-introduction examples exercises guide desirables coding \
	obsolete bibliography

# book is a special case
LIJST_TAGS = $(LIJST) fdl index

FOOS = $(patsubst %,%.foo,$(LIJST_TAGS))
BARS = $(patsubst %,%.bar,$(LIJST_TAGS))
DVIS = $(patsubst %,%.dvi,$(LIJST_TAGS))
PDFS = $(patsubst %,%.pdf,$(LIJST_TAGS))

LATEX := ../latex.sh "latex"
PDFLATEX := ../latex.sh "pdflatex"

.PHONY: all
all: book.dvi book.pdf $(DVIS) $(PDFS)

# We need the following to cancel the built-in rule for
# dvi files (which uses tex not latex).
%.dvi : %.tex

# Make aux file
%.foo: %.tex
	$(LATEX) $*
	$(LATEX) $*
	touch $*.foo

# These do not get bibtexed
index.bar:
	touch index.bar

fdl.bar:
	touch fdl.bar

# Make bbl file
%.bar: %.foo
	bibtex $*
	touch $*.bar

# Make dvi
%.dvi : %.tex %.bar $(FOOS)
	$(LATEX) $*
	$(LATEX) $*

# Make pdf file from others
%.pdf: %.tex %.bar $(FOOS)
	$(PDFLATEX) $*
	$(PDFLATEX) $*
