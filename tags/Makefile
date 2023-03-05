# Known suffixes.
.SUFFIXES: .aux .bbl .bib .blg .dvi .htm .html .css .log .out .pdf .ps .tex \
	.toc .foo .bar

# Master list of stems of tex files in the project.
# Should be the same as in the main Makefile
# except that it includes the bibliography
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
	desirables coding obsolete bibliography

# book is a special case
LIJST_TAGS = $(LIJST) fdl index

FOOS = $(patsubst %,%.foo,$(LIJST_TAGS))
BARS = $(patsubst %,%.bar,$(LIJST_TAGS))
PDFS = $(patsubst %,%.pdf,$(LIJST_TAGS))

PDFLATEX := ../latex.sh "pdflatex"

.PHONY: all
all: book.pdf $(PDFS)

# We need the following to cancel the built-in rule for
# dvi files (which uses tex not latex).
%.dvi : %.tex

# Make aux file
%.foo: %.tex
	$(PDFLATEX) $*
	$(PDFLATEX) $*
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

# Make pdf file from others
%.pdf: %.tex %.bar $(FOOS)
	$(PDFLATEX) $*
	$(PDFLATEX) $*
