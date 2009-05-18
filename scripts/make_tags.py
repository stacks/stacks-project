from functions import *

def print_type(type):
	print type[0].capitalize() + type[1:],

path = get_path()

tags = get_tags(path)

labels = all_labels(path)

print "\\input{preamble}"
print "\\begin{document}"
print "\\title{Tags}"
print "\\maketitle"
print
print "\\phantomsection"
print "\\label{section-phantom}"
print
print "\\section{The tag system}"
print
print "\\noindent"
print "The tag system provides stable references to definitions, lemmas,"
print "propositions, theorems, remarks, examples, exercises, situations and"
print "even equations, sections and items."
print "During development, each of these gets a tag which will always point"
print "to the same, mathematically speaking, result. The place of the lemma"
print "in the document may change, the lemma may be moved to a different"
print "chapter, but its tag always keeps pointing to it."
print
print "\\medskip\\noindent"
print "This is accomplished in the following manner. There is a file called"
print "tags in the tags subdirectory which has on each line the tag followed"
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
print "its dissappearance. For example see tag 02C0."
print
print "\\medskip\\noindent"
print "New tags are assigned by the maintainer of the project every once in a"
print "while using the python script add\\_tags.py. A tag is a four character"
print "string made up out of digits and capital letters. They are ordered"
print "lexicographically between 0000 and ZZZZ giving 1679616 possible tags."
print
print "\\medskip\\noindent"
print "The purpose of the document you are reading now is to be a human"
print "readable version of the tags file with hyperlinks from the each"
print "tag to the corresponding spot in the project. It will serve as a kind"
print "of dictionary between tags and mathematical results in the project."

n = 0
while n < len(tags):
	print "\\vfill\\eject"
	print
	print "\\medskip\\noindent"
	print "TAG: " + tags[n][0]
	print
	print "\\medskip\\noindent"
	
	if check_ref(tags[n][1], labels):
		print "This tag points to"
		split = split_label(tags[n][1])
		print_type(split[1])
		print "\\ref*{" + tags[n][1] + "}"
		print "in the chapter"
	else:
		print "This tag points nowhere."
		print "This may be because the result it pointed to was"
		print "found to be wrong. In any case you can find a"
		print "comment about it in the file tags/tags."
	n = n + 1

print "\\input{chapters}"
print "\\end{document}"

