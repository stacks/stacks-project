from functions import *

def print_section_title(title):
	print("")
	print("\\medskip\\noindent")
	print("{\\bf " + title + "}")
	print("")
	print("\\medskip")
	return

def print_def_terms(label, def_terms):
	print("")
	print("\\noindent")
	print("In \\ref{" + label + "}: ")
	n = len(def_terms)
	m = 0
	while m < n:
		if m + 1 < n:
			print(def_terms[m] + ",")
		else:
			print(def_terms[m])
		m = m + 1
	print("")
	return

def add_def_terms(terms, label, def_terms):
	n = 0
	while n < len(def_terms):
		terms.append([def_terms[n], label])
		n = n + 1
	return

def add_defs(defs, label, def_terms):
	defs.append([def_terms, label])
	return

def find_name(name, label):
	if label.find(name + "-definition") == 0:
		return 1
	else:
		return 0

path = get_path()
lijstje = list_text_files(path)
ext = ".tex"
terms = []
defs = []
titles = []
for name in lijstje:
	filename = path + name + ext
	tex_file = open(filename, 'r')
	in_definition = 0
	nr_lines_def = 0
	line_nr = 0
	have_title = 0
	def_text = ""
	for line in tex_file:
		line_nr = line_nr + 1
		if not have_title and is_title(line):
			have_title = 1
			titles.append(find_title(line))
		if in_definition == 1:
			def_text = def_text + " " + line.rstrip()
			nr_lines_def = nr_lines_def + 1
			if end_of_definition(line) == 1:
				in_definition = 0
				label = find_label(def_text)
				label = name + "-" + label
				def_terms = find_defined_terms(def_text)
				add_def_terms(terms, label, def_terms)
				add_defs(defs, label, def_terms)
		else:
			in_definition = beginning_of_definition(line)
			if in_definition == 1:
				nr_lines_def = 1
				def_text = line.rstrip()

	tex_file.close()


print("\\input{preamble}")
print("\\begin{document}")
print("\\title{Auto generated index}")
print("\\maketitle")
print()
print("\\phantomsection")
print("\\label{section-phantom}")
print()
print("\\tableofcontents")
print()
print("\\frenchspacing")
print()
print()
print("\\begin{multicols}{2}[\\section{Alphabetized definitions}\\label{section-alphabetized}]")
terms.sort(key=lambda x: x[0].lower())
n = 0
while n < len(terms):
	print("\\noindent")
	print(terms[n][0])
	print("in \\ref{" + terms[n][1] + "}")
	print()
	n = n + 1
print("\\end{multicols}")
print()
print("\\begin{multicols}{2}[\\section{Definitions listed per chapter}\\label{section-per-chapter}]")
n = 0
m = 0
for name in lijstje:
	print_section_title(titles[m])
	m = m + 1
	while n < len(defs) and find_name(name, defs[n][1]):
		print_def_terms(defs[n][1], defs[n][0])
		n = n + 1

print("\\end{multicols}")
print()
print("\\input{chapters}")
print("\\end{document}")
