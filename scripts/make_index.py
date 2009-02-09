from functions import *

def print_section_title(line):
	title = find_title(line)
	print
	print "\\medskip\\noindent"
	print "{\\bf " + title + "}"
	print
	print "\\medskip"
	return

def print_def_notions(def_text):
	label = find_label(def_text)
	label = label.lstrip("{")
	label = "{" + name + "-" + label
	def_notions = find_defined_notions(def_text)
	print
	print "\\noindent"
	print "In \\ref" + label + ": "
	n = len(def_notions)
	m = 0
	while m < n:
		if m + 1 < n:
			print def_notions[m] + ","
		else:
			print def_notions[m]
		m = m + 1
	print
	return

lijstje = list_text_files()

print "\\input{preamble}"
print "\\begin{document}"
print "\\title{Auto generated index of definitions}"
print "\\maketitle"
print
print "\\frenchspacing"
print "\\begin{multicols}{2}"
path = "../"
ext = ".tex"
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
			print_section_title(line)
		if in_definition == 1:
			def_text = def_text + " " + line.rstrip()
			nr_lines_def = nr_lines_def + 1
			if end_of_definition(line) == 1:
				in_definition = 0
				print_def_notions(def_text)
		else:
			in_definition = beginning_of_definition(line)
			if in_definition == 1:
				nr_lines_def = 1
				def_text = line.rstrip()

	tex_file.close()
print "\\end{multicols}"
print "\\input{chapters}"
print "\\end{document}"
