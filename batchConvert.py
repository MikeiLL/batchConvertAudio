# batchConvert.py
import os
import sys
import subprocess as sp
from optparse import OptionParser

FFMPEG_BIN = "ffmpeg" # on Linux ans Mac OS
# FFMPEG_BIN = "ffmpeg.exe" # on Windows

def find_aifs(parentFolder):
		""" 
		Build and return an object with a key for each unique hash, and a 
		list of all matching files as its value: {hash:[names]}
		"""
		aifs = []
		for dir_name, subdirs, fileList in os.walk(parentFolder):
				print('Scanning %s...' % dir_name)
				for fullfilename in fileList:
						# Get the path to the file
						path = os.path.join(dir_name, fullfilename)
						basefilename, file_extension = os.path.splitext(fullfilename)
						if file_extension in ['.aif', '.aiff']:
								# Add the file path if not present
								if not path in aifs:
										aifs.append(path)
		return aifs
 
 
def handle_results(aifs_list, options):
		"""
		Get the FULL list of all found aif files and make wav versions using ffmpeg
		"""
		
		if options.examine == True:
				print("There are {} aif files, first of which is {}, last is {}".format(len(aifs_list), aifs_list[0] \
																																			, aifs_list[-1]))
				sys.exit()
		
		for aif in aifs_list:		
				basename = os.path.basename(aif)
				basefilename, file_extension = os.path.splitext(basename)
				save_to = os.path.dirname(aif) + "/" + basefilename + '.' + options.format
				print(save_to)
				if not os.path.exists(save_to):
						command_mp3 = [ FFMPEG_BIN,
												'-i', str(aif),
												'-f', 'mp3',
												'-acodec', 'libmp3lame',
												'-ab', str(192000),
												'-ar', str(44100), save_to
												]
						command_wav = [ FFMPEG_BIN,
											 '-i', str(aif),  
											 save_to
											 ]
											 
						print("Creating file {}".format(save_to))
						if not options.testing == True:
								if options.format == 'wav':
										pipe = sp.Popen(command_wav, stdout = sp.PIPE, bufsize=10**8)
								else:
										pipe = sp.Popen(command_mp3, stdout = sp.PIPE, bufsize=10**8)
						else:
								if options.format == 'wav':
										print("Testing: {}".format(command_wav))
								else:
										print("Testing: {}".format(command_mp3))

def get_options(warn=False):
    usage = "usage: %s [options] directory_containing_aif_files" % sys.argv[0]
    parser = OptionParser(usage=usage)
    parser.add_option("-t", "--test", action="store_true", dest="testing", help="Don't actually create the new files.")
    parser.add_option("-e", "--examine", action="store_true", dest="examine", help="Count number of files in specified dirs.")
    parser.add_option("-f", "--format", default='mp3', help="output format default=mp3 - other option is 'wav'")
    
    (options, args) = parser.parse_args()
    if warn and len(args) < 1: 
        parser.print_help()
    return (options, args)
     
def main(args): 
		"""
		Do the work of the program if args provided, or exit and show usage.
		"""
		options, args = get_options(warn=True)
		aifs = []
		print(options)
		print(args)
		for dir in args:
				# Iterate the folders given
				print(dir)
				if os.path.exists(dir):
						# strip trailing slash if exists
						dir = dir.rstrip('/')
						# Find the aif files and extend aifs list
						some_aifs = find_aifs(dir)
						print("1. {}".format(some_aifs))
						print("2. {}".format(aifs))
						aifs.extend(some_aifs)
						print("3. {}".format(aifs))
				else:
						print('\'%s\' is not a valid path, please verify' % dir)
						sys.exit()
		handle_results(aifs, options)

if __name__ == '__main__':
    main(sys.argv)

