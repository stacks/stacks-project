from functions import *

path = get_path()

lijstje = list_text_files(path)

short_titles = {'introduction' : 'Introduction',\
'conventions' : 'Conventions,',\
'sets' : 'Sets,',\
'categories' : 'Categories,',\
'topology' : 'Topology,',\
'sheaves' : 'Sheaves,',\
'sites' : 'Sites,',\
'stacks' : 'Stacks,',\
'algebra' : 'Algebra,',\
'brauer' : 'Brauer Groups,',\
'homology' : 'Homology,',\
'derived' : 'Derived Categories,',\
'simplicial' : 'Simplicial,',\
'more-algebra' : 'More on Algebra,',\
'smoothing' : 'Smoothing Ring Maps,',\
'modules' : 'Modules,',\
'sites-modules' : 'Modules on Sites,',\
'injectives' : 'Injectives,',\
'cohomology' : 'Cohomology,',\
'sites-cohomology' : 'Cohomology on Sites,',\
'hypercovering' : 'Hypercoverings,',\
'schemes' : 'Schemes,',\
'constructions' : 'Constructions,',\
'properties' : 'Properties,',\
'morphisms' : 'Morphisms,',\
'coherent' : 'Cohomology of Schemes,',\
'divisors' : 'Divisors,',\
'limits' : 'Limits,',\
'varieties' : 'Varieties,',\
'topologies' : 'Topologies,',\
'descent' : 'Descent,',\
'perfect' : 'Derived Categories of Schemes,',\
'more-morphisms' : 'More on Morphisms,',\
'flat' : 'More on Flatness,',\
'groupoids' : 'Groupoids,',\
'more-groupoids' : 'More on Groupoids,',\
'etale' : '\\\'Etale Morphisms,',\
'chow' : 'Chow Homology,',\
'adequate' : 'Adequate Modules,',\
'dualizing' : 'Dualizing Complexes,',\
'etale-cohomology' : '\\\'Etale Cohomology,',\
'crystalline' : 'Crystalline Cohomology,',\
'proetale' : 'Pro-\\\'etale Cohomology,',\
'spaces' : 'Spaces,',\
'spaces-properties' : 'Properties of Spaces,',\
'spaces-morphisms' : 'Morphisms of Spaces,',\
'decent-spaces' : 'Decent Spaces,',\
'spaces-cohomology' : 'Cohomology of Spaces,',\
'spaces-limits' : 'Limits of Spaces,',\
'spaces-divisors' : 'Divisors on Spaces,',\
'spaces-topologies' : 'Topologies on Spaces,',\
'spaces-descent' : 'Descent on Spaces,',\
'spaces-perfect' : 'Derived Categories of Spaces,',\
'spaces-more-morphisms' : 'More on Morphisms of Spaces,',\
'spaces-over-fields' : 'Spaces over Fields,',\
'spaces-groupoids' : 'Groupoids in Spaces,',\
'spaces-more-groupoids' : 'More on Groupoids in Spaces,',\
'bootstrap' : 'Bootstrap,',\
'groupoids-quotients' : 'Quotients of Groupoids,',\
'formal-defos' : 'Formal Deformation Theory,',\
'defos' : 'Deformation Theory,',\
'cotangent' : 'Cotangent,',\
'algebraic' : 'Algebraic Stacks,',\
'examples-stacks' : 'Examples of Stacks,',\
'stacks-sheaves' : 'Sheaves on Stacks,',\
'criteria' : 'Criteria for Representability,',\
'artin' : 'Artin\'s Axioms,',\
'quot' : 'Quot,',\
'stacks-properties' : 'Properties of Stacks,',\
'stacks-morphisms' : 'Morphisms of Stacks,',\
'stacks-cohomology' : 'Cohomology of Stacks,',\
'stacks-perfect' : 'Derived Categories of Stacks,',\
'stacks-introduction' : 'Introducing Algebraic Stacks,',\
'examples' : 'Examples,',\
'exercises' : 'Exercises,',\
'guide' : 'Guide to Literature,',\
'desirables' : 'Desirables,',\
'coding' : 'Coding Style,',\
'obsolete' : 'Obsolete,',\
'fdl' : 'GNU Free Documentation License,',\
'index' : 'Auto Generated Index,'}

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


def exists_ref(line):
	if line.find("\\ref{") < 0:
		return 0
	N = line.count("\\ref{")
	A = line.count("\\ref{item-")
	B = line.count("\\ref{equation-")
	C = line.count("-item-")
	D = line.count("-equation-")
	# This means that references to items and equations do not count
	if N > A + B + C + D:
		return 1
	return 0

def check_short_title_and_type(prev, name, line_nr):
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
			if not Short_Title in text:
				print "Did not find short title in:"
				print text
				print
				print "gvim +{} {}.tex".format(line_nr - 1, name)
				print
		if not ( split[1] == 'item' or split[1] == 'equation' ):
			Type = caps_types[split[1]]
			if not Type in text:
				print "Did not find cap type in:"
				print text
				print
				print "gvim +{} {}.tex".format(line_nr - 1, name)
				print
		n = n + 1


#
#
# First time through we do some basic checks on the existence of
# Short Titles and Type
#
#
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
				check_short_title_and_type(prev, name, line_nr)
				prev = []
				have_ref = 0
		if math:
			if math == 2:
				math = 0
				prev_line = ''
			continue

		# No references on line
		if not exists_ref(line):
			if have_ref == 1:
				check_short_title_and_type(prev, name, line_nr)
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

#
# Finds a Short Title if there is one and returns
# 'error' if there is more than one
#
def get_title(line):
	Short_Titles = short_titles.values()
	occur = []
	n = 0
	while n < len(Short_Titles):
		Short_Title = Short_Titles[n]
		if Short_Title in line:
			occur.append(Short_Title)
		n = n + 1
	if len(occur) == 0:
		return ''
	if len(occur) == 1:
		if line.count(occur[0]) > 1:
			return 'error'
		else:
			return occur[0]
	if len(occur) == 2:
		if occur[1] in occur[0]:
			return occur[0]
		if occur[0] in occur[1]:
			return occur[1]
		return 'error'
	if len(occur) == 3:
		Short_Title = 'More on Morphisms of Spaces,'
		if occur[0] == Short_Title or occur[1] == Short_Title or occur[2] == Short_Title:
			return Short_Title
		Short_Title = 'More on Groupoids in Spaces,'
		if occur[0] == Short_Title or occur[1] == Short_Title or occur[2] == Short_Title:
			return Short_Title
		Short_Title = 'Introducing Algebraic Stacks,'
		if occur[0] == Short_Title or occur[1] == Short_Title or occur[2] == Short_Title:
			return Short_Title
	# len(occur) >= 3
	return 'error'

import re
Types = [\
'Definition',\
'Definitions',\
'Lemma',\
'Lemmas',\
'Proposition',\
'Propositions',\
'Theorem',\
'Theorems',\
'Remark',\
'Remarks',\
'Example',\
'Examples',\
'Exercise',\
'Exercises',\
'Situation',\
'Situations',\
'Section',\
'Sections',\
'Subsection',\
'Subsections']

PTypes = []
n = 0
while n < len(Types):
	PTypes.append(re.compile(Types[n] + '$'))
	PTypes.append(re.compile(Types[n] + ' \\\\ref{'))
	n = n + 1

#
# Finds a Type if there is an occurence of
#	<Type><whitespace>\ref{
# or
#	<Type><whitespace><end of line>.
# Returns this pattern.
# It returns 'error' if there is more than one
# such pattern on the line.
#
def get_type(line):
	occur = []
	line = line.rstrip()
	n = 0
	while n < len(PTypes):
		Type = Types[2*(n/4)]
		if PTypes[n].search(line):
			occur.append(Type)
		n = n + 1
	if len(occur) == 0:
		return ''
	if len(occur) == 1:
		# check for uniqueness, so we can parse the line later on.
		if line.count(occur[0]) > 1:
			# Exception
			if 'Exercises, Exercise' in line:
				return 'Exercise'
			return 'error'
		else:
			return occur[0]
	# len(occur) >= 2
	return 'error'

#
#
# Checks the line
#
#
def check_line(line, name, Short_Title, New_Short_Title, Type, New_Type):
	if New_Short_Title:
		new_short_title = line.find(New_Short_Title)
	else:
		new_short_title = len(line) + 1
	if New_Type:
		new_type = line.find(New_Type)
	else:
		new_type = len(line) + 1
	refs = find_refs(line, name)
	n = 0
	while n < len(refs):
		ref = refs[n]
		split = split_label(ref)
		if split[0] == name:
			position = line.find(split[1] + split[2])
		else:
			position = line.find(ref)

		# Check for Short Title only for external references
		# Also do this for items and equations...
		if not split[0] == name:
			if position < new_short_title:
				if not Short_Title == short_titles[split[0]]:
					print "Did not find short title in:"
					print line
					print
					print "gvim +{} {}.tex".format(line_nr, name)
					print
			else:
				if not New_Short_Title == short_titles[split[0]]:
					print "Did not find short title in:"
					print line
					print
					print "gvim +{} {}.tex".format(line_nr, name)
					print

		# Do not check for Type of item and equation
		if not (split[1] == 'item' or split[1] == 'equation'):
			if position < new_type:
				if (not Type) or (not Type in caps_types[split[1]]):
					print "Did not find type in:"
					print line,
					print
					print "gvim +{} {}.tex".format(line_nr, name)
					print
			else:
				if (not New_Type) or (not New_Type in caps_types[split[1]]):
					print "Did not find type in:"
					print line,
					print
					print "gvim +{} {}.tex".format(line_nr, name)
					print
		n = n + 1
	return len(refs)

ext = ".tex"
for name in lijstje:
	tex_file = open(path + name + ext, 'r')
	line_nr = 0
	verbatim = 0
	math = 0
	Short_Title = ''
	Type = ''
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
		if math:
			if math == 2:
				math = 0
			continue

		New_Short_Title = get_title(line)
		if New_Short_Title == 'error':
			print 'More than one short title on a line'
			print line
			print
			print "gvim +{} {}.tex".format(line_nr, name)
			print

		New_Type = get_type(line)
		if New_Type == 'error':
			print 'More than one type on a line'
			print line,
			print
			print "gvim +{} {}.tex".format(line_nr, name)
			print

		nr = check_line(line, name, Short_Title, New_Short_Title, Type, New_Type)

		if New_Type:
			Type = New_Type

		if New_Short_Title:
			Short_Title = New_Short_Title

		# Reset if we have a line having nothing to do with references
		if nr == 0 and not (New_Type or New_Short_Title):
			Type = ''
			Short_Title = ''
			

	tex_file.close()


