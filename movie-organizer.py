import os, glob, sys, itertools, datetime, re
from helper.filelist import delete_files, print_filenames, print_file
from helper.term import TermColor

print("Plex library movie and subtitle organizer")
print("Current directory is "  + os.getcwd())
print("")

def get_all_files_flatten(path, exts):
    nested = [glob.glob(os.path.join(path, "**."+ x)) for x in exts]
    return list(itertools.chain.from_iterable(nested))

def is_valid(movie):
    if len(movie) <= 0:
        print("Did not detect any movie")
        return False
    elif len(movie) > 1:
        print("More than one movie file")
        return False
    try:
        year = get_year(os.path.basename(movie[0]))
    except Exception:
        return False
    return True;

def get_year(filename):
    curr_year = datetime.date.today().year;
    match = re.findall(r'([1-9][0-9]{3})', filename)

    if match is not None:
        min_year = 1889

        for m in match:
            year = int(m)
            if (min_year < year < curr_year+1):
                return year
    raise ValueError("Does not contain a valid year")

def get_formatted_title(filename, year):
    #Assumes file start with title of the movie, and then list year.
    if str(year) not in filename:
        return None

    idx = filename.find(str(year))
    title = filename[0:idx]

    ugly_ending = title[-1]
    if (ugly_ending == "(" or ugly_ending == "."):
        title=title[0:-1]
    title = title.replace(".", " ").strip() #TODO Only punctation without whitespace afterwards
    return title + " (" + str(year) + ")"

def rename_folder(path, new_path):
    os.rename(path, new_path)

curr_dir = os.getcwd()
movies = os.listdir(curr_dir)
movie_ext = ["mkv", "avi", "mp4"]
sub_ext = [ "srt", "smi"]

for movie in movies:
    path = os.path.join(curr_dir, movie)

    if (not is_valid([movie])):
        continue

    year = get_year(movie)
    new_title = get_formatted_title(movie, year)

    if (movie == new_title):
        continue

    print("Rename folder:")
    print("--  " + movie)
    print("to: " + new_title)
    user_choice = input(TermColor.OKGREEN + "Rename folder: y/N:" + TermColor.ENDC)

    if(str.lower(user_choice) == "y"):
        try:
            rename_folder(path, os.path.join(curr_dir, new_title))
        except IOError as detail:
            print(detail)
            print(TermColor.FAIL + "Could not rename file" + TermColor.ENDC)
    elif(str.lower(user_choice) == "n" or not str.lower(user_choice)):
        continue
    else:
        break
    #Do not rename subs and movie files. TODO: are filename used by plex?
    #subs_files = get_all_files_flatten(path, sub_ext)
    #movie_files = get_all_files_flatten(path, movie_ext)

    #if (is_valid(movie_files)):
    #    mov = movie_files[0]
    #    year = get_year(mov)
    #    new_title = get_formatted_title(mov, year)
print("Finished!")
