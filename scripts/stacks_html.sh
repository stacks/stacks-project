#! /bin/bash
#
# Trivial script that copies verbatim into stacks.html.
#

cat > stacks.html << "EOF"
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
<head>
<style type="text/css">
table { padding:8px 0px; }
th { padding:0px 5px; text-align:left; }
td { padding:0px 5px; vertical-align:top; }
</style>
<title>Web-based algebraic stacks project</title>
</head>
<body>
<h1>Web-based algebraic stacks project</h1>
<p>The idea of this web-site is that there is a place for open
development of mathematics next to the current scientific model.
For more information on how this is supposed to work, please see
the general discussion on the
<a href="http://www.math.columbia.edu/mailman/listinfo/algebraic_geometry">
algebraic_geometry mailing list</a>
and its 
<a href="http://www.math.columbia.edu/pipermail/algebraic_geometry">
archives</a>.</p>
<p>The documents on this website are published under the
<a href="http://www.gnu.org/licenses/fdl.html">
GFDL</a>.</p>
<h2><a name="stacks"></a>Algebraic Stacks</h2>
<p>This is the first project started on the open source model in algebraic
geometry. Its aim is mainly to explain and elucidate how to work with
algebraic stacks in algebraic geometry. We will provide proofs of all
results, apart from some basic facts from algebra, set theory, sheaf
theory. Sometimes we will avoid stating (and proving) a result in its
utmost generality to avoid the project getting too large. Sometimes as well
we will use an advanced result that has a good exposition in the
mathematical literature, however, in general we try to avoid this.</p>
<p>To contribute please start reading the documents in this
project (see below). Feel free to point out typos, mistakes on the <a href=
"http://www.math.columbia.edu/mailman/listinfo/algebraic_geometry"
>mailing list</a> (a ``stacks'' mailing list will be instituted later). 
The .tex files are in the <a href="src">source directory</a>. Feel 
free to edit and send ``patches'' and/or new files to the mailing
list. The section <a href="#downloads">Downloads</a> below has a list
of downloads in different formats.</p>
EOF
