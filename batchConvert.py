# dupFinder.py
import os
import sys
from shutil import move
from datetime import datetime
from hashlib import sha256

usage = 'Usage: python batchConvert.py folder or python [-t] dupFinder.py folder1 folder2 folder3'

def find_aifs(parentFolder):
    """ 
    Build and return an object with a key for each unique hash, and a 
    list of all matching files as its value: {hash:[names]}
    """
    aifs = []
    for dir_name, subdirs, fileList in os.walk(parentFolder):
        #print('Scanning %s...' % dir_name)
        for fullfilename in fileList:
            # Get the path to the file
            path = os.path.join(dir_name, fullfilename)
            basefilename, file_extension = os.path.splitext(fullfilename)
            if file_extension in ['.aif', '.aiff']:
            	# Add the file path if not present
							if not path in aifs:
									aifs.append(path)
            
    return aifs
 
 
def handle_results(aifs_list, testrun=0):
    """
    Get the FULL list of all found aif files and make mp3 versions using ffmpeg
    """
    print("There are {} aif files, first of which is {}, last is {}".format(len(all_aifs), all_aifs[0] \
    																																	, all_aifs[-1]))
 
def main(args): 
    """
    Do the work of the program if args provided, or exit and show usage.
    """
    if not len(args) > 1:
        print(usage)
        sys.exit()
    if args[1] == '-t':
        testrun = 1
        directories = args[2:]
    else:
        testrun = 0
        directories = args[1:]
    for dir in directories:
        # Iterate the folders given
        if os.path.exists(dir):
            # Find the duplicated files and append them to the dups
            all_aifs = find_aifs(dir)
        else:
            print('\'%s\' is not a valid path, please verify' % dir)
            sys.exit()
    handle_results(all_aifs, testrun)

if __name__ == '__main__':
    main(sys.argv)

