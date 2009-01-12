Makefile_file = open('../Makefile', 'r')
for lijst in Makefile_file:
	n = lijst.find("LIJST = ")
	if n == 0:
		break
Makefile_file.close()
lijst = lijst.replace("LIJST = ", "")
lijst = lijst.rstrip()
lijstje = lijst.split(" ")

def print_where_we_are():
	print "In file " + name + ".tex"
	print "On line", line_nr

def beginning_of_line(pattern, line):
	n = line.find(pattern)
	if n > 0:
		print_where_we_are()
		print n
		print pattern
		print line
		raise Exception('Not at the beginning of the line')
	return

def beginning_of_definition(line):
	n = line.find("\\begin{definition}")
	if n == 0:
		return 1
	else:
		return 0

def end_of_definition(line):
	n = line.find("\\end{definition}")
	if n == 0:
		return 1
	else:
		return 0

def find_sub_clause(text, spot):
	nr_braces = 0
	while nr_braces >= 0:
		spot = spot + 1
		if text[spot] == "{":
			nr_braces = nr_braces + 1
		if text[spot] == "}":
			nr_braces = nr_braces - 1
	return spot

def is_title(line):
	n = line.find("\\title{")
	if n < 0:
		return 0
	else:
		return 1

def find_title(line):
	n = line.find("\\title{")
	if n < 0:
		print_where_we_are()
		raise Exception('No title on line')
	n = n + 6
	m = find_sub_clause(line, n)
	title = line[n : m + 1]
	return title

def print_section_title(line):
	title = find_title(line)
	print
	print "\\medskip\\noindent {\\bf " + title + "}"
	print
	print "\\medskip"
	return

def find_label(env_text):
	n = env_text.find("\\label{")
	if n < 0:
		print_where_we_are()
		raise Exception('No label in environment')
	n = n + 6
	m = find_sub_clause(env_text, n)
	label = env_text[n : m + 1]
	return label

def find_defined_notions(def_text):
	n = def_text.find("{\\it ")
	def_notions = []
	if n < 0:
		print_where_we_are()
		raise Exception('Nothing defined in definition')
	while n >= 0:
		m = find_sub_clause(def_text, n)
		def_notions.append(def_text[n : m + 1])
		n = def_text.find("{\\it ", m)
	return def_notions

def print_def_notions(def_text):
	label = find_label(def_text)
	label = label.lstrip("{")
	label = "{" + name + "-" + label
	def_notions = find_defined_notions(def_text)
	print
	print "\\noindent In \\ref" + label + ": "
	n = len(def_notions)
	m = 0
	while m < n:
		print def_notions[m],
		m = m + 1
		if m < n:
			print ", ",
	print
	return

print "\\input{preamble}"
print "\\begin{document}"
print "\\title{Auto generated index of definitions}"
print "\\maketitle"
print
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
		beginning_of_line("\\begin{", line)
		beginning_of_line("\\end{", line)
		beginning_of_line("$$", line)
		beginning_of_line("\\label{", line)
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
