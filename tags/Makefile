# Known suffixes.
.SUFFIXES: .aux .bbl .bib .blg .dvi .htm .html .css .log .out .pdf .ps .tex \
	.toc .foo .bar


# Master list of stems of tex files in the project.
# Should be the same as in the main Makefile
LIJST = introduction conventions sets categories topology sheaves algebra \
	sites homology simplicial modules sites-modules injectives cohomology \
	sites-cohomology hypercovering schemes constructions properties \
	morphisms coherent divisors limits varieties chow topologies \
	descent more-morphisms groupoids more-groupoids etale \
	etale-cohomology spaces spaces-properties spaces-morphisms \
	spaces-topologies spaces-descent spaces-more-morphisms stacks \
	spaces-groupoids spaces-more-groupoids bootstrap examples-stacks \
	groupoids-quotients algebraic stacks-properties examples exercises \
	guide desirables coding

LIJST_TAGS = $(LIJST) fdl index book

FOOS = $(patsubst %,%.foo,$(LIJST_TAGS))
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
