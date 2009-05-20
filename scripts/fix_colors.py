from functions import *


from sys import argv
if not len(argv) == 3:
	print
	print "This script needs exactly two arguments"
	print "namely the path to the stacks project"
	print "and the stem of the tex file"
	print
	raise Exception('Wrong arguments')

path = argv[1]
path.rstrip("/")
path = path + "/"

name = argv[2]


filename = path + name

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

file.close()
