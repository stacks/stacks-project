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

# Assuming there is a title on the line, find it.
def find_title(line):
	n = line.find("\\title{")
	if n < 0:
		return ""
	n = n + 6
	m = find_sub_clause(line, n, "{", "}")
	title = line[n + 1 : m]
	return title

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

# Spits out the git version of the git repositor in the path
def git_version(path):
	from subprocess import Popen, PIPE, STDOUT
	cmd = 'git --git-dir=' + path + '.git log --pretty=format:%h -n1'
	p = Popen(cmd, shell=True, stdout=PIPE).stdout
	version = p.read()
	p.close()
	return version

# Check if the line contains a label
def is_label(env_text):
	n = env_text.find("\\label{")
	if n < 0:
		return 0
	return 1

# Check if there are references on the line
def contains_ref(line):
	n = line.find("\\ref{")
	if n < 0:
		return 0
	return 1


########################################################################
#
#
# The rest of the code is shared with the code in the file
# functions.py in stacks-tools
#
#
########################################################################

# We also have labels for
#	'section', 'subsection', 'subsubsection' (every one of these has a label)
#	'item' (typically an item does not have a label)
list_of_labeled_envs = ['lemma', 'proposition', 'theorem', 'remark', 'remarks', 'example', 'exercise', 'situation', 'equation', 'definition']

# Standard labels
list_of_standard_labels = ['definition', 'lemma', 'proposition', 'theorem', 'remark', 'remarks', 'example', 'exercise', 'situation', 'equation', 'section', 'subsection', 'subsubsection', 'item']

# List the stems of the TeX files in the project
# in the correct order
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

# Check if the line contains the title of the document
def is_title(line):
	n = line.find("\\title{")
	if n < 0:
		return 0
	return 1

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

# Returns short label. Does not assume there is a label on the line
def find_label(env_text):
	n = env_text.find("\\label{")
	if n < 0:
		return ""
	n = n + 6
	m = find_sub_clause(env_text, n, "{", "}")
	label = env_text[n + 1 : m]
	return label

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

# Silly function
def get_tag_line(line):
	line = line.rstrip()
	return line.split(",")

# Get all active tags in the project
def get_tags(path):
	tags = []
	tag_file = open(path + "tags/tags", 'r')
	for line in tag_file:
		if not line.find("#") == 0:
			tags.append(get_tag_line(line))
	tag_file.close()
	return tags

# Check if environment should have a label
# The input should be a line from latex file containing the
# \begin{environment} statement
def labeled_env(env):
	n = 0
	while n < len(list_of_labeled_envs):
		if env.find('\\begin{' + list_of_labeled_envs[n] + '}') == 0:
			return 1
		n = n + 1
	return 0

