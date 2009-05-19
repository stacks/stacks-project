from functions import *

def parse_aux_file(name):
	label_loc = {}
	aux_file = open(name + ".aux", 'r')
	for line in aux_file:
		if line.find("\\newlabel{") < 0:
			continue
		
		n = find_sub_clause(line, 9, "{", "}")
		short_label = line[10: n]

		if short_label.find("tocindent") == 0:
			continue

		# Turn short label into full label if necessary
		if not name == "book":
			label = name + "-" + short_label
		else:
			label = short_label
		
		split = split_label(label)

		# Find the current number of the lemma, theorem, etc.
		m = find_sub_clause(line, n + 2, "{", "}")
		nr = line[n + 3: m]

		# find the current page number
		k = find_sub_clause(line, m + 1, "{", "}")
		page = line[m + 2: k]

		text = cap_type(split[1]) + " " + nr + " on page " + page
		label_loc[label] = text
	aux_file.close()
	return label_loc

path = get_path()

tags = get_tags(path)

titles = all_titles(path)

lijstje = list_text_files(path)

list_dict = {}
for name in lijstje:
	label_loc = parse_aux_file(name)
	list_dict[name] = label_loc

label_loc = parse_aux_file("book")

print "<html>"
print "<head>"
print "<title> Location of tag </title>"
print "</head>"
print "<body>"
print
print "<p align=left>"
print "<a href=\"http://math.columbia.edu/algebraic_geometry/stacks-git\">stacks-git</a> | <a href=query.php>query</a> | <a href=\"tags.pdf\">more on tags</a>"
print "</p>"
print
print "<?php"

# Make the long array for book version
print "$tag_loc = array("
n = 0
while n < len(tags):
	tag = tags[n][0]
	label = tags[n][1]
	if label in label_loc:
		print "\"" + tag + "\" => \"" + label_loc[label] + "\","
	n = n + 1
print "\"ZZZ\" => \"Does not exist yet.\");"
print "$tag_loc_chap = array("
n = 0
while n < len(tags):
	tag = tags[n][0]
	label = tags[n][1]
	if label in label_loc:
		split = split_label(label)
		name = split[0]
		text = name + ".pdf#" + tag + "\\\">"
		text = text + list_dict[name][label]
		text = text + "</a> in ``" + titles[name] + "''"
		print "\"" + tag + "\" => \"" + text + "\","
	n = n + 1
print "\"ZZZ\" => \"Does not exist yet.\");"

# Text the reader sees
print "echo \"<p align=center>\";"
print "echo \"Your tag \";"
print "echo $_GET[\"tag\"];"
print "echo \" points to </p>\\n\";"

print "echo \"<p align=center>\";"
print "echo \"<a href=\\\"\";"
print "echo $tag_loc_chap[$_GET[\"tag\"]];"
print "echo \" or the identical</a></p>\\n\";"

print "echo \"<p align=center>\";"
print "echo \"<a href=\\\"book.pdf#\";"
print "echo $_GET[\"tag\"];"
print "echo \"\\\">\";"
print "echo $tag_loc[$_GET[\"tag\"]];"
print "echo \"</a> of the book version.</p>\\n\";"

print "?>"
print
print "</body>"
print "</html>"
