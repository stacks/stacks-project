from functions import *

def find_tag(label, label_tags):
	if not label in label_tags:
		return "ZZZZ"
	else:
		return label_tags[label]

path = get_path()

labels = []

lijstje = list_text_files(path)

# Check the tags file for correctness
tags = get_tags(path)
label_tags = dict((tags[n][1], tags[n][0]) for n in range(0, len(tags)))

print "digraph dependencies {"
print
print "node [shape=point]"
print "edge [dir=none]"
print

ext = ".tex"
for name in lijstje:
	filename = path + name + ext
	tex_file = open(filename, 'r')
	in_proof = 0
	line_nr = 0
	verbatim = 0
	next_proof = 0
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
			if next_proof:
				proof_label = name + "-" + label
				proof_tag = find_tag(proof_label, label_tags)

		# Reset boolean
		next_proof = 0

		# Beginning environment?
		if beginning_of_env(line):
			if proof_env(line):
				next_proof = 1

		# In proofs
		if in_proof:
			refs = find_refs(line, name)
			n = 0
			while n < len(refs):
				ref_tag = find_tag(refs[n], label_tags)
				print "a" + proof_tag + "a",
				print "->",
				print "a" + ref_tag + "a"
				n = n + 1
			if end_of_proof(line):
				in_proof = 0
		else:
			in_proof = beginning_of_proof(line)

	tex_file.close()

print "}"
