#! /bin/bash
#
# Write a downloads section to downloads.html.

# Same list as in contents_html.sh.
LIJST=$(grep --max-count=1 LIJST Makefile)
LIJST=$(echo $LIJST | sed 's@LIJST = @@')

cat > downloads.html << "EOF"
<h3><a name="downloads"></a>Downloads</h3>
<table summary="tarball and src" cellspacing="0" cellpadding="0">
<tbody>
<tr><td>Tarball</td><td><a href="stacks-0.2.tar.bz2">stacks-0.2.tar.bz2</a></td></tr>
<tr><td>Source directory</td><td><a href="src">src</a></td></tr>
</tbody>
</table>
<table summary="list of files" cellspacing="0" cellpadding="0">
<tbody>
<tr><td>.pdf</td><td>.ps</td><td>.dvi</td><td>.tex</td></tr>
EOF

for STAM in $LIJST ; do
	echo "<tr>" >> downloads.html
	echo "<td><a href=\"$STAM.pdf\">$STAM.pdf</a></td>" >> downloads.html
	echo "<td><a href=\"$STAM.ps\">$STAM.ps</a></td>" >> downloads.html
	echo "<td><a href=\"$STAM.dvi\">$STAM.dvi</a></td>" >> downloads.html
	echo "<td><a href=\"src/$STAM.tex\">$STAM.tex</a></td>" >> downloads.html
	echo "</tr>" >> downloads.html ;
done

cat >> downloads.html << "EOF"
</tbody>
</table>
</body>
</html>
EOF
