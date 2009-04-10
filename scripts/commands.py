from functions import *

path = get_path()

commands = []

lijstje = list_text_files(path)

ext = ".tex"
for name in lijstje:
	filename = path + name + ext
	tex_file = open(filename, 'r')
	line_nr = 0
	verbatim = 0
	def_text = ""
	for line in tex_file:

		# Update line number
		line_nr = line_nr + 1

		# Check for verbatim, because we do not look for commands
		# inside verbatim environment.
		verbatim = verbatim + beginning_of_verbatim(line)
		if verbatim:
			if end_of_verbatim(line):
				verbatim = 0
			continue

		potential_new = find_commands(line)
		n = 0
		while n < len(potential_new):
			if new_command(potential_new[n], commands):
				commands.append(potential_new[n])
			n = n + 1

	tex_file.close()

n = 0
while n < len(commands):
	print commands[n]
	n = n + 1
