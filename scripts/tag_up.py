from functions import *

from sys import argv
if not len(argv) == 3:
	print
	print "This script needs exactly two arguments"
	print "namely the path to the stacks project"
	print "and the stem of the tex file"
	print
	raise Exception('Wrong arguments')

path = argv[1]
path.rstrip("/")
path = path + "/"

name = argv[2]

tags = get_tags(path)

label_tags = dict((tags[n][1], tags[n][0]) for n in range(0, len(tags)))

if name == "book":
	tex_file = open(path + "tmp/" + name + ".tex", 'r')
else:
	tex_file = open(path + name + ".tex", 'r')

TAG_def = 0
verbatim = 0
for line in tex_file:
	
	# Check for verbatim
	verbatim = verbatim + beginning_of_verbatim(line)
	if verbatim:
		if end_of_verbatim(line):
			verbatim = 0
		print line,
		continue

	if not TAG_def and line.find("\\begin{document}") == 0:
		print line,
		print "\\newcommand{\\TAG}{long-ZZZ}"
		TAG_def = 1
		continue
	
	if beginning_of_env(line) and labeled_env(line):
		oldline = line
		line = tex_file.next()
		short = find_label(line)
		if name == "book":
			label = short
		else:
			label = name + "-" + short
		if not label in label_tags:
			print oldline,
			print line
			continue
		print "\\renewcommand{\\TAG}{long-" + label_tags[label] + "}"
		print oldline,
		print line,
		print "\\hypertarget{" + label_tags[label] + "}{}"
	else:
		print line,

tex_file.close()
