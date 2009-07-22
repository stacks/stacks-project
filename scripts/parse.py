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

		# Check double dollar signs
		error_text = check_double_dollar(line)
		if error_text:
			print_error(error_text, line, name, line_nr)

		# Find label if there is one
		label = find_label(line)
		if label:
			if not standard_label(label):
				print_error("Nonstandard label.",
				line, name, line_nr)
			label = name + "-" + label
			labels.append(label)
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
			if labeled_env(line):
				next_labeled = 1

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
			if end_of_proof(line):
				in_proof = 0
		else:
			in_proof = beginning_of_proof(line)

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

	tex_file.close()

print "------------------------------------------------"
print

# Check the tags file for correctness
tags = get_tags(path)
nr = len(tags)
# Exceptional cases...
exceptions = ['02C0', '003W', '003X']
print "There are",
print nr,
print "tags. Checking tags..."
n = 0
while n < nr:
	if not check_ref(tags[n][1], labels):
		if not tags[n][0] in exceptions:
			print "Tag pointing nowhere: ",
			print tags[n]
	n = n + 1

print "All done."





