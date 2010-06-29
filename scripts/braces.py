from functions import *

path = get_path()

lijstje = list_text_files(path)

def begin_xymatrix(line):
	n = line.find("\\xymatrix{")
	if n > 0:
		raise Exception('\\begin{verbatim} not at start of line.')
	if n == 0:
		return 1
	else:
		return 0

def nr_braces_xymatrix(text):
	spot = 0
	nr_braces = 0
	while spot < len(text):
		if text[spot] == '{':
			nr_braces = nr_braces + 1
		if text[spot] == '}':
			nr_braces = nr_braces - 1
		spot = spot + 1
	return nr_braces

def do_it(text):
	new = "\\xymatrix{{"
	open = 1
	nr = 2
	spot = 11
	while spot < len(text):
		if text[spot] == '{':
			nr = nr + 1
			new = new + '{'
			spot = spot + 1
			continue
		if text[spot] == '}':
			nr = nr - 1
			new = new + '}'
			spot = spot + 1
			continue
		if nr > open + 1:
			new = new + text[spot]
			spot = spot + 1
			continue
		if text[spot] == '&' and open == 1:
			new = new + '}&{'
			open = 1
			spot = spot + 1
			continue
		if text[spot] == '&' and open == 0:
			new = new + '&{'
			open = 1
			nr = nr + 1
			spot = spot + 1
			continue
		# \ar
		if text[spot] == '\\' and text[spot + 1] == 'a' and text[spot + 2] == 'r' and open == 1:
			new = new + '}\\'
			open = 0
			nr = nr - 1
			spot = spot + 1
			continue
		# \rtwocell
		if text[spot] == '\\' and text[spot + 1] == 'r' and text[spot + 2] == 't' and text[spot + 3] == 'w' and open == 1:
			new = new + '}\\'
			open = 0
			nr = nr - 1
			spot = spot + 1
			continue
		# \ruppertwocell
		if text[spot] == '\\' and text[spot + 1] == 'r' and text[spot + 2] == 'u' and text[spot + 3] == 'p' and open == 1:
			new = new + '}\\'
			open = 0
			nr = nr - 1
			spot = spot + 1
			continue
		# \rlowertwocell
		if text[spot] == '\\' and text[spot + 1] == 'r' and text[spot + 2] == 'l' and text[spot + 3] == 'o' and open == 1:
			new = new + '}\\'
			open = 0
			nr = nr - 1
			spot = spot + 1
			continue
		# \rrtwocell
		if text[spot] == '\\' and text[spot + 1] == 'r' and text[spot + 2] == 'r' and text[spot + 3] == 't' and open == 1:
			new = new + '}\\'
			open = 0
			nr = nr - 1
			spot = spot + 1
			continue
		if text[spot] == '\\' and text[spot + 1] == '\\' and open == 1:
			new = new + '}\\\\{'
			open = 1
			spot = spot + 2
			continue
		if text[spot] == '\\' and text[spot + 1] == '\\' and open == 0:
			new = new + '\\\\{'
			open = 1
			nr = nr + 1
			spot = spot + 2
			continue
		new = new + text[spot]
		spot = spot + 1

	if open == 1:
		new = new + '}'
		nr = nr - 1

	if nr > 0:
		raise Exception(text + "\n" + new)

	return new

ext = ".tex"
for name in lijstje:
	filename = path + name + ext
	tex_file = open(filename, 'r')
	tex_out = open(path + "tmp/" + name + ext, 'w')
	line_nr = 0
	verbatim = 0
	xymatrix = 0
	xytext = ""
	for line in tex_file:

		# Update line number
		line_nr = line_nr + 1

		# Check for verbatim, because we do not check correctness
		# inside verbatim environment.
		verbatim = verbatim + beginning_of_verbatim(line)
		if verbatim:
			tex_out.write(line)
			if end_of_verbatim(line):
				verbatim = 0
			continue

		# Check xymatrix
		xymatrix = xymatrix + begin_xymatrix(line)
		if not xymatrix:
			tex_out.write(line)
			continue

		if line.find('%') >= 0:
			line = line[0:line.find('%')]
			line = line + '\\empty'
		xytext = xytext + " " + line.rstrip()
		if nr_braces_xymatrix(xytext) == 0:
			xymatrix = 0
			tex_out.write(do_it(xytext))
			tex_out.write('\n')
			xytext = ""

	tex_file.close()
	tex_out.close()
