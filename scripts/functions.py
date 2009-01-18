def list_text_files():
	Makefile_file = open('../Makefile', 'r')
	for lijst in Makefile_file:
		n = lijst.find("LIJST = ")
		if n == 0:
			break
	Makefile_file.close()
	lijst = lijst.replace("LIJST = ", "")
	lijst = lijst.rstrip()
	return lijst.split(" ")

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

def is_label(env_text):
	n = env_text.find("\\label{")
	if n < 0:
		return 0
	else:
		return 1

def find_label(env_text):
	n = env_text.find("\\label{")
	if n < 0:
		print_where_we_are()
		raise Exception('No label in environment')
	n = n + 6
	m = find_sub_clause(env_text, n)
	label = env_text[n : m + 1]
	return label

def check_defined_notions(def_text):
	n = def_text.find("{\\it ")
	if n < 0:
		print_where_we_are()
		raise Exception('Nothing defined in definition')

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


