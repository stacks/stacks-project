from functions import *

path = get_path()

tags = get_tags(path)

new_tags = get_new_tags(path, tags)

print "Writing ",
print len(new_tags),
print " new tags."

write_new_tags(path, new_tags)
