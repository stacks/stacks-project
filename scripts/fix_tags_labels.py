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

lijstje = list_text_files(path)

print "------------------------------------------------"
print "Finding labels."
print

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

	tex_file.close()



print "------------------------------------------------"
print "Fixing tags whose labels got moved."
print

fixed_tags = 0
nowhere_tags = 0
multiple_tags = 0
moved_detected_lazy = set()

filename = path + "tags/tags"
tags_file = open(filename, 'r')
tags_out = open(path + "tmp/tags", 'w')
for line in tags_file:
	if line.find("#") == 0:
		tags_out.write(line)
		continue

	l = line.rstrip()
	t = l.split(",")
	tag = t[0]
	t = split_label(t[1])
	tag_name = t[0]
	tag_label = t[1] + t[2]

	matches = []
	for name in lijstje:
		if tag_label in labels[name]:
			matches.append(name)

	if tag_name in matches:
		tags_out.write(line)
		continue

	if len(matches) == 0:
		print "Cannot fix tag " + tag
		print "Tag points nowhere"
		nowhere_tags = nowhere_tags + 1
		newline = line
	
	if len(set(matches) & set(moved)) == 1:
		fixed_tags = fixed_tags + 1
		for new_name in set(matches) & set(moved): break
		newline = tag + "," + new_name + "-" + tag_label + "\n"
	else:
		if len(matches) == 1:
			moved_detected_lazy.add(matches[0])
		if len(matches) > 1:
			print "Cannot fix tag " + tag
			print "Multiple possibilites"
			multiple_tags = multiple_tags + 1
		newline = line
	
	tags_out.write(newline)


tags_file.close()
tags_out.close()




print
print "------------------------------------------------"
print "Fixing references."
print

fixed_refs = 0
nowhere_refs = 0
multiple_refs = 0



def fix_ref(ref, name):
	global fixed_refs, nowhere_refs, multiple_refs
	# short label case
	if standard_label(ref):
		if ref in labels[name]:
			return ref
		nr = 0
		for other in moved:
			if ref in labels[other]:
				nr = nr + 1
				new_name = other
		if nr == 1:
			fixed_refs = fixed_refs + 1
			return new_name + "-" + ref

		if nr > 1:
			multiple_refs = multiple_refs + 1
			print "Cannot fix reference " + ref + " in " + name
			print "Multiple possibilites"

		if nr == 0:
			nowhere_refs = nowhere_refs + 1
			print "Cannot fix reference " + ref + " in " + name
			print "No corresponding labels found in listed files."
			for other in lijstje:
				if ref in labels[other]:
					nr = nr + 1
					new_name = other
			if nr == 1:
				moved_detected_lazy.add(new_name)

		return ref

	# long label case
	t = split_label(ref)
	ref_name = t[0]
	ref_label = t[1] + t[2]
	if ref_label in labels[ref_name]:
		return ref

	nr = 0
	for other in moved:
		if ref_label in labels[other]:
			nr = nr + 1
			new_name = other
	if nr == 1:
		fixed_refs = fixed_refs + 1
		return new_name + "-" + ref_label

	if nr > 1:
		multiple_refs = multiple_refs + 1
		print "Cannot fix reference " + ref + " in " + name
		print "Multiple possibilites"

	if nr == 0:
		nowhere_refs = nowhere_refs + 1
		print "Cannot fix reference " + ref + " in " + name
		print "No corresponding labels found in listed files."
		for other in lijstje:
			if ref in labels[other]:
				nr = nr + 1
				new_name = other
		if nr == 1:
			moved_detected_lazy.add(new_name)

	return ref


ext = ".tex"
for name in lijstje:
	filename = path + name + ext
	tex_file = open(filename, 'r')
	tex_out = open(path + "tmp/" + name + ext, 'w')
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
			tex_out.write(line)
			continue

		# No references
		if line.find("\\ref{") < 0:
			tex_out.write(line)
			continue

		newline = ""
		m = 0
		n = line.find("\\ref{")
		while n >= 0:
			newline = newline + line[m: n + 5]
			m = find_sub_clause(line, n + 4, "{", "}")
			ref = line[n + 5: m]
			newline = newline + fix_ref(ref, name)
			n = line.find("\\ref{", m)
		newline = newline + line[m: len(line)]
		tex_out.write(newline)

	tex_file.close()
	tex_out.close()


print "------------------------------------------------"
print
print "Fixed tags: ",
print fixed_tags
print "Moved tags with multiple choices: ",
print multiple_tags
print "Tags pointing nowhere: ",
print nowhere_tags
print
print "Fixed references: ",
print fixed_refs
print "Bad references with multiple choices: ",
print multiple_refs
print "References pointing nowhere: ",
print nowhere_refs
print

print
print "------------------------------------------------"
print
print "Lazily detected files to use as input"
print
for name in moved_detected_lazy:
	print name,
print
print

