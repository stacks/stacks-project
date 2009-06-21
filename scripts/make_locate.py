from functions import *

# Only use this script after running
#	make tags
#
def parse_aux_file(name, path):
	label_loc = {}
	aux_file = open(path + "tags/tmp/" + name + ".aux", 'r')
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
	label_loc = parse_aux_file(name, path)
	list_dict[name] = label_loc

label_loc = parse_aux_file("book", path)

print "<html>"
print "<head>"
print "<link rel=\"icon\" type=\"image/vnd.microsoft.icon\" href=\"stacks.ico\" />"
print "<title> Location of tag </title>"
print "</head>"
print "<body>"
print
print "<p align=left>"
print "<a href=\"index.html\">stacks project</a> | <a href=query.php>search</a> | <a href=\"tags.html\">tags explained</a>"
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
print "\"ZZZZ\" => \"does not exist yet\");"
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
print "\"ZZZZ\" => \"introduction.pdf#ZZZZ\\\">does not exist yet</a>\");"

# Text the reader sees
print "if (array_key_exists($_GET[\"tag\"], $tag_loc)) {"
print "echo \"<p align=center>\";"
print "echo \"Use tag \";"
print "echo $_GET[\"tag\"];"
print "echo \" to reference <br>\\n\";"
print "echo \"<a href=\\\"\";"
print "echo $tag_loc_chap[$_GET[\"tag\"]];"
print "echo \" or the identical</a><br>\\n\";"
print "echo \"<a href=\\\"book.pdf#\";"
print "echo $_GET[\"tag\"];"
print "echo \"\\\">\";"
print "echo $tag_loc[$_GET[\"tag\"]];"
print "echo \"</a> of the book version.</p>\\n\";"
print "}"
print "else"
print "{"
print "echo \"<p align=center>\";"
print "echo \"This tag does not exist.<br>\";"
print "echo \"This may be because you mistyped<br>\";"
print "echo \"or the result it pointed to was<br>\";"
print "echo \"found to be wrong.<br>\";"
print "echo \"For more on tags click \";"
print "echo \"<a href=\\\"tags.html\\\">here</a>.<br>\";"
print "echo \"To try again click \";"
print "echo \"<a href=\\\"tags.html\\\">here</a>.\";"
print "}"
print "?>"
print
print "</body>"
print "</html>"
