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
						basefilename, file_extension = os.path.splitext(fullfilename)
						the_mp3 = dir_name + "/" + basefilename + '.mp3'
						the_wav = dir_name + "/" + basefilename + '.aif'
						print(the_mp3)
						if os.path.exists(the_mp3):
								if os.path.getsize(the_mp3) == 0:
										print("Removing zero-byte file: {}".format(the_mp3))
										os.remove(the_mp3)
								else:
										size_rendered_file = os.path.getsize(the_mp3)
										try:
												size_orignal_file = os.path.getsize(the_wav)
												print("{} / {} is {}".format(size_orignal_file, size_rendered_file, size_orignal_file / size_rendered_file))
												if size_orignal_file / size_rendered_file > 15:
														# Add the file path if not present
														if not path in probably_broken:
																probably_broken.append(path)
																print("{} is probably broken.".format(the_mp3))
										except OSError:
												print("OS Error, maybe there is no aif file")
		return probably_broken

def delete_bad_files(broken, testrun=1):
		"""
		Get a list of file paths and if not testrun, delete them.
		"""
		print("{} files probably broken starting with {} and ending with {}".format(len(broken), broken[0], broken[-1]))
		count = 1
		if not testrun:
				print("Delete all suspect files? y/N")
				confirm = raw_input()
				if not confirm.lower() == 'y':
						print("Exiting as per {}".format(confirm.lower()))
						sys.exit()
				for file in broken:
						print("Bad file {} exists: {}. Removing.".format(file, os.path.exists(file)))
						os.remove(file)
						count += 1
				print("Deleted {} files, this programmed evaluated as broken mp3 encodings".format(count))
		else:
				print("Had this not been a test, they all would have been deleted.")
		return 0
		
def main(args): 
		"""
		Do the work of the program if args provided, or exit and show usage.
		"""
		if not len(args) > 1:
				print(usage)
				sys.exit()
		broken = []
		if args[1] == '-t':
				testrun = 1
				directories = args[2:]
		else:
				testrun = 0
				directories = args[1:]
		for dir in directories:
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
		delete_bad_files(broken, testrun)
						
if __name__ == '__main__':
		main(sys.argv)