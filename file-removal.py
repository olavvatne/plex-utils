import os
import glob
import sys
from helper.filelist import delete_files, print_filenames, print_file
from helper.term import TermColor

print("Plex library unecessary files removal tool")
print("Current directory is "  + os.getcwd())
print("")

applicable_files = []
patterns = ["*/sample.*", "*/*.nfo", "*/WWW*.jpg", "*/*.txt", "*/*.website" ]
#Assumes two level nesting only.
curr_dir = os.getcwd()
for pattern in patterns:
    applicable_files.extend(glob.glob(os.path.join(curr_dir, pattern)))

#Filenames are printed and user is prompted to delete file.
for f in applicable_files:
    print(os.path.relpath(f))
    print_filenames([f])

    user_choice = input(TermColor.OKGREEN + "Delete this file: y/N:" + TermColor.ENDC)

    if(str.lower(user_choice) == "y"):
        try:
            delete_files([f])
        except IOError as detail:
            print(detail)
            print(TermColor.FAIL + "Could not delete file" + TermColor.ENDC)
    elif(str.lower(user_choice) == "n" or not str.lower(user_choice)):
        continue
    else:
        break

print("Finished!")
