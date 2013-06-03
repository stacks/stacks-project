#!/bin/bash

# This script makes some assumptions that only apply to the stacks project.
# But if you know how to read this script then it should be fairly easy to
# figure out what they are and adapt them to your specific case.

# Stacks Project Directory
SPD=$1

# Latex command to use
LATEX=$2

# Stem of latex file
STEM=$3

# Temporary directory
TMPD=`mktemp -d --tmpdir=$SPD/tmp`

# Symbolically link files that are hopefully not modified during process
ln -s $SPD/preamble.tex $SPD/chapters.tex $SPD/hyperref.cfg \
	$SPD/stacks-project.cls $SPD/$STEM.tex $TMPD

# Exceptional cases
if [ "$STEM" == "tmp/index" ]; then STEM="index"; fi
if [ "$STEM" == "tmp/book" ]; then
	STEM="book";
	ln -s $SPD/stacks-project-book.cls $TMPD;
fi

# Link to bibliography file
ln -s $SPD/$STEM.bbl $TMPD

# Copy working files
cp *.aux $TMPD
cp $STEM.toc $TMPD

# Latex the file in temporary directory
cd $TMPD
$LATEX $STEM.tex

# Move newly created files back to stacks project directoy
mv $STEM.pdf $STEM.dvi $STEM.aux $STEM.toc $STEM.out $STEM.log $SPD

# Remove temporary directory
cd $SPD
rm -r $TMPD
