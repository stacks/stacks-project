#! /bin/bash
#
# This script makes a list of contents of the pdf 
# files in the project and puts them in a file
# called "contents.html".
#
# Horrible, terrible, no good, very bad script!
#
# Translation (for variable names used):
# Dutch		English
# --------------------------
# LIJST		LIST
# ANTWOORD	ANSWER
# STAM		STEM
# TITEL		TITLE
# UIT		OUT
# REGEL		LINE
# AANTAL	NUMBER
# TELLER	COUNTER
# LAATSTE	LAST
# DIEPTE	DEPTH
# TEXT		TEXT
#
# Script returns 0 on succes and 1 on failure.

# Start.
cat > contents.html << "EOF"
<h3><a name="contents"></a>Table of contents</h3>
<!-- This is added automatically by running make in src -->
<dl>
EOF
DIEPTE=1

# LIJST is the list of STEMS of .toc files in the order in which you want it
# to appear on the web-site. Do not include fdl.
LIJST=$(grep --max-count=1 LIJST Makefile)
LIJST=$(echo $LIJST | sed 's@LIJST = @@')
TELLER=0

for STAM in $LIJST; do
	if [ ! -f $STAM.toc ]; then
		echo "File $STAM.toc does not exist. Stop."
		exit 1;
	fi
	TELLER=$(($TELLER+1))
# The following assumes that in the .tex file you have
# garbage title{Actual title} garbage
# all on one line, the first one of its kind.
	TITEL=$(grep --max-count=1 '\\title{.*}' $STAM.tex)
	TITEL=$(echo $TITEL | sed 's@^.*title{@@' | sed 's@}.*$@@')
	echo "<dt>$TELLER. <a href=\"$STAM.pdf\">$TITEL</a></dt>" >> contents.html
	AANTAL_REGELS=$(sed -n '$=' $STAM.toc)
	sed -e 's@\\contentsline @@' \
		-e 's@{\\toc[a-z]* @@' \
		-e 's@}}{@}{@' $STAM.toc > tmp/uit
	for (( REGEL=1 ; 1+AANTAL_REGELS-REGEL ; REGEL=REGEL+1 )) ; do
		REGEL_TEXT=$(sed '2,$ d' tmp/uit)
		sed -i -e '1 d' tmp/uit
# OK, this is horrible and slow.
NAAM=$(echo $REGEL_TEXT | sed 's@\({[^}{]*}\)\({[^}{]*}\)\({[^}{]*}\)\({[^}{]*}\)\({[^}{]*}\)\({[^}{]*}\)@\4@' | sed 's@{@@g' | sed 's@}@@g' | sed 's@\$@@g')
LABEL=$(echo $REGEL_TEXT | sed 's@\({[^}{]*}\)\({[^}{]*}\)\({[^}{]*}\)\({[^}{]*}\)\({[^}{]*}\)\({[^}{]*}\)@\6@' | sed 's@{@@g' | sed 's@}@@g' | sed 's@\$@@g')
NUMBER=$(echo $REGEL_TEXT | sed 's@\({[^}{]*}\)\({[^}{]*}\)\({[^}{]*}\)\({[^}{]*}\)\({[^}{]*}\)\({[^}{]*}\)@\3@' | sed 's@{@@g' | sed 's@}@@g' | sed 's@\$@@g')
# Debug.
# echo naam---$NAAM---label---$LABEL---number---$NUMBER---
		LAATSTE=$(echo $NUMBER | sed 's@.*\.@@')
# Debug.
# echo ---$LAATSTE---
		if [ " $LAATSTE" = " 1" ]; then
			echo "<dd><dl>" >> contents.html
			echo "<dt>$TELLER.$NUMBER. <a href=\"$STAM.pdf#$LABEL\">$NAAM</a></dt>" >> contents.html
			DIEPTE=$(($DIEPTE+1)) ;
		else
			AANTAL_PUNTEN=$(echo ".$NUMBER" | sed 's@[^\.]@@g' | wc -c)
			while [ $AANTAL_PUNTEN -lt $DIEPTE ]; do
				DIEPTE=$(($DIEPTE-1))
				echo "</dl></dd>" >> contents.html ;
			done
			if [ " $NAAM" = " References" ]; then
				echo "<dt>$TELLER. <a href=\"$STAM.pdf#$LABEL\">References</a></dt>" >> contents.html ;
			else
				echo "<dt>$TELLER.$NUMBER. <a href=\"$STAM.pdf#$LABEL\">$NAAM</a></dt>" >> contents.html
			fi ;
		fi ;
	done
	while [ 1 -lt $DIEPTE ]; do
		DIEPTE=$(($DIEPTE-1))
		echo "</dl></dd>" >> contents.html ;
	done 
done
TELLER=$(($TELLER+1))
echo "<dt>$TELLER. <a href=\"fdl.pdf\">GNU Free Documentation License</a></dt>" >> contents.html
echo "</dl>" >> contents.html

# Clean up.
rm tmp/uit
