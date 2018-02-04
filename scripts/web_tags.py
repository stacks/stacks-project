from functions import *

path = get_path()
parts = get_parts(path)
for part in parts:
    print parts[part][2] + "," + parts[part][1]
print "ZZZY,index-section-phantom"
