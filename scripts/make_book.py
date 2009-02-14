from functions import *

def print_chapter_title(line):
	title = find_title(line)
	print
	print "\\chapter{" + title + "}"
	print
	return

def print_preamble():
	preamble = open("../preamble.tex", 'r')
	for line in preamble:
		if line.find("%") == 0:
			continue
		if line.find("externaldocument") >= 0:
			continue
		if line.find("xr-hyper") >= 0:
			continue
		if line.find("\\documentclass") == 0:
			line = line.replace("amsart", "amsbook")
		print line,
	preamble.close()
	return

def replace_refs(line, name):
	line = line.replace("\\ref{lemma-", "\\ref{" + name + "-lemma-")
	line = line.replace("\\ref{proposition-", "\\ref{" + name + "-proposition-")
	line = line.replace("\\ref{theorem-", "\\ref{" + name + "-theorem-")
	line = line.replace("\\ref{remark-", "\\ref{" + name + "-remark-")
	line = line.replace("\\ref{remarks-", "\\ref{" + name + "-remarks-")
	line = line.replace("\\ref{example-", "\\ref{" + name + "-example-")
	line = line.replace("\\ref{exercise-", "\\ref{" + name + "-exercise-")
	line = line.replace("\\ref{situation-", "\\ref{" + name + "-situation-")
	line = line.replace("\\ref{equation-", "\\ref{" + name + "-equation-")
	line = line.replace("\\ref{definition-", "\\ref{" + name + "-definition-")
	line = line.replace("\\ref{section-", "\\ref{" + name + "-section-")
	line = line.replace("\\ref{item-", "\\ref{" + name + "-item-")
	return line

print_preamble()

print "\\begin{document}"
print "\\title{Stacks project}"
print "\\maketitle"
print "\\tableofcontents"

lijstje = list_text_files()

path = "../"
ext = ".tex"
for name in lijstje:
	filename = path + name + ext
	tex_file = open(filename, 'r')

	for line in tex_file:
		if line.find("\\input{preamble}") == 0:
			continue
		if line.find("\\begin{document}") == 0:
			continue
		if line.find("\\title{") == 0:
			line = line.replace("\\title{", "\\chapter{")
		if line.find("\\maketitle") == 0:
			continue
		if line.find("\\tableofcontents") == 0:
			continue
		if line.find("\\input{chapters}") == 0:
			continue
		if line.find("\\bibliography") == 0:
			continue
		if line.find("\\end{document}") == 0:
			continue
		if is_label(line):
			text = "\\label{" + name + "-"
			line = line.replace("\\label{", text)
		if contains_ref(line):
			line = replace_refs(line, name)
		print line,

	tex_file.close()

print "\\bibliography{my}"
print "\\bibliographystyle{alpha}"
print "\\end{document}"
