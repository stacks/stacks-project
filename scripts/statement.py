import os

name='test'

cmd = 'latex ' + name + '.tex'

os.system(cmd)

cmd = 'dvipng -D 100 -T tight -x 1000 -z 9 -bg Transparent -o '
cmd += name + '.png ' + name + '.dvi'

os.system(cmd)
