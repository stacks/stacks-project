Makefile_file = open('/home/johan/OpenSourceMath/stacks-git/Makefile', 'r')

for lijst in Makefile_file:
	n = lijst.find("LIJST")
	if n == 0:
		break

Makefile_file.close()

lijst = lijst.replace("LIJST = ", "")
lijst = lijst.rstrip()
lijstje = lijst.split(" ")

def beginning_of_line(pattern, line):
	n = line.find(pattern)
	if n > 0:
		print n
		print pattern
		print line
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
	title = ""

	if n < 0:
		raise Exception('No title on line')

	n = n + 6

	m = find_sub_clause(line, n)

	title = line[n : m + 1]
	
	return title


def find_label(environment_text, stem):
	n = environment_text.find("\\label{")
	label = ""
	m = n + 7
	nr_braces = 0
	while nr_braces >= 0:
		if environment_text[m] == "{":
			nr_braces = nr_braces + 1
		if environment_text[m] == "}":
			nr_braces = nr_braces - 1
		label = label + environment_text[m]
		m = m + 1

	label = label.rstrip("}")

	return label

def find_defined_notions(def_text):
	n = def_text.find("{\\it ")
	def_notions = []

	if n < 0:
		print "In file " + name + ".tex"
		print "On line ",
		print line_nr
		raise Exception('Nothing defined in definition')

	while n >= 0:
		m = find_sub_clause(def_text, n)
		def_notions.append(def_text[n : m + 1])
		n = def_text.find("{\\it ", m)

	return def_notions


path = "/home/johan/OpenSourceMath/stacks-git/"
ext = ".tex"

for name in lijstje:
	filename = path + name + ext
	tex_file = open(filename, 'r')
	in_definition = 0
	nr_lines_def = 0
	line_nr = 0
	def_text = ""

	for line in tex_file:
		line_nr = line_nr + 1
		beginning_of_line("\\begin{", line)
		beginning_of_line("\\end{", line)
		beginning_of_line("$$", line)
		beginning_of_line("\\label{", line)

		if is_title(line):
			print find_title(line)

		if in_definition == 1:
			def_text = def_text + " " + line.rstrip()
			nr_lines_def = nr_lines_def + 1
			if end_of_definition(line) == 1:
				in_definition = 0
				find_defined_notions(def_text)
		else:
			in_definition = beginning_of_definition(line)
			if in_definition == 1:
				nr_lines_def = 1
				def_text = line.rstrip()

	tex_file.close()
