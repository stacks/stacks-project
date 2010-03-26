from functions import *

# Find location of repository
from sys import argv

if not len(argv) >= 2:
	print
	print "This script at least one argument"
	print "namely the path to the stacks project directory."
	print "The other arguments are the stem names of the tex files"
	print "to which the material got moved."
	print
	raise Exception('Wrong arguments')

path = argv[1]
path.rstrip("/")
path = path + "/"
moved = []
n = 2
while n < len(argv):
	moved.append(argv[n])
	n = n + 1

labels = {}
refs = []

lijstje = list_text_files(path)

ext = ".tex"
for name in lijstje:
	filename = path + name + ext
	tex_file = open(filename, 'r')
	labels[name] = []
	line_nr = 0
	verbatim = 0
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

		# Find label if there is one
		label = find_label(line)
		if label:
			if not standard_label(label):
				print_error("Nonstandard label.",
				line, name, line_nr)
			if label in labels[name]:
				print_error("Double label.",
				line, name, line_nr)
			labels[name].append(label)
			continue

		# Find references if there are some
		refs_line = find_refs(line, name)
		n = 0
		while n < len(refs_line):
			ref = refs_line[n]
			if ref == "":
				print_error("Empty reference.",
				line, name, line_nr)
			else:
				refs.append([name, ref, line_nr])
			n = n + 1

	tex_file.close()

print "------------------------------------------------"
print

tags = []
filename = path + "tags/tags"
tags_file = open(filename, 'r')
for line in tags_file:
	if line.find("#") == 0:
		continue

	line = line.rstrip()
	t = line.split(",")
	tag = t[0]
	t = split_label(t[1])
	tags.append([tag, t[0], t[1] + t[2]])

tags_file.close()

nr = len(refs)
print "There are",
print nr,
print "references."
nr = len(labels)
print "There are",
print nr,
print "files."
nr = len(tags)
print "There are",
print nr,
print "tags."
print
print "------------------------------------------------"
print
print "We are going to look for tags whose corresponding labels got moved to new files."
print

fixable = 0
nowhere = 0
multiple = 0
moved_detected_lazy = set()

n = 0
while n < len(tags):

	tag = tags[n][0]
	tag_name = tags[n][1]
	tag_label = tags[n][2]

	matches = []
	for name in lijstje:
		if tag_label in labels[name]:
			matches.append(name)
	
	if not tag_name in matches:
		if len(matches) == 0:
			nowhere = nowhere + 1
		if len(matches) == 1:
			moved_detected_lazy.add(matches[0])
		if len(set(matches) & set(moved)) == 1:
			fixable = fixable + 1
		else:
			if len(matches) > 1:
				multiple = multiple + 1

	n = n + 1

print "Lazily detected files to use as input"
for name in moved_detected_lazy:
	print name
print
print "Moved fixable tags: ",
print fixable
print "Moved tags with multiple choices: ",
print multiple
print "Tags pointing nowhere: ",
print nowhere

if fixable == 0:
	print "Nothing fixable."
	exit(0)


