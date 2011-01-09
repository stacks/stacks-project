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

# Get locations in chapters
list_dict = {}
for name in lijstje:
	label_loc = parse_aux_file(name, path)
	list_dict[name] = label_loc

# get locations in book
label_loc = parse_aux_file("book", path)

# Get labeled environments texts
label_texts = {}
ext = ".tex"
for name in lijstje:
	filename = path + name + ext
	tex_file = open(filename, 'r')
	line_nr = 0
	verbatim = 0
	in_lab_env = 0
	text = ""
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

		# See if labeled environment starts
		if labeled_env(line) and line.find("\\begin{equation}") < 0:
			in_lab_env = 1
			text = line.rstrip() + "<br>\n"
			line = tex_file.next()
			label = name + "-" + find_label(line)

		if in_lab_env:
			text = text + line.rstrip() + "<br>\n"
			if end_labeled_env(line) and line.find("\\end{equation}") < 0:
				in_lab_env = 0
				label_texts[label] = text
				text = ""

	tex_file.close()

print "<html>"
print "<head>"
print "<link rel=\"icon\" type=\"image/vnd.microsoft.icon\" href=\"stacks.ico\" />"
print "<title> Location of tag </title>"
print "</head>"
print "<body>"
print
print "<p align=left>"
print "<a href=\"index.html\">stacks project</a> | <a href=\"query.php\">search</a> | <a href=\"tags.html\">tags explained</a>"
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

# Make the array for chapters
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

# Make the array with the texts
print "$tag_text = array(\"ZZZZ\" => \"does not exist yet\");"
n = 0
while n < len(tags):
	tag = tags[n][0]
	label = tags[n][1]
	if label in label_texts:
		print "$tag_text[\"" + tag + "\"]=<<<\'END\'"
		print label_texts[label],
		print "END;"
	n = n + 1

# Change to upper case
print "$TAG=strtoupper($_GET[\"tag\"]);"

# Text the reader sees
print "echo \"<div style=\\\"margin-left: auto; margin-right: auto; text-align: left; width: 600px\\\">\\n\";"
print "if (array_key_exists($TAG, $tag_loc)) {"
print "echo \"Use tag \";"
print "echo $TAG;"
print "echo \" to reference:\\n\";"
print "echo \"<ul>\";"
print "echo \"<li><a href=\\\"\";"
print "echo $tag_loc_chap[$TAG];"
print "echo \", or</li>\\n\";"
print "echo \"<li><a href=\\\"book.pdf#\";"
print "echo $TAG;"
print "echo \"\\\">\";"
print "echo $tag_loc[$TAG];"
print "echo \"</a> of the book version.</li></ul>\\n\";"
print "if (array_key_exists($TAG, $tag_text)) {"
print "echo \"The latex code of the corresponding environment is:\\n\";"
print "echo \"<div style=\\\"font-family: monospace; text-align: left; display: table\\\">\\n\";"
print "echo \"<p>\\n\";"
print "echo $tag_text[$TAG];"
print "echo \"</p>\\n\";"
print "echo \"</div>\\n\";"
print "}"
print "}"
print "else"
print "{"
print "echo \"Tag $TAG does not exist.<br>\\n\";"
print "echo \"This may be because you mistyped it.<br>\\n\";"
print "echo \"Tags are 4 character strings of \";"
print "echo \"digits and letters.<br>\\n\";"
print "echo \"For more on tags click \";"
print "echo \"<a href=\\\"tags.html\\\">here</a>.\\n\";"
print "echo \"To try again click \";"
print "echo \"<a href=\\\"query.php\\\">here</a>.\\n\";"
print "}"
print "echo \"</div>\\n\";"
print "?>"
print
print "</body>"
print "</html>"
