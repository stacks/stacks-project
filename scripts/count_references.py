from functions import *

path = get_path()

lijstje = list_text_files(path)
# Just pick one input file:
#lijstje = ['sites']

# All tags
tags = get_tags(path)

# Dictionary labels --> tags
label_tags = dict((tags[n][1], tags[n][0]) for n in range(0, len(tags)))

# Dictionary tags --> number of references
tags_nr = dict()
n = 0
while n < len(tags):
	tags_nr[tags[n][0]] = 0
	n = n + 1
tags_nr['ZZZZ'] = 0

ext = ".tex"
for name in lijstje:
	filename = path + name + ext
	tex_file = open(filename, 'r')
	in_proof = 0
	line_nr = 0
	verbatim = 0
	next_proof = 0
	refs_proof = []
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

		# In proofs
		if in_proof:
			refs = find_refs(line, name)
			refs_proof.extend(refs)
			if end_of_proof(line):
				refs_proof_set = set(refs_proof)
				refs_proof_set.discard('ZZZZ')
				refs_proof = list(refs_proof_set)
				nr = -1
				tags_proof = []
				n = 0
				while n < len(refs_proof):
					ref_tag = label_tags[refs_proof[n]]
					tags_nr[ref_tag] = tags_nr[ref_tag] + 1
					n = n + 1
				refs_proof = []
				in_proof = 0
		else:
			in_proof = beginning_of_proof(line)

	tex_file.close()

T = 0
n = 0
while n < len(tags):
	if tags_nr[tags[n][0]] > T:
		T = tags_nr[tags[n][0]]
	n = n + 1

print "Maximum number of references is",
print T,
print "attained by: "
n = 0
while n < len(tags):
	if tags_nr[tags[n][0]] == T:
		print tags[n][0],
	n = n + 1
print
print "The next few maxima are: "
m = 1
while m < 70:
	print "Number of references:",
	print T - m,
	print " : ",
	n = 0
	while n < len(tags):
		if tags_nr[tags[n][0]] == T - m:
			print tags[n][0],
		n = n + 1
	print
	m = m + 1

