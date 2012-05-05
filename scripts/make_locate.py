from sys import exit
from functions import *

# Only use this script after running
#	make tags
#
def parse_aux_file(name, path):
	label_loc = {}
	aux_file = open(path + "tags/tmp/" + name + ".aux", 'r')
	for line in aux_file:
		if line.find("\\newlabel{") < 0:
			continue
		
		n = find_sub_clause(line, 9, "{", "}")
		short_label = line[10: n]

		if short_label.find("tocindent") == 0:
			continue

		# Turn short label into full label if necessary
		if not name == "book":
			label = name + "-" + short_label
		else:
			label = short_label
		
		split = split_label(label)

		# Find the current number of the lemma, theorem, etc.
		m = find_sub_clause(line, n + 2, "{", "}")
		nr = line[n + 3: m]

		# find the current page number
		k = find_sub_clause(line, m + 1, "{", "}")
		page = line[m + 2: k]

		text = cap_type(split[1]) + " " + nr + " on page " + page
		label_loc[label] = text
	aux_file.close()
	return label_loc

# Variable to contain all the texts of labels
label_texts = {}

# Variable to contain all the texts of proofs
proof_texts = {}

# Helper function
def assign_label_text(label, text):
	if not label:
		exit(1)
	if not text:
		print label
		exit(1)
	label_texts[label] = text

path = get_path()

# Get all tags
tags = get_tags(path)
label_tags = dict((tags[n][1], tags[n][0]) for n in range(0, len(tags)))

titles = all_titles(path)

lijstje = list_text_files(path)

# Get locations in chapters
list_dict = {}
for name in lijstje:
	label_loc = parse_aux_file(name, path)
	list_dict[name] = label_loc

# get locations in book
label_loc = parse_aux_file("book", path)

# Function to convert refs into links
def make_links(line, name):
	new_line = ""
	m = 0
	n = line.find("\\ref{")
	while n >= 0:
		new_line = new_line + line[m : n + 5]
		m = find_sub_clause(line, n + 4, "{", "}")
		ref = line[n + 5: m]
		if standard_label(ref):
			label = name + "-" + ref
		else:
			label = ref
		if label in label_tags:
			new_line = new_line + '<a href=\"locate.php?tag=' + label_tags[label] + '\">' + ref + '</a>'
		else:
			new_line = new_line + ref
		n = line.find("\\ref{", m)
	new_line = new_line + line[m:]
	return new_line

# Get text of
#	labeled environments
#	proofs
#	labeled items
#	sections, subsections, subsubsections
#	equations
ext = ".tex"
for name in lijstje:
	filename = path + name + ext
	tex_file = open(filename, 'r')
	line_nr = 0
	verbatim = 0
	in_env = 0
	in_proof = 0
	in_item = 0
	in_section = 0
	in_subsection = 0
	in_subsubsection = 0
	in_equation = 0
	label = ""
	label_env = ""
	label_proof = ""
	label_item = ""
	label_section = ""
	label_subsection = ""
	label_subsubsection = ""
	label_equation = ""
	text_env = ""
	text_proof = ""
	text_item = ""
	text_section = ""
	text_subsection = ""
	text_subsubsection = ""
	text_equation = ""
	for line in tex_file:

		# Update line number
		line_nr = line_nr + 1

		# Check for verbatim, because we do not check correctness
		# inside verbatim environment.
		verbatim = verbatim + beginning_of_verbatim(line)
		if verbatim:
			if end_of_verbatim(line):
				verbatim = 0
			continue

		# See if labeled environment starts
		if labeled_env(line) and line.find("\\begin{equation}") < 0:
			in_env = 1

		# See if a proof starts
		if beginning_of_proof(line):
			in_proof = 1

		# See if item starts
		if new_item(line):
			# Closeout previous item
			if in_item and label_item:
				assign_label_text(label_item, text_item)
				in_item = 0
				text_item = ""
				label_item = ""
			in_item = 1

		# See if section starts
		if new_part(line):
			# Closeout previous section/subsection/subsubsection
			if in_section and line.find('\\section') == 0:
				assign_label_text(label_section, text_section)
				in_section = 0
				text_section = ""
				label_section = ""
			if in_subsection and (line.find('\\section') == 0 or line.find('\\subsection') == 0):
				assign_label_text(label_subsection, text_subsection)
				in_subsection = 0
				text_subsection = ""
				label_subsection = ""
			if in_subsubsection and (line.find('\\section') == 0 or line.find('\\subsection') == 0 or line.find('\\subsubsection') == 0):
				assign_label_text(label_subsubsection, text_subsubsection)
				in_subsubsection = 0
				text_subsubsection = ""
				label_subsubsection = ""
			# Start new section/subsection/subsubsection
			if line.find('\\section') == 0:
				in_section = 1
			if line.find('\\subsection') == 0:
				in_subsection = 1
			if line.find('\\subsubsection') == 0:
				in_subsubsection = 1

		# See if equation starts
		if line.find('\\begin{equation}') == 0:
			in_equation = 1

		# Find label if there is one
		if line.find('\\label{') == 0:
			label = find_label(line)
			if label.find('item') == 0:
				label_item = name + '-' + label
			elif label.find('section') == 0:
				label_section = name + '-' + label
			elif label.find('subsection') == 0:
				label_subsection = name + '-' + label
			elif label.find('subsubsection') == 0:
				label_subsubsection = name + '-' + label
			elif label.find('equation') == 0:
				label_equation = name + '-' + label
			else:
				label_env = name + '-' + label
				if label.find('lemma') == 0 or label.find('proposition') == 0 or label.find('theorem') == 0:
					label_proof = label_env

		# Add line to env_text if we are in an environment
		if in_env:
			text_env = text_env + make_links(line, name)

		# Add line to proof_text if we are in a proof
		if in_proof:
			text_proof = text_proof + make_links(line, name)

		# Add line to item_text if we are in an item
		if in_item:
			text_item = text_item + make_links(line, name)

		# Add line to section_text if we are in a section
		if in_section:
			text_section = text_section + make_links(line, name)
		if in_subsection:
			text_subsection = text_subsection + make_links(line, name)
		if in_subsubsection:
			text_subsubsection = text_subsubsection + make_links(line, name)

		# Add line to equation_text if we are in an equation
		if in_equation:
			text_equation = text_equation + make_links(line, name)

		# Closeout env
		if end_labeled_env(line) and line.find("\\end{equation}") < 0:
			in_env = 0
			assign_label_text(label_env, text_env)
			text_env = ""
			label_env = ""

		# Closeout proof
		if end_of_proof(line):
			in_proof = 0
			# We pick up only the first proof if there are multiple proofs
			if label_proof:
				if not text_proof:
					exit(1)
				proof_texts[label_proof] = text_proof
			text_proof = ""
			label_proof = ""

		# Closeout item
		if line.find('\\end{enumerate}') == 0 or line.find('\\end{itemize}') == 0 or line.find('\\end{list}') == 0:
			if in_item and label_item:
				assign_label_text(label_item, text_item)
				label_item = ""
			in_item = 0
			text_item = ""
			label_item = ""

		# Closeout section/subsection/subsubsection
		if line.find('\\input{chapters}') == 0:
			if in_section:
				assign_label_text(label_section, text_section)
				in_section = 0
				text_section = ""
				label_section = ""
			if in_subsection:
				assign_label_text(label_subsection, text_subsection)
				in_subsection = 0
				text_subsection = ""
				label_subsection = ""
			if in_subsubsection:
				assign_label_text(label_subsubsection, text_subsubsection)
				in_subsubsection = 0
				text_subsubsection = ""
				label_subsubsection = ""

		# Closeout equation
		if line.find('\\end{equation}') == 0:
			in_equation = 0
			assign_label_text(label_equation, text_equation)
			text_equation = ""
			label_equation = ""

	tex_file.close()


# Prepare directory for latex code snippets
code_dir = path + '/tags/tmp/code'
import os
if not os.path.exists(code_dir):
	os.mkdir(code_dir)
else:
	print "Warning: tags/tmp/code not empty!"

# ZZZZ is a special case
text = 'Tag ZZZZ. If a result has been labeled with tag ZZZZ<br>\n'
text = text + 'this means the result has not been given a stable tag yet.'
filename = code_dir + '/ZZZZ'
code_file = open(filename, 'w')
code_file.write(text)
code_file.close()

# Print link to location in chapter
n = 0
while n < len(tags):
	tag = tags[n][0]
	label = tags[n][1]
	if not label in label_loc:
		print "Warning: missing location for tag " + tag
		print "and label " + label
		n = n + 1
		continue
	split = split_label(label)
	name = split[0]
	text = "Use tag " + tag + " to reference\n"
	text = text + "<ul>\n<li><a href=\"" + name + ".pdf#" + tag + "\">"
	text = text + list_dict[name][label]
	text = text + "</a> in ``" + titles[name] + "'', or </li>\n"
	filename = code_dir + '/' + tag
	code_file = open(filename, 'w')
	code_file.write(text)
	text = "<li><a href=\"book.pdf#" + tag + "\">"
	text = text + label_loc[label] + "</a> of the book version.</li>\n</ul>\n"
	code_file.write(text)
	if not label in label_texts:
		n = n + 1
		continue	
	text = "The latex code of the corresponding environment is:\n"
	text =  text + "<div style=\"font-family: monospace; text-align: left; display: table\">\n"
	text = text + "<pre>\n"
	code_file.write(text)
	code_file.write(label_texts[label])
	if label in proof_texts:
		code_file.write("\n")
		code_file.write(proof_texts[label])
	code_file.write("</pre></div>\n")
	code_file.close()
	n = n + 1



