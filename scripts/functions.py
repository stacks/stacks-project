def get_path():
	from sys import argv
	if not len(argv) == 2:
		print
		print "This script needs exactly one argument"
		print "namely the path to the stacks project directory"
		print
		raise Exception('Wrong arguments')
	path = argv[1]
	path.rstrip("/")
	path = path + "/"
	return path

def list_text_files(path):
	Makefile_file = open(path + "Makefile", 'r')
	for line in Makefile_file:
		n = line.find("LIJST = ")
		if n == 0:
			break
	lijst = ""
	while line.find("\\") >= 0:
		line = line.rstrip()
		line = line.rstrip("\\")
		lijst = lijst + " " + line
		line = Makefile_file.next()
	Makefile_file.close()
	lijst = lijst + " " + line
	lijst = lijst.replace("LIJST = ", "")
	lijst = lijst + " fdl"
	return lijst.split()

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

def beginning_of_verbatim(line):
	n = line.find("\\begin{verbatim}")
	if n == 0:
		return 1
	else:
		return 0

def end_of_verbatim(line):
	n = line.find("\\end{verbatim}")
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

def find_defined_terms(def_text):
	def_terms = []
	n = def_text.find("{\\it ")
	while n >= 0:
		m = find_sub_clause(def_text, n, "{", "}")
		def_terms.append(def_text[n : m + 1])
		n = def_text.find("{\\it ", m)
	return def_terms

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

def find_commands(line):
	commands = []
	n = line.find("\\")
	while n >= 0:
		m = n + 1
		while m < len(line):
			if line[m] == "(" or line[m] == " " or line[m] == "\\" or line[m] == "{" or line[m] == "_" or line[m] == "\n" or line[m] == "$" or line[m] == "[" or line[m] == "," or line[m] == "'" or line[m] == "}" or line[m] == "]" or line[m] == ")" or line[m] == "^" or line[m] == "/" or line[m] == "=" or line[m] == "." or line[m] == "|" or line[m] == "+" or line[m] == "-" or line[m] == ":" or line[m] == "&" or line[m] == "\"" or line[m] == "@" or line[m] == ";":
				break
			m = m + 1
		if m == n + 1:
			m = m + 1
		commands.append(line[n : m])
		n = line.find("\\", m)
	return commands

def new_command(new, commands):
	m = 0
	while m < len(commands):
		if new == commands[m]:
			return 0;
		m = m + 1
	return 1

# Structure of tags:
#	Already created tags are listed in the file tags/tags
#	Each line of tags/tags is of the form
#		tag,full_label
#	with no spaces and where
#		tag: the actual tag
#		full_label: label with "name-" prepended if the label occurs
#			in the file name.tex
#	See also the file tags/tags for an example.
#	We can also have lines starting with a hash # marking comments.
#	We may want to change the name/label if a result moves from one file to
#	another, or if we split a long file into two pieces. We may also
#	sometimes change the label of a result (eg if there is a typo in the
#	label itself). But the tags should never change.

# The first tag is 0000 and the last tag is ZZZZ
def next_tag(tag):
	next = list(tag)
	S = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	i = 3
	while i >= 0:
		n = S.find(next[i])
		if n == 35:
			next[i] = '0'
		else:
			next[i] = S[n + 1]
			break
		i = i - 1
	return next[0] + next[1] + next[2] + next[3]

def get_tag_line(line):
	line = line.rstrip()
	return line.split(",")

def get_tags(path):
	tags = []
	tag_file = open(path + "tags/tags", 'r')
	for line in tag_file:
		if not line.find("#") == 0:
			tags.append(get_tag_line(line))
	tag_file.close()
	return tags

def new_label(tags, label):
	n = 0
	new = 1
	while new and n < len(tags):
		if tags[n][1] == label:
			new = 0
		n = n + 1
	return new

def get_all_labels(path, name):
	labels = []
	tex_file = open(path + name + ".tex", 'r')
	for line in tex_file:
		label = find_label(line)
		if label:
			label = label.rstrip("}")
			label = label.lstrip("{")
			label = name + "-" + label
			labels.append(label)
	tex_file.close()
	return labels

def get_new_tags(path, tags):
	last_tag = tags[-1][0]
	lijstje = list_text_files(path)
	new_tags = []
	for name in lijstje:
		labels = get_all_labels(path, name)
		n = 0
		while n < len(labels):
			if new_label(tags, labels[n]):
				last_tag = next_tag(last_tag)
				new_tags.append([last_tag, labels[n]])
			n = n + 1
	return new_tags

def print_new_tags(new_tags):
	n = 0
	while n < len(new_tags):
		print new_tags[n][0] + "," + new_tags[n][1]
		n = n + 1
	return

def write_new_tags(path, new_tags):
	tag_file = open(path + "tags/tags", 'a')
	n = 0
	while n < len(new_tags):
		tag_file.write(new_tags[n][0] + "," + new_tags[n][1] + "\n")
		n = n + 1
	tag_file.close()
	return
