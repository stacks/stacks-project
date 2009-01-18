from functions import *

labels = {}

lijstje = list_text_files()

path = "../"
ext = ".tex"
for name in lijstje:
	filename = path + name + ext
	tex_file = open(filename, 'r')
	labels[name] = []
	have_title = 0
	in_proof = 0
	in_definition = 0
	in_environment = 0
	in_math_mode = 0
	line_nr = 0
	def_text = ""
	for line in tex_file:

		# update line number
		line_nr = line_nr + 1

		# These we always want at the beginning of the line
		beginning_of_line("\\begin{", line)
		beginning_of_line("\\end{", line)
		beginning_of_line("$$", line)
		beginning_of_line("\\label{", line)

		# Have we found a title?
		if not have_title and is_title(line):
			have_title = 1

		# Check definition
		if in_definition == 1:
			def_text = def_text + " " + line.rstrip()
			if end_of_definition(line) == 1:
				in_definition = 0
				check_defined_notions(def_text)
		else:
			in_definition = beginning_of_definition(line)
			if in_definition == 1:
				def_text = line.rstrip()

	# Check for title in the file
	if not have_title:
		print "No title in " + name
		raise Exception('No title present.')
	
	tex_file.close()
