from functions import *

labels = []

lijstje = list_text_files()

path = "../"
ext = ".tex"
for name in lijstje:
	filename = path + name + ext
	tex_file = open(filename, 'r')
	have_title = 0
	in_proof = 0
	in_definition = 0
	in_environment = 0
	in_math_mode = 0
	line_nr = 0
	def_text = ""
	for line in tex_file:

		# Update line number
		line_nr = line_nr + 1

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
		error_text = check_double_dollar(line)
		if error_text:
			print_error(error_text, line, name, line_nr)

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

		# Find label if there is one
		label = find_label(line)
		if label:
			label = label.rstrip("}")
			label = label.lstrip("{")
			labels.append(label)

		# Check for forward references in proofs
		if in_proof:
			refs = find_refs(line)
			error_text = check_refs(refs, labels)
			if error_text:
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











