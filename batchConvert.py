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
 
 
def join_dicts(dict1, dict2):
    """
    Combine two dictionaires, by adding to key in dict one if exists, or creating a new key if not.

    We use this to create a single hash-keyed dictionary of all files sent to the scripts.
    """
    for key in dict2.keys():
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]
 
 
def hashfile(path, blocksize = 65536):
    """
    Create a sha256 hash instance from a file by reading the binary data in blocks of 2**16 bytes 
    and updating hash accordingly.
    """
    with open(path, 'rb') as afile:
        hasher = sha256()
        while True: 
            buf = afile.read(blocksize)
            if not buf:
                break
            hasher.update(buf)
    return hasher.hexdigest()
 
 
def handle_results(dict1, testrun=0):
    """
    Get the BIG dictionary of all files per hash, and remove all but the first copy of each duplicate
    file as compared by sha256 hash.
    """
    #Make a list of all the files for which there is more than one per hash
    results = list(filter(lambda x: len(x) > 1, dict1.values()))
    if not testrun:
    	backupdir = 'removed_' + str(datetime.now())
    	if not os.path.exists(backupdir):
    		os.makedirs(backupdir)
    else:
	    backupdir = 'backup_dir_date_now'
    if len(results) > 0:
        print('Duplicates Found:')
        print('The following files are identical. The name could differ, but the content is identical')
        print('^^^^^^^^^^^^^^^^^')
        count = 0
        for result in results:
            for subresult in result:
                if count == 0:
                    print('KEEPING ONE COPY: %s.' % subresult)
                    count += 1
                elif testrun:
                    print('\t\t %s WILL BE REMOVED TO: %s' % (subresult, backupdir))
                    count += 1
                else:
                    print('\t\tREMOVING %s TO %s' % (subresult, backupdir))
                    try:
                        move(subresult, backupdir)
                    except shutil.Error:
                        print ('\t\t EXISTS. DELETING.')
                        os.remove(subresult)
                    print('___________________')
    else:
        print('No duplicate files found.')
 
def main(args): 
    """
    Do the work of the program if args provided, or exit and show usage.
    """
    if not len(args) > 1:
        print(usage)
        sys.exit()
    aifs = {}
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
            print("There are {} aif files, first of which is {}".format(len(all_aifs), all_aifs[0]))
        else:
            print('\'%s\' is not a valid path, please verify' % dir)
            sys.exit()
    handle_results(aifs, testrun)

if __name__ == '__main__':
    main(sys.argv)

