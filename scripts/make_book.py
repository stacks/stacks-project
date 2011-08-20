from functions import *

# Preamble for the book does not have external references
def print_preamble(path):
	preamble = open(path + "preamble.tex", 'r')
	for line in preamble:
		if line.find("%") == 0:
			continue
		if line.find("externaldocument") >= 0:
			continue
		if line.find("xr-hyper") >= 0:
			continue
		if line.find("\\IfFileExists{") == 0:
			line = line.replace("stacks-project", "stacks-project-book")
		if line.find("\\documentclass") == 0:
			line = line.replace("amsart", "amsbook")
			line = line.replace("stacks-project", "stacks-project-book")
		print line,
	preamble.close()
	return

# Use full labels everywhere in book.tex
def replace_refs(line, name):
	n = 0
	while n < len(list_of_standard_labels):
		text = "\\ref{" + list_of_standard_labels[n] + "-"
		repl = "\\ref{" + name + "-" + list_of_standard_labels[n] + "-"
		line = line.replace(text, repl)
		n = n + 1
	return line

# Chapters unmodified
def print_chapters(path):
	chapters = open(path + "chapters.tex", 'r')
	for line in chapters:
		print line,
	chapters.close()
	return

# Print version and date
def print_version(path):
	from datetime import date
	now = date.today()
	version = git_version(path)
	print "Version " + version + ", compiled on " + now.strftime('%h %d, %Y.')

# Print names contributors
def print_list_contrib(path):
	filename = path + 'CONTRIBUTORS'
	CONTRIBUTORS = open(filename, 'r')
	first = 1
	for line in CONTRIBUTORS:
		if line.find("%") == 0:
			continue
		if len(line.rstrip()) == 0:
			continue
		if first:
			names = line.rstrip()
			first = 0
			continue
		names = names + ", " + line.rstrip()
	CONTRIBUTORS.close()
	names = names + "."
	print names

# Print license blurp
def print_license_blurp(path):
	filename = path + 'introduction.tex'
	introduction = open(filename, 'r')
	inside = 0
	for line in introduction:
		if line.find('\\begin{verbatim}') == 0:
			inside = 1
		if inside == 0:
			continue
		print line,
		if line.find('\\end{verbatim}') == 0:
			inside = 0
	introduction.close()

path = get_path()

print_preamble(path)

print "\\begin{document}"
print "\\begin{titlepage}"
print "\\pagestyle{empty}"
print "\\setcounter{page}{1}"
print "\\centerline{\\LARGE\\bfseries Stacks Project}"
print "\\vskip1in"
print "\\noindent"
print "\\centerline{"
print_version(path)
print "}"
print "\\vskip1in"
print "\\noindent"
print "The following people have contributed to this work:"
print_list_contrib(path)
print "\\end{titlepage}"
print_license_blurp(path)
print "\\tableofcontents"

lijstje = list_text_files(path)
lijstje.append("index")

ext = ".tex"
for name in lijstje:
	if name == "index":
		filename = path + "tmp/index.tex"
	else:
		filename = path + name + ext
	tex_file = open(filename, 'r')
	verbatim = 0
	for line in tex_file:
		verbatim = verbatim + beginning_of_verbatim(line)
		if verbatim:
			if end_of_verbatim(line):
				verbatim = 0
			if name != 'introduction':
				print line,
			continue
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
	print_chapters(path)

print "\\bibliography{my}"
print "\\bibliographystyle{amsalpha}"
print "\\end{document}"
