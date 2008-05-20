#! /bin/bash
#
# Use this script to change all the preambles in all tex files simultaneously.
# 

function change_file ()
{
	FILE=$@
	sed -i -e 's@\\usepackage{hyperref}@\\usepackage\[colorlinks=true\]{hyperref}@' $FILE
}

LIJST=`ls *.tex`

for BESTAND in $LIJST; do
	# The file fdl.tex has a different preamble.
	if [ ! $BESTAND = "fdl.tex" ]; then
		change_file $BESTAND ;
	fi ;
done
