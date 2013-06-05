from functions import *

path = get_path()

labels = []

lijstje = list_text_files(path)

ext = ".tex"
for name in lijstje:
	filename = path + name + ext
	tex_file = open(filename, 'r')
	have_title = 0
	in_proof = 0
	in_definition = 0
	line_nr = 0
	verbatim = 0
	next_labeled = 0
	needs_proof = 0
	next_proof_label = 0
	in_lab_env = 0
	item_on_line = 0
	def_text = ""
	for line in tex_file:

		# Update line number
		line_nr = line_nr + 1

		# Check length of line
		error_text = length_of_line(line)
		if error_text:
			print_error(error_text, line, name, line_nr)

		# Check for verbatim, because we do not check correctness
		# inside verbatim environment.
		verbatim = verbatim + beginning_of_verbatim(line)
		if verbatim:
			if end_of_verbatim(line):
				verbatim = 0
			continue

		# These we always want at the start of a line by themselves
		error_text = only_on_line("\\begin{", 7, line)
		if error_text:
			print_error(error_text, line, name, line_nr)
		error_text = only_on_line("\\end{", 5, line)
		if error_text:
			print_error(error_text, line, name, line_nr)
		error_text = only_on_line("\\label{", 7, line)
		if error_text:
			print_error(error_text, line, name, line_nr)
		error_text = only_on_line("\\title{", 7, line)
		if error_text:
			print_error(error_text, line, name, line_nr)
		error_text = beginning_of_line('\\item', line)
		if error_text:
			print_error(error_text, line, name, line_nr)
		error_text = beginning_of_line('\\xymatrix', line)
		if error_text:
			print_error(error_text, line, name, line_nr)
		error_text = beginning_of_line('\\medskip', line)
		if error_text:
			print_error(error_text, line, name, line_nr)
		error_text = beginning_of_line('\\section', line)
		if error_text:
			print_error(error_text, line, name, line_nr)
		error_text = beginning_of_line('\\subsection', line)
		if error_text:
			print_error(error_text, line, name, line_nr)
		error_text = beginning_of_line('\\subsubsection', line)
		if error_text:
			print_error(error_text, line, name, line_nr)
		error_text = beginning_of_line('\\phantomsection', line)
		if error_text:
			print_error(error_text, line, name, line_nr)

		# Check double dollar signs
		error_text = check_double_dollar(line)
		if error_text:
			print_error(error_text, line, name, line_nr)

		# Find label if there is one
		label = find_label(line)
		if label:
			if not standard_label(label):
				print_error("Nonstandard label.", line, name, line_nr)
			if label.find('item') == 0:
				if not item_on_line:
					print_error("Item label on wrong line.", line, name, line_nr)
			label = name + "-" + label
			if label in labels:
				print_error("Double label.",
				line, name, line_nr)
			labels.append(label)
			if next_proof_label:
				proof_label = label
				next_proof_label = 0
		else:
			# check if there is a label if there should be one
			if next_labeled:
				error_text = "No label for environment."
				print_error(error_text, line, name, line_nr)

		# Reset boolean
		next_labeled = 0

		# Beginning environment?
		if beginning_of_env(line):
			if not standard_env(line):
				error_text = 'Not a standard environment.'
				print_error(error_text, line, name, line_nr)

		# Beginning labeled environment?
		if labeled_env(line):
			# Equations are allowed to occur inside labeled envs
			if in_lab_env and line.find("\\begin{equation}") < 0:
				error_text = 'Nested environments.'
				print_error(error_text, line, name, line_nr)
			# The following checks that there are no labeled
			# environments between the beginning of one that needs
			# a proof and the start of its proof, except for
			# equations.
			if needs_proof and line.find("\\begin{equation}") < 0:
				error_text = 'Missing proof.'
				print_error(error_text, line, name, line_nr)
			in_lab_env = 1
			next_labeled = 1
			if proof_env(line):
				needs_proof = 1
				next_proof_label = 1

		# End labeled environment?
		if end_labeled_env(line):
			in_lab_env = 0

		# New part?
		if new_part(line):
			next_labeled = 1

		# Line defines new item?
		item_on_line = new_item(line)	

		# Have we found a title?
		if not have_title and is_title(line):
			have_title = 1

		# Check definition
		if in_definition == 1:
			def_text = def_text + " " + line.rstrip()
			if end_of_definition(line) == 1:
				in_definition = 0
				error_text = check_def_text(def_text)
				if error_text:
					print_error(error_text, def_text, name, line_nr)
		else:
			in_definition = beginning_of_definition(line)
			if in_definition == 1:
				def_text = line.rstrip()

		# Check for forward references in proofs
		if in_proof:
			refs = find_refs(line, name)
			error_text = check_refs(refs, labels)
			if error_text:
				error_text = "Forward reference "\
				+ error_text + " in proof."
				print_error(error_text, line, name, line_nr)
			if proof_label in refs:
				error_text = "Self reference "
				print_error(error_text, line, name, line_nr)
			if end_of_proof(line):
				in_proof = 0
		else:
			in_proof = beginning_of_proof(line)
			if in_proof:
				needs_proof = 0

	# Check for title in the file
	if not have_title:
		print "No title in " + name
		raise Exception('No title present.')

	tex_file.close()

print "------------------------------------------------"
print

# Pass through all the files again to see if all references point to labels
for name in lijstje:
	filename = path + name + ext
	tex_file = open(filename, 'r')
	line_nr = 0
	verbatim = 0
	for line in tex_file:

		# Update line number
		line_nr = line_nr + 1

		# Check for verbatim, because we do not check references
		# inside verbatim environment
		verbatim = verbatim + beginning_of_verbatim(line)
		if verbatim:
			if end_of_verbatim(line):
				verbatim = 0
			continue

		# Check for references
		refs = find_refs(line, name)
		error_text = check_refs(refs, labels)
		if error_text:
			error_text = "Reference " + error_text +\
			" not found."
			print_error(error_text, line, name, line_nr)

		# Internal references
		error_text = internal_refs(line, refs, name)
		if error_text:
			error_text = "Internal reference " + error_text
			print_error(error_text, line, name, line_nr)

	tex_file.close()

print "------------------------------------------------"
print

# Check the tags file for correctness
tags = get_tags(path)
nr = len(tags)
print "There are",
print nr,
print "tags. Checking tags..."
n = 0
tagged_up = {}
while n < nr:
	label = tags[n][1]
	if label.find(' ') >= 0:
		print "Found illegal character in: " + label
	if not check_ref(label, labels):
		print "Tag pointing nowhere: ",
		print tags[n]
	if not label in tagged_up:
		tagged_up[label] = tags[n][0]
	else:
		print "Two tags for " + label + ": " + tags[n][0] + " and " + tagged_up[label]
	n = n + 1

print "All done."





