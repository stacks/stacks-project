list_of_standard_envs = ['abstract', 'verbatim', 'quote', 'itemize', 'list', 'center', 'eqnarray*', 'eqnarray', 'align', 'align*', 'document', 'equation', 'enumerate', 'proof', 'matrix', 'lemma', 'proposition', 'theorem', 'remark', 'remarks', 'example', 'exercise', 'situation', 'equation', 'definition', 'item']

list_of_labeled_envs = ['lemma', 'proposition', 'theorem', 'remark', 'remarks', 'example', 'exercise', 'situation', 'definition']

list_of_standard_labels = ['definition', 'lemma', 'proposition', 'theorem', 'remark', 'remarks', 'example', 'exercise', 'situation', 'equation', 'section', 'item']




# Find location of repository
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

# List the stems of the TeX files in the project
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

# Print error
def print_error(error_text, line, name, line_nr):
	print "In file " + name + ".tex"
	print "On line", line_nr
	print "Line: " + line.rstrip()
	print "Error: " + error_text
	print

# Check length line
def length_of_line(line):
	n = len(line)
	if n > 81:
		return "More than 80 characters on a line."
	return ""

# Check if line starts with given pattern
def beginning_of_line(pattern, line):
	n = line.find(pattern)
	if n > 0:
		return "Pattern: " + pattern + " not at the start of the line."
	return ""

# See if line starts an environment
def beginning_of_env(line):
	n = line.find("\\begin{")
	if n == 0:
		return 1
	return 0

# See if line starts a definition
def beginning_of_definition(line):
	n = line.find("\\begin{definition}")
	if n == 0:
		return 1
	return 0

# See if line ends a definition
def end_of_definition(line):
	n = line.find("\\end{definition}")
	if n == 0:
		return 1
	return 0

# See if line starts a proof
def beginning_of_proof(line):
	n = line.find("\\begin{proof}")
	if n == 0:
		return 1
	return 0

# See if line ends a proof
def end_of_proof(line):
	n = line.find("\\end{proof}")
	if n == 0:
		return 1
	return 0

# See if line starts verbatim environment,
# also check if the \begin{verbatim} starts the line
def beginning_of_verbatim(line):
	n = line.find("\\begin{verbatim}")
	if n > 0:
		raise Exception('\\begin{verbatim} not at start of line.')
	if n == 0:
		return 1
	else:
		return 0

# See if line ends verbatim environment,
# also check if the \begin{verbatim} starts the line
def end_of_verbatim(line):
	n = line.find("\\end{verbatim}")
	if n > 0:
		raise Exception('\\end{verbatim} not at start of line.')
	if n == 0:
		return 1
	return 0

# Find clause starting in specific spot with specific open and close characters
def find_sub_clause(text, spot, open, close):
	nr_braces = 0
	while nr_braces >= 0:
		spot = spot + 1
		if text[spot] == open:
			nr_braces = nr_braces + 1
		if text[spot] == close:
			nr_braces = nr_braces - 1
	return spot

# See if there is a clause immediately following the current spot, and
# return spot of closing brace
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

# Find spot of last brace of sequence of clauses starting at spot
def rest_clauses(text, spot):
	n = next_clause(text, spot)
	while n > spot:
		spot = n
		n = next_clause(text, spot)
	return n

# Check if the pattern starts the line and has only clauses following...
def only_on_line(pattern, spot, line):
	line = line.rstrip()
	n = line.find(pattern)
	if n > 0:
		return "Pattern: " + pattern + "not at the start of the line."
	if n == 0:
		m = find_sub_clause(line, spot, "{", "}")
		m = rest_clauses(line, m)
		if not m + 1 == len(line):
			return "Pattern: " + pattern + "*} not by itself."
	return ""

# Check if $$ is by itself and at the start of the line
def check_double_dollar(line):
	n = line.find("$$")
	if n < 0:
		return ""
	if n > 0:
		return "Double dollar not at start of line."
	line = line.rstrip()
	if not len(line) == 2:
		return "Double dollar not by itself on line."

# Check if the line contains the title of the document
def is_title(line):
	n = line.find("\\title{")
	if n < 0:
		return 0
	return 1

# Assuming there is a title on the line, find it.
def find_title(line):
	n = line.find("\\title{")
	if n < 0:
		raise Exception('No title on line')
	n = n + 6
	m = find_sub_clause(line, n, "{", "}")
	title = line[n + 1 : m]
	return title

# Check if the line contains a label
def is_label(env_text):
	n = env_text.find("\\label{")
	if n < 0:
		return 0
	return 1

# Returns short label. Does not assume there is a label on the line
def find_label(env_text):
	n = env_text.find("\\label{")
	if n < 0:
		return ""
	n = n + 6
	m = find_sub_clause(env_text, n, "{", "}")
	label = env_text[n + 1 : m]
	return label

# Check if there are references on the line
def contains_ref(line):
	n = line.find("\\ref{")
	if n < 0:
		return 0
	return 1

# Returns list of full references on the line
def find_refs(line, name):
	refs = []
	n = line.find("\\ref{")
	while n >= 0:
		m = find_sub_clause(line, n + 4, "{", "}")
		ref = line[n + 5: m]
		if standard_label(ref):
			ref = name + "-" + ref
		refs.append(ref)
		n = line.find("\\ref{", m)
	return refs

# Check if short label is standard
def standard_label(label):
	n = 0
	while n < len(list_of_standard_labels):
		if label.find(list_of_standard_labels[n] + '-') == 0:
			return 1
		n = n + 1
	return 0

# Split label into comonents
def split_label(label):
	pieces = label.split('-')
	name = pieces[0]
	type = pieces[1]
	rest = pieces[2]
	n = 3
	while n < len(pieces):
		rest = rest + "-" + pieces[n]
		n = n + 1
	return [name, type, rest]

# Check if environment is standard
# The input should be a line from latex file containing the
# \begin{environment} statement
def standard_env(env):
	n = 0
	while n < len(list_of_standard_envs):
		if env.find('{' + list_of_standard_envs[n] + '}') >= 0:
			return 1
		n = n + 1
	return 0

# Check if environment should have a label
# The input should be a line from latex file containing the
# \begin{environment} statement
def labeled_env(env):
	n = 0
	while n < len(list_of_labeled_envs):
		if env.find('{' + list_of_labeled_envs[n] + '}') >= 0:
			return 1
		n = n + 1
	return 0

# Checks inner text of definition for existence of a label (this is now
# obsolete) and for the existence of at least one term which is being
# defined
def check_def_text(def_text):
	n = def_text.find("\\label{")
	if n < 0:
		return "No label in definition."
	n = def_text.find("{\\it ")
	if n < 0:
		return "Nothing defined in definition."
	return ""

# Returns list of terms being defined, which are pieces of the form
#	{\it definition-text}
def find_defined_terms(def_text):
	def_terms = []
	n = def_text.find("{\\it ")
	while n >= 0:
		m = find_sub_clause(def_text, n, "{", "}")
		def_terms.append(def_text[n : m + 1])
		n = def_text.find("{\\it ", m)
	return def_terms

# See if ref occurs in list labels
def check_ref(ref, labels):
	try:
		labels.index(ref)
	except:
		return 0
	return 1

# See if references already occur in list labels
def check_refs(refs, labels):
	n = 0
	while n < len(refs):
		ref = refs[n]
		if not check_ref(ref, labels):
			return ref
		n = n + 1
	return ""

# Silly function to detect LaTeX commands. Not perfect.
def find_commands(line):
	S = "( \\{_\n$[,'}])^/=.|+-:&\"@;"
	commands = []
	n = line.find("\\")
	while n >= 0:
		m = n + 1
		while m < len(line):
			if S.find(line[m]) >= 0:
				break
			m = m + 1
		if m == n + 1:
			m = m + 1
		commands.append(line[n : m])
		n = line.find("\\", m)
	return commands

# See if a command already occurs
def new_command(new, commands):
	try:
		commands.index(new)
	except:
		return 1
	return 0

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
	verbatim = 0
	for line in tex_file:
		# Check for verbatim, because we do not add labels from
		# verbatim environments.
		verbatim = verbatim + beginning_of_verbatim(line)
		if verbatim:
			if end_of_verbatim(line):
				verbatim = 0
			continue

		label = find_label(line)
		if label:
			label = name + "-" + label
			labels.append(label)
	tex_file.close()
	return labels

def all_labels(path):
	lijstje = list_text_files(path)
	labels = []
	for name in lijstje:
		extra = get_all_labels(path, name)
		labels = labels + extra
	return labels

def get_new_tags(path, tags):
	last_tag = tags[-1][0]
	label_tags = dict((tags[n][1], tags[n][0]) for n in range(0, len(tags)))
	lijstje = list_text_files(path)
	new_tags = []
	for name in lijstje:
		labels = get_all_labels(path, name)
		n = 0
		while n < len(labels):
			if labels[n] not in label_tags:
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
