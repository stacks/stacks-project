#!/bin/bash

# Latex command to use
LATEX=$1

# Stem of latex file
STEM=$2

# Current directory
OLD=${PWD}

# Temporary directory
TMPD=`mktemp -d --tmpdir=../../tmp`

# Symbolically link or copy files to temp dir
# 	Common for both cases
ln -s $OLD/$STEM.bbl $OLD/hyperref.cfg $OLD/$STEM.tex $TMPD
cp $STEM.toc $TMPD

# 	Different
if [ "$STEM" == "book" ]; then
	ln -s $OLD/stacks-project-book.cls $TMPD;
	cp book.aux $TMPD
else
	ln -s $OLD/preamble.tex $OLD/chapters.tex \
		$OLD/stacks-project.cls $TMPD;
	cp *.aux $TMPD
fi

# pdflatex needs .out file
if [ "$LATEX" == "pdflatex" ]; then
	cp $STEM.out $TMPD;
fi

# Latex the file in temporary directory
# Exit without copying the results if there is a latex error.
cd $TMPD
$LATEX $STEM.tex
if [ ! $? == 0 ]; then
	rm -rf $TMPD;
	exit 1;
fi

# Move newly created files back to stacks project directory
mv $STEM.pdf $STEM.dvi $STEM.aux $STEM.toc $STEM.out $STEM.log $OLD

# Remove temporary directory
cd $OLD
rm -rf $TMPD
