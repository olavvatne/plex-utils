import os
import glob
import sys
from helper.filelist import delete_files, print_filenames, print_file
from helper.term import TermColor

detailed = False
if "detailed" in sys.argv:
    detailed = True

print("Plex library text files removal tool")

if detailed:
    print("Detailed mode. 1 line per file is printed")
print("Current directory is "  + os.getcwd())
print("")

applicable_files = []

#Assumes two level nesting only.
for folder in os.listdir(os.getcwd()):
    for filename in glob.glob(os.path.join(folder, '*.txt')):
        applicable_files.append(filename)

n = 10
if detailed:
    n = 1

#User presented with sublist to make bulk delete easier
chunks = [applicable_files[x:x+n] for x in range(0, len(applicable_files), n)]

#Filenames are printed and user is prompted to delete file.
for chunk in chunks:
    print_filenames(chunk)

    if detailed:
        lines = 1
        print_file(chunk, 1)

    user_choice = input(TermColor.OKGREEN + "Delete these files: y/N:" + TermColor.ENDC)

    if(str.lower(user_choice) == "y"):
        try:
            delete_files(chunk)
        except IOError as detail:
            print(detail)
            print(TermColor.FAIL + "Could not delete file" + TermColor.ENDC)
    elif(str.lower(user_choice) == "n" or not str.lower(user_choice)):
        continue
    else:
        break

print("Finished!")
