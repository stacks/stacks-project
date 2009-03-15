from functions import *

path = get_path()

filename = path + "stacks-git.htm"

file = open(filename, 'r')

dark = 1
dark_text = "<tr class=\"dark\">"
light_text = "<tr class=\"light\">"

for line in file:
	if line.find(dark_text) >= 0 or line.find(light_text) >= 0:
		if dark:
			print dark_text
			dark = 0
		else:
			print light_text
			dark = 1
	else:
		print line,
