import os

def delete_files(file_list):
    for f in file_list:
        os.remove(f)

def print_file(file_list, nr_lines):
    if file_list and len(file_list) > 0:
        f = open(file_list[0], 'r')
        print(f.readlines(nr_lines))

def print_filenames(file_list):
    for f in file_list:
        print(os.path.basename(f))
