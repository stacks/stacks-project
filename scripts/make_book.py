from functions import *

# Preamble for the book does not have external references
# Use the CJKutf8
# Use stacks-project-book if available
# Use amsbook otherwise
def print_preamble(path):
	preamble = open(path + "preamble.tex", 'r')
	for line in preamble:
		if line.find("%") == 0:
			continue
		if line.find("externaldocument") >= 0:
			continue
		if line.find("xr-hyper") >= 0:
			line = line.replace("xr-hyper", "CJKutf8")
		if line.find("\\IfFileExists{") == 0:
			line = line.replace("stacks-project", "stacks-project-book")
		if line.find("\\documentclass") == 0:
			line = line.replace("amsart", "amsbook")
			line = line.replace("stacks-project", "stacks-project-book")
		print(line, end = '')
	preamble.close()
	return

# Print names contributors
def print_list_contrib(path):
	filename = path + 'CONTRIBUTORS'
	CONTRIBUTORS = open(filename, 'r')
	first = 1
	for line in CONTRIBUTORS:
		if line.find("%") == 0:
			continue
		if len(line.rstrip()) == 0:
			continue
		contributor = line.rstrip()
		contributor = contributor.replace("(", "(\\begin{CJK}{UTF8}{min}")
		contributor = contributor.replace(")", "\\end{CJK})")
		if first:
			contributors = contributor
			first = 0
			continue
		contributors = contributors + ", " + contributor
	CONTRIBUTORS.close()
	contributors = contributors + "."
	print(contributors)

path = get_path()

print_preamble(path)

print("\\begin{document}")
print("\\begin{titlepage}")
print("\\pagestyle{empty}")
print("\\setcounter{page}{1}")
print("\\centerline{\\LARGE\\bfseries Stacks Project}")
print("\\vskip1in")
print("\\noindent")
print("\\centerline{")
print_version(path)
print("}")
print("\\vskip1in")
print("\\noindent")
print("The following people have contributed to this work:")
print_list_contrib(path)
print("\\end{titlepage}")
print_license_blurp(path)

lijstje = list_text_files(path)
lijstje.append("index")

parts = get_parts(path)

ext = ".tex"
for name in lijstje:
	if name in parts:
		print("\\part{" + parts[name][0] + "}")
	if name == "index":
		filename = path + "tmp/index.tex"
	else:
		filename = path + name + ext
	tex_file = open(filename, 'r')
	verbatim = 0
	for line in tex_file:
		verbatim = verbatim + beginning_of_verbatim(line)
		if verbatim:
			if end_of_verbatim(line):
				verbatim = 0
			if name != 'introduction':
				print(line, end = '')
			continue
		if line.find("\\input{preamble}") == 0:
			continue
		if line.find("\\begin{document}") == 0:
			continue
		if line.find("\\title{") == 0:
			line = line.replace("\\title{", "\\chapter{")
		if line.find("\\maketitle") == 0:
			continue
		if line.find("\\tableofcontents") == 0:
			continue
		if line.find("\\input{chapters}") == 0:
			continue
		if line.find("\\bibliography") == 0:
			continue
		if line.find("\\end{document}") == 0:
			continue
		if is_label(line):
			text = "\\label{" + name + "-"
			line = line.replace("\\label{", text)
		if contains_ref(line):
			line = replace_refs(line, name)
		print(line, end = '')

	tex_file.close()
	print_chapters(path)

print("\\bibliography{my}")
print("\\bibliographystyle{amsalpha}")
print("\\end{document}")
