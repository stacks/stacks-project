# Known suffixes.
.SUFFIXES: .aux .bbl .bib .blg .dvi .htm .html .css .log .out .pdf .ps .tex \
	.toc .foo .bar


# Master list of stems of tex files in the project.
# Should be the same as in the main Makefile
LIJST = introduction conventions sets categories topology sheaves algebra \
	sites homology simplicial modules injectives cohomology \
	sites-cohomology hypercovering schemes constructions properties \
	morphisms coherent divisors limits varieties chow topologies \
	groupoids fpqc-descent more-morphisms etale spaces stacks \
	stacks-groupoids algebraic flat examples exercises desirables coding

LIJST_TAGS = $(LIJST) index fdl book

AUXS = $(patsubst %,%.aux,$(LIJST_TAGS))
FOOS = $(patsubst %,%.foo,$(LIJST_TAGS))
BBLS = $(patsubst %,%.bbl,$(LIJST_TAGS))
BARS = $(patsubst %,%.bar,$(LIJST_TAGS))
DVIS = $(patsubst %,%.dvi,$(LIJST_TAGS))
PDFS = $(patsubst %,%.pdf,$(LIJST_TAGS))

all: $(FOOS) $(BARS) $(DVIS) $(PDFS)

# We need the following to cancel the built-in rule for
# dvi files (which uses tex not latex).
%.dvi : %.tex

# Make aux file from tex file
%.foo: %.tex
	latex $<
	latex $<
	touch $*.foo

# These do not get bibtexed
index.bar:
	touch index.bar

fdl.bar:
	touch fdl.bar

# Make bbl file from aux file
%.bar: %.foo
	bibtex $*
	touch $*.bar

# Make dvi from others
%.dvi : %.tex %.bar $(FOOS)
	latex $<
	latex $<

# Make pdf file from others
%.pdf: %.tex %.bar $(FOOS)
	pdflatex $<
	pdflatex $<
