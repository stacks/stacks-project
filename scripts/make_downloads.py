from functions import *

path = get_path()

downloads = open(path + "downloads", 'r')

odd = 0
for line in downloads:
	if not line.find("INSERT HERE") == 0:
		print line,
		continue
	
	import os
	ttt = os.popen('git ls-files')
	for t in ttt:
		if odd:
			print "<tr class=\"dark\">"
			odd = 0
		else:
			print "<tr class=\"light\">"
			odd = 1
			
		print "<td>" + t + "</td>"
		print "<td class=\"link\"><a href=\"" + t + "\">" + t + "</a></td>"
		print "</tr>"

