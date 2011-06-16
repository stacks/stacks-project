from functions import *

path = get_path()

lijstje = list_text_files(path)

short_titles = {'introduction' : 'Introduction',\
'conventions' : 'Conventions',\
'sets' : 'Sets',\
'categories' : 'Categories',\
'topology' : 'Topology',\
'sheaves' : 'Sheaves',\
'algebra' : 'Algebra',\
'sites' : 'Sites',\
'homology' : 'Homology',\
'derived' : 'Derived Categories',\
'more-algebra' : 'More on Algebra',\
'simplicial' : 'Simplicial',\
'modules' : 'Modules',\
'sites-modules' : 'Modules on Sites',\
'injectives' : 'Injectives',\
'cohomology' : 'Cohomology',\
'sites-cohomology' : 'Cohomology on Sites',\
'hypercovering' : 'Hypercoverings',\
'schemes' : 'Schemes',\
'constructions' : 'Constructions',\
'properties' : 'Properties',\
'morphisms' : 'Morphisms',\
'coherent' : 'Coherent',\
'divisors' : 'Divisors',\
'limits' : 'Limits',\
'varieties' : 'Varieties',\
'chow' : 'Chow Homology',\
'topologies' : 'Topologies',\
'descent' : 'Descent',\
'more-morphisms' : 'More on Morphisms',\
'flat' : 'More on Flatness',\
'groupoids' : 'Groupoids',\
'more-groupoids' : 'More on Groupoids',\
'etale' : '\'Etale Morphisms',\
'etale-cohomology' : '\'Etale Cohomology',\
'spaces' : 'Spaces',\
'spaces-properties' : 'Properties of Spaces',\
'spaces-morphisms' : 'Morphisms of Spaces',\
'decent-spaces' : 'Decent Spaces',\
'spaces-topologies' : 'Topologies on Spaces',\
'spaces-descent' : 'Descent on Spaces',\
'spaces-more-morphisms' : 'More on Morphisms of Spaces',\
'quot' : 'Quot',\
'spaces-over-fields' : 'Spaces over Fields',\
'stacks' : 'Stacks',\
'formal-defos' : 'Formal Deformation Theory',\
'spaces-groupoids' : 'Groupoids in Spaces',\
'spaces-more-groupoids' : 'More on Groupoids in Spaces',\
'bootstrap' : 'Bootstrap',\
'examples-stacks' : 'Examples of Stacks',\
'groupoids-quotients' : 'Quotients of Groupoids',\
'algebraic' : 'Algebraic Stacks',\
'criteria' : 'Criteria for Representability',\
'stacks-properties' : 'Properties of Stacks',\
'stacks-morphisms' : 'Morphisms of Stacks',\
'examples' : 'Examples',\
'exercises' : 'Exercises',\
'guide' : 'Guide to Literature',\
'desirables' : 'Desirables',\
'coding' : 'Coding Style',\
'fdl' : 'GNU Free Documentation License',\
'index' : 'Auto Generated Index'}

#
# Do not test for item or equation
#
caps_types = {'definition' : 'Definition',\
'lemma' : 'Lemma',\
'proposition' : 'Proposition',\
'theorem' : 'Theorem',\
'remark' : 'Remark',\
'remarks' : 'Remarks',\
'example' : 'Example',\
'exercise' : 'Exercise',\
'situation' : 'Situation',\
'section' : 'Section',\
'subsection' : 'Subsection'}

def fix_it(prev, name, line_nr):
	text = prev[0].rstrip()
	n = 1
	while n < len(prev):
		text = text + " " + prev[n].rstrip()
		n = n + 1

	# full labels of references
	refs = find_refs(text, name)

	n = 0
	while n < len(refs):
		ref = refs[n]
		split = split_label(ref)
		if not split[0] == name:
			Short_Title = short_titles[split[0]]
			if text.find(Short_Title) < 0:
				print "Did not find short title in:"
				print text
				print "In file " + name + ".tex"
				print "On line", line_nr - 1
				print
		if not ( split[1] == 'item' or split[1] == 'equation' ):
			Type = caps_types[split[1]]
			if text.find(Type) < 0:
				print "Did not find cap type in:"
				print text
				print "In file " + name + ".tex"
				print "On line", line_nr - 1
				print
		n = n + 1

ext = ".tex"
for name in lijstje:
	filename = path + name + ext
	tex_file = open(filename, 'r')
	prev = []
	have_ref = 0
	line_nr = 0
	verbatim = 0
	math = 0
	prev_line = ''
	for line in tex_file:

		# Update line number
		line_nr = line_nr + 1

		# Check for verbatim, because we do not have references
		# inside verbatim environments.
		verbatim = verbatim + beginning_of_verbatim(line)
		if verbatim:
			if end_of_verbatim(line):
				verbatim = 0
			continue

		# Check for math environment since we don't fix references
		# in those (too tricky).
		if line.find("$$") == 0:
			math = math + 1
			if math == 1 and have_ref:
				fix_it(prev, name, line_nr)
				prev = []
				have_ref = 0
		if math:
			if math == 2:
				math = 0
			continue

		# No references on line
		if line.find("\\ref{") < 0:
			if have_ref == 1:
				fix_it(prev, name, line_nr)
				prev = []
				have_ref = 0
		# there are references
		else:
			if have_ref == 1:
				prev.append(line)
			else:
				have_ref = 1
				prev.append(prev_line)
				prev.append(line)

		prev_line = line

	tex_file.close()
	# tex_out.close()



