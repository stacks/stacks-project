from functions import *

from sys import argv
if not len(argv) == 3:
	print()
	print("This script needs exactly two arguments")
	print("namely the path to the stacks project")
	print("and the stem of the tex file")
	print()
	raise Exception('Wrong arguments')

path = argv[1]
path.rstrip("/")
path = path + "/"

name = argv[2]

def replace_newtheorem(line):
	if line.find("\\newtheorem{") == 0:
		line = line.replace("]{", "]{\\href{https://stacks.math.columbia.edu/tag/\\TAG}{",1)
		line = line.rstrip()
		return line + "}\n"
	if line.find("\\documentclass") == 0:
		line = line.replace("\\documentclass", "\\documentclass[oneside]")
		return line
	return line



# File preamble.tex is a special case and we do it separately
if name == "preamble":
	tex_file = open(path + name + ".tex", 'r')
	for line in tex_file:
		print(replace_newtheorem(line), end = '')

	version = git_version(path)

	from datetime import date
	now = date.today()

	print("\\usepackage{marginnote}")
	print("\\renewcommand*{\\marginfont}{\\normalfont}")

	print("\\date{This is a chapter of the Stacks Project, version " + version + ", compiled on " + now.strftime('%h %d, %Y.}'))

	tex_file.close()

	from sys import exit
	exit()




tags = get_tags(path)

label_tags = dict((tags[n][1], tags[n][0]) for n in range(0, len(tags)))

if name == "book":
	tex_file = open(path + "tmp/" + name + ".tex", 'r')
else:
	tex_file = open(path + name + ".tex", 'r')

document = 0
verbatim = 0
for line in tex_file:

	# Check for verbatim
	verbatim = verbatim + beginning_of_verbatim(line)
	if verbatim:
		if end_of_verbatim(line):
			verbatim = 0
		print(line, end = '')
		continue

	# Do stuff in preamble or just after \begin{document}
	if not document:
		if name == "book":
			line = replace_newtheorem(line)
			if line.find("\\begin{document}") == 0:
				print("\\usepackage{marginnote}")
				print("\\renewcommand*{\\marginfont}{\\normalfont}")
		print(line, end = '')
		if line.find("\\begin{document}") == 0:
			print("\\newcommand{\\TAG}{ZZZZ}")
			document = 1
		continue

	# labels all get hypertargets
	if is_label(line):
		short = find_label(line)
		if name == "book":
			label = short
		else:
			label = name + "-" + short
		print(line, end = '')
		# don't put in hypertarget if label does not have a tag
		if label in label_tags:
			print("\\hypertarget{" + label_tags[label] + "}{}")
			# there is a bug in marginnotes that eats subsection titles...
			if short.find("subsection") >= 0:
				line = tex_file.readline()
				print(line, end = '')
				line = tex_file.readline()
				print(line, end = '')
				print("\\reversemarginpar\\marginnote{" + label_tags[label] + "}")
			else:
				print("\\reversemarginpar\\marginnote{" + label_tags[label] + "}")
		continue

	# Lines with labeled environments
	if labeled_env(line):
		oldline = line
		line = tex_file.readline()
		short = find_label(line)
		if name == "book":
			label = short
		else:
			label = name + "-" + short
		if not label in label_tags:
			# ZZZZ is used as pointer to nonexistent tags
			print("\\renewcommand{\\TAG}{ZZZZ}")
			print(oldline, end = '')
			print(line, end = '')
			continue
		print("\\renewcommand{\\TAG}{" + label_tags[label] + "}")
		print(oldline, end = '')
		print(line, end = '')
		print("\\reversemarginpar\\marginnote{" + label_tags[label] + "}\\hypertarget{" + label_tags[label] + "}{}")
		continue

	if line.find("\\begin{reference}") == 0:
		print("\\normalmarginpar\\marginnote{")
		continue

	if line.find("\\end{reference}") == 0:
		print("}")
		continue

	print(line, end = '')

tex_file.close()
