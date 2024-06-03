from functions import *

# Preamble for the web-book to be parsed by plastex
# All refs are internal in canonical form
# documentclass book
# load amsmath package for plastex
# Ignore reference, slogan, history environments
# Do not bother with multicol and xr-hyper pacakges
def print_preamble(path):
	preamble = open(path + "preamble.tex", 'r')
	next(preamble)
	next(preamble)
	next(preamble)
	next(preamble)
	next(preamble)
	print("\\documentclass{book}")
	print("\\usepackage{amsmath}")
	for line in preamble:
		if line.find("%") == 0:
			continue
		if line.find("externaldocument") >= 0:
			continue
		if line.find("\\newenvironment{reference}") >= 0:
			continue
		if line.find("\\newenvironment{slogan}") >= 0:
			continue
		if line.find("\\newenvironment{history}") >= 0:
			continue
		if line.find("multicol")>= 0:
			continue
		if line.find("xr-hyper") >= 0:
			continue
		print(line, end = '')
	preamble.close()
	return

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
print("\\end{titlepage}")
print_license_blurp(path)

lijstje = list_text_files(path)

parts = get_parts(path)

ext = ".tex"
for name in lijstje:
	if name in parts:
		print("\\part{" + parts[name][0] + "}")
		print("\\label{" + parts[name][1] + "}")

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

print("\\bibliography{my}")
print("\\bibliographystyle{amsalpha}")
print("\\end{document}")
