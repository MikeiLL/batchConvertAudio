import os
import sys

usage = 'Usage: python findBrokenMP3s.py folder'

def find_broken_mp3s(parentFolder):
		""" 
		Build and return an object with a key for each unique hash, and a 
		list of all matching files as its value: {hash:[names]}
		"""
		probably_broken = []
		for dir_name, subdirs, fileList in os.walk(parentFolder):
				print('Scanning {}...'.format(dir_name))
				for fullfilename in fileList:
						# Get the path to the file
						path = os.path.join(dir_name, fullfilename)
						size_orignal_file = os.path.getsize(path)
						basefilename, file_extension = os.path.splitext(fullfilename)
						the_mp3 = os.path.dirname(fullfilename) + "/" + basefilename + '.mp3'
						if os.path.exists(the_mp3):
								size_rendered_file = os.path.getsize(the_mp3)
								if size_orignal_file / size_rendered_file > 15:
										# Add the file path if not present
										if not path in probably_broken:
												probably_broken.append(path)
												print(the_mp3)
		return probably_broken
		
def main(args): 
		"""
		Do the work of the program if args provided, or exit and show usage.
		"""
		if not len(args) > 1:
				print(usage)
				sys.exit()
		broken = []
		for dir in args:
				# Iterate the folders given
				if os.path.exists(dir):
						# strip trailing slash if exists
						dir = dir.rstrip('/')
						# Find the aif files and extend aifs list
						some_aifs = find_broken_mp3s(dir)
						broken.extend(some_aifs)
				else:
						print('\'%s\' is not a valid path, please verify' % dir)
						sys.exit()
						
		print("{} files probably".format(len(broken)))

if __name__ == '__main__':
		main(sys.argv)