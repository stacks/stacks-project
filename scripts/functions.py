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

def print_error(error_text, line, name, line_nr):
	print "In file " + name + ".tex"
	print "On line", line_nr
	print "Line: " + line.rstrip()
	print "Error: " + error_text
	print
#	raise Exception(error_text)

def length_of_line(line):
	n = len(line)
	if n > 81:
		return "More than 80 characters on a line."
	return ""

def beginning_of_line(pattern, line):
	n = line.find(pattern)
	if n > 0:
		print_where_we_are()
		print n
		print pattern
		print line
		raise Exception('Not at the beginning of the line')
	return

def only_on_line(pattern, spot, line):
	line = line.rstrip()
	n = line.find(pattern)
	if n > 0:
		return "Pattern: " + pattern + "not at the start of the line."
	if n == 0:
		m = find_sub_clause(line, spot, "{", "}")
		m = rest_clauses(line, m)
		if not m + 1 == len(line):
			return "Pattern: " + pattern + "*} not only on the line."
	return ""

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

def beginning_of_proof(line):
	n = line.find("\\begin{proof}")
	if n == 0:
		return 1
	else:
		return 0

def end_of_proof(line):
	n = line.find("\\end{proof}")
	if n == 0:
		return 1
	else:
		return 0

def rest_clauses(text, spot):
	n = next_clause(text, spot)
	while n > spot:
		spot = n
		n = next_clause(text, spot)
	return n

def next_clause(text, spot):
	open = ""
	if spot + 1 == len(text):
		return spot
	if text[spot + 1] == "[":
		open = "["
		close = "]"
	if text[spot + 1] == "{":
		open = "{"
		close = "}"
	if open:
		spot = find_sub_clause(text, spot + 1, open, close)
	return spot

def find_sub_clause(text, spot, open, close):
	nr_braces = 0
	while nr_braces >= 0:
		spot = spot + 1
		if text[spot] == open:
			nr_braces = nr_braces + 1
		if text[spot] == close:
			nr_braces = nr_braces - 1
	return spot

def check_double_dollar(line):
	n = line.find("$$")
	if n < 0:
		return ""
	if n > 0:
		return "Double dollar not at start of line."
	line = line.rstrip()
	if not len(line) == 2:
		return "Double dollar not by itself on line."

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
	m = find_sub_clause(line, n, "{", "}")
	title = line[n : m + 1]
	return title

def is_label(env_text):
	n = env_text.find("\\label{")
	if n < 0:
		return 0
	else:
		return 1

def contains_ref(line):
	n = line.find("\\ref{")
	if n < 0:
		return 0
	else:
		return 1

def find_label(env_text):
	n = env_text.find("\\label{")
	if n < 0:
		return ""
	n = n + 6
	m = find_sub_clause(env_text, n, "{", "}")
	label = env_text[n : m + 1]
	return label

def standard_label(ref):
	n = ref.find("{lemma-")
	if n >= 0:
		return 1
	n = ref.find("{proposition-")
	if n >= 0:
		return 1
	n = ref.find("{theorem-")
	if n >= 0:
		return 1
	n = ref.find("{remark-")
	if n >= 0:
		return 1
	n = ref.find("{remarks-")
	if n >= 0:
		return 1
	n = ref.find("{example-")
	if n >= 0:
		return 1
	n = ref.find("{exercise-")
	if n >= 0:
		return 1
	n = ref.find("{situation-")
	if n >= 0:
		return 1
	n = ref.find("{equation-")
	if n >= 0:
		return 1
	n = ref.find("{definition-")
	if n >= 0:
		return 1
	n = ref.find("{section-")
	if n >= 0:
		return 1
	n = ref.find("{item-")
	if n >= 0:
		return 1
	return 0

def find_refs(line, name):
	refs = []
	n = line.find("\\ref{")
	while n >= 0:
		m = find_sub_clause(line, n + 4, "{", "}")
		ref = line[n + 4: m + 1]
		if standard_label(ref):
			ref = ref.lstrip("{")
			ref = "{" + name + "-" + ref
		refs.append(ref)
		n = line.find("\\ref{", m)
	return refs

def check_def_text(def_text):
	n = def_text.find("\\label{")
	if n < 0:
		return "No label in definition."
	n = def_text.find("{\\it ")
	if n < 0:
		return "Nothing defined in definition."
	return ""

def find_defined_notions(def_text):
	def_notions = []
	n = def_text.find("{\\it ")
	while n >= 0:
		m = find_sub_clause(def_text, n, "{", "}")
		def_notions.append(def_text[n : m + 1])
		n = def_text.find("{\\it ", m)
	return def_notions

def check_refs(refs, labels):
	n = 0
	while n < len(refs):
		ref = refs[n]
		m = 0
		found = -1
		while found == -1 and m < len(labels):
			if ref == labels[m]:
				found = 1
			m = m + 1
		if found == -1:
			return ref
		n = n + 1
	return ""
