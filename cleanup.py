import os


def find_and_remove(path, pattern, maxdepth=5):
	""" Searches a directory and its subdirectories to remove all of a file type """
	cpath = path.count(os.sep)
	for r, d, f in os.walk(path):
		if r.count(os.sep) - cpath < maxdepth:
			for files in f:
				if files.endswith(pattern):
					try:
						#print "Removing %s" % (os.path.join(r, files))
						os.remove(os.path.join(r, files))
					except Exception, e:
						print e
					else:
						pass
						#print "%s removed" % (os.path.join(r, files))


def run():
	""" Auto run main method """
	find_and_remove("../../", ".pyc")


if __name__ == "__main__":
	run()
