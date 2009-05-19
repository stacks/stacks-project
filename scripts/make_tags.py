from functions import *

def print_type(type):
	print type[0].capitalize() + type[1:],

path = get_path()

tags = get_tags(path)

labels = all_labels(path)
titles = all_titles(path)


print "\\input{preamble}"
print "\\externaldocument[book-]{book}"
print "\\begin{document}"
print "\\title{Tags}"
print "\\maketitle"
print
print "\\phantomsection"
print "\\label{section-phantom}"
print
print "\\section*{The tag system}"
print "\\label{section-tags}"
print 
print "\\noindent"
print "Each tag refers to a unique lemma, theorem, etc.\ in order for this"
print "project to be referenceable. These tags don't change even if the lemma"
print "(or theorem, etc.) moves within the text. To look up a lemma, theorem"
print "etc.\ using a tag, just go to the page:"
print "\\begin{center}"
print "\\url{http://math.columbia.edu/algebraic_geometry/stacks-git/query}"
print "\\end{center}"
print "and input the tag in the box."
print
print "\\medskip\\noindent"
print "For more information click \hyperref[section-more-tags]{here}."
print "\\vfill\\eject"
print
print "\\section*{More on the tag system}"
print "\\label{section-more-tags}"
print
print "\\noindent"
print "The tag system provides stable references to definitions, lemmas,"
print "propositions, theorems, remarks, examples, exercises, situations and"
print "even equations, sections and items."
print "During development, each of these gets a tag which will always point"
print "to the same mathematical result. The place of the lemma"
print "in the document may change, the lemma may be moved to a different"
print "chapter, but its tag always keeps pointing to it."
print
print "\\medskip\\noindent"
print "This is accomplished in the following manner. There is a file called"
print "tags (in the tags subdirectory) which has on each line the tag followed"
print "by the current full label of the tag. Example:"
print "\\noindent"
print "\\begin{verbatim}"
print "01MB,constructions-lemma-proj-scheme"
print "\\end{verbatim}"
print "\\noindent"
print "Here the tag is 01MB and the full label is"
print "constructions-lemma-proj-scheme."
print "This means that the tag points to a lemma which is in the file"
print "constructions.tex and which currently has the label"
print "lemma-proj-scheme in that file."
print "If we ever change the lemma's label, or move the lemma to a different"
print "file, then we will change the corresponding line in the file tags"
print "by changing the full label correspondingly. But we will never change"
print "the tag."
print
print "\\medskip\\noindent"
print "If it ever turns out that a lemma/proposition/theorem was wrong"
print "then we may remove it from the project. However, we will keep"
print "the corresponding line in the file tags and put in a comment explaining"
print "its dissappearance. For an example see tag 02C0."
print
print "\\medskip\\noindent"
print "New tags are assigned by the maintainer of the project every once in a"
print "while using the python script add\\_tags.py. A tag is a four character"
print "string made up out of digits and capital letters. They are ordered"
print "lexicographically between 0000 and ZZZZ giving 1679616 possible tags."

n = 0
while n < len(tags):
	tag = tags[n][0]
	label = tags[n][1]
	n = n + 1

	print "\\vfill\\eject"
	print
	print "\\medskip\\noindent"
	print "{\\bf TAG: " + tag + "}"
	print
	print "\\medskip\\noindent"
	
	split = split_label(label)
	name = split[0]
	type = split[1]
	short = split[2]

	if not label in labels:
		print "This tag points nowhere."
		print "This may be because the result it pointed to was"
		print "found to be wrong. In any case you can find a"
		print "comment about it in the file tags/tags."
		print "For more on tags click"
		print "\\hyperref[section-tags]{here}."
		continue

	if label in labels and short == "phantom":
		print "Use this tag to refer to a"
		print "\hyperref[" + label + "]{phantom section}{}"
		print "at the beginning of"
		print "``" + titles[name] + "''."
		print "For more on tags click"
		print "\\hyperref[section-tags]{here}."
		continue

	print "Use this tag to reference"
	print_type(split[1])
	print "\\ref{" + label + "} in ``" + titles[name] + "'', or the"
	print "identical"
	print_type(split[1])
	print "\\ref{book-" + label + "} in the corresponding chapter"
	print "of the book version. For more on tags click"
	print "\\hyperref[section-tags]{here}."


print "\\input{chapters}"
print "\\end{document}"

