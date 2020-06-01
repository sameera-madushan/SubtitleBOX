# coded by sameera madushan
#Important: During development and for tests purposes, please use http://sandbox.thesubdb.com/ as the API url.

import os
import re
import sys
import time
import locale
import hashlib
import gettext
import requests
import argparse
import numpy as np
from os import path
from pathlib import Path
from tkinter import Tk, filedialog

locales_path = sys.path[0] + '/locales'
try:
    user_locale = locale.getdefaultlocale()[0]
    lang = gettext.translation('messages', localedir=locales_path, languages=[user_locale])
    lang.install()
    _ = lang.gettext
except FileNotFoundError:
    lang = gettext.translation('messages', localedir=locales_path, languages=["en_US"])
    lang.install()
    _ = lang.gettext


def tk_get_file_path():
    """
    This function will ask the user for the movie file/s and return the 
    file path/s of them. Tkinter module is used to show the File dialog. 

    Parameters
    ----------
    None
    """

    root = Tk()
    root.withdraw()

    file_path = root.tk.splitlist(
        filedialog.askopenfilenames(parent=root, title='Choose a file'))
    if not file_path:
        print(_("Cancelled"))
        sys.exit()

    try:
        for file in file_path:
            with open(file, 'r') as f:
                pass
    except IOError:
        print(_("Cancelled"))
        sys.exit()

    return file_path


languages = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "it": "Italian",
    "nl": "Dutch",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "sv": "Swedish",
    "tr": "Turkish"
}
lang = list(languages.keys())


def get_hash(name):
    """
    This function receives the name of the file and returns the hash code
    Hash is composed by taking the first and the last 64kb of the video file, 
    putting all together and generating a md5 of the resulting data (128kb).

    Parameters
        ----------
        name : str
            The path of the movie file/s. 
    """

    readsize = 64 * 1024
    with open(name, 'rb') as f:
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()


def create_url(file_path):
    """
    This function will append the hash generated in get_hash function
    to the subtitle search URL and return the URL

    Parameters
    ----------
    file_path : str
        The path of the movie file/s. 
    """

    film_hash = get_hash(name=file_path)
    url = "http://api.thesubdb.com/?action=search&hash={}".format(film_hash)
    return url


def request_subtitle_languages(file_path):
    """
    Return a list with all the available languages in which
    subs are available for a file.
    Return None is no subs are available.

    Parameters
    ----------
       file_path : str
           The path of the file/s for which sub/s should be found.
    """

    url = create_url(file_path)
    header = {"user-agent": "SubDB/1.0 (SubtitleBOX/1.0; https://github.com/sameera-madushan/SubtitleBOX.git)"}
    req = requests.get(url, headers=header)
    if req.status_code == 200:
        k = req.content.decode('utf-8')
        available_languages = k.split(",")
        return available_languages
    else:
        available_languages = None
        return available_languages


def download(file_path, data):
    """
    This function download the subtitle file from SubDB database.
    Filename of the subtitle file will be same as the movie name and append '.srt' extention at the end.

    Pythonic approach for filename generation is by https://www.reddit.com/user/panzerex/

    Parameters
    ----------
       file_path : str
           The path of the file/s for which sub/s should be found.

        data : bytes
            Binary data of the subtitle file.
    """

    filename = Path(file_path).with_suffix('.srt')
    with open(filename, 'wb') as f:
        f.write(data)
    f.close()


def check_existence_of_subtitles(files_path):
    """
    Check if there exists at least one subtitle available for every
    file in files_path.

    If a file is not a video file or is corrupted, abort and exit.
    Otherwise, returns 3 output parameters:
        1 - List of all available languages for each selected file.
        2 - A list of Booleans, True if subtitles for specific file exists and False if not.
        3 - The sequence number of the file whose subtitles do not exist.

    Parameters
    ----------
       files_path : str
           The path containing all the files for which subs should
           be found.
    """

    all_available_languages_selection = []
    bool_find_subtitles = np.ones(
        len(files_path), dtype=bool)
    loc_none = []
    for i, file_path in enumerate(files_path):
        try:
            found_languages = request_subtitle_languages(file_path)
            all_available_languages_selection.append(found_languages)
            if found_languages == None:
                loc_none.append(i)
                bool_find_subtitles[i] = False
        except:
            print(_("The selected file cannot be used to find subtitles:"))
            print(f" x {os.path.basename(file_path)}")
            print(_("Cancelled"))
            sys.exit()
    return all_available_languages_selection, bool_find_subtitles, loc_none


def select_files_with_subtitles(all_files, bool_loc):
    """
    Returns the selected elements from the all_file list that are selected 
    based on the values of the elements in bool_loc (list of Booleans)

    Parameters
    ----------
       all_files : list
           The path containing all the files for which subs should
           be found. Or a list of all available languages for each selected file.
        
        bool_loc : list
            List of Booleans, True if subtitles for specific file exists and False if not.
    """

    return np.asarray(all_files)[bool_loc]


def get_common_languages_for_all_files(all_available_languages_selection, lang):
    """
    This function checks which common languages are available for all selected files.
    Returns a list of common languages.

    Parameters
    ----------
       all_available_languages_selection : list
           List containing all the languages available for the individual 
           files for which subtitles exist at all.
        
        lang : list
            List of all language codes that can be found in the database.
    """

    availability_in_all_files = []
    if all_available_languages_selection.size > 0:
        for _lang in lang:
            availability_in_all_files.append(all((_lang in x)
                                                 for x in all_available_languages_selection))
        return np.asarray(lang)[availability_in_all_files]
    else:
        print(_("There is no common language available for the selected files."))
        sys.exit()


def main(cli_file_path, language_code_cli):
    banner = r'''
         ___     ___     ___   __  __  
        / __|   | _ )   / _ \  \ \/ /  
        \__ \   | _ \  | (_) |  >  <   
        |___/   |___/   \___/  /_/\_\  
        _|"""""|_|"""""|_|"""""|_|"""""| 
        "`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'  
                 Subtitles BOX    
    '''

    print(banner)
    time.sleep(1)

    # If no file path was given as CLI argument, show the dialog window and ask for a file.
    if cli_file_path is None:
        files_path = tk_get_file_path()
    else:
        files_path = (cli_file_path,)
        if not path.exists(cli_file_path):
            print(_("File does not exist."))
            sys.exit()

    # Check, which files do and do not have subtitle file
    files_with_available_subs, find_subtitles, loc_none = check_existence_of_subtitles(
        files_path)

    # Check, which languages appears in all requested episodes
    all_available_languages = select_files_with_subtitles(
        files_with_available_subs, find_subtitles)
    available_languages = get_common_languages_for_all_files(
        all_available_languages, lang)

    if False in find_subtitles:
        print(_("Subtitle file is not available for following files:"))
        print("\n", end="")
        for i in loc_none:
            print(f" x {os.path.basename(files_path[i])}")
        if True in find_subtitles:
            print("________________________________________________________\n")

    files_path = select_files_with_subtitles(files_path, find_subtitles)

    print(_("Subtitles are available for following files:"))
    print("\n", end="")
    for file in files_path:
        print(f" - {os.path.basename(file)}")
    print("\n", end="")

    try:
        if len(files_path) == 1:
            print(_("Subtitles are available in following languages..."))
            print("\n", end="")
        elif len(files_path) > 1:
            print(_("Subtitles for all selected files are available in following languages..."))
            print("\n", end="")
    except:
        print(_("Error"))

    for i in available_languages:
        for k, v in languages.items():
            if i == k:
                print("     " + "\u2022" + " " + k + " (" + v + ")")
    print("\n", end="")

    # If no language code was given as CLI argument, ask it to the user
    if language_code_cli is None:
        selected_language = input(
            _("Choose your language (Please use language codes): ")).lower()
    else:
        selected_language = language_code_cli

    if selected_language in available_languages:
        for index, file_path in enumerate(files_path):
            url = create_url(file_path)
            search = re.sub(r'search', "download", url)
            final_url = search + "&language={}".format(selected_language)
            header = {"user-agent": "SubDB/1.0 (SubtitleBOX/1.0; https://github.com/sameera-madushan/SubtitleBOX.git)"}
            req = requests.get(final_url, headers=header)
            if req.status_code == 200:
                data = req.content
                download(file_path=file_path, data=data)
                print(f"\n{index+1}/{len(files_path)}" + " " +
                      _("Subtitle downloaded successfully"))
            else:
                print("\n", end="")
                print(_("Unknown Error"))
    else:
        print("\n", end="")
        print(_("Invalid language code selected. Please try again."))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SubtitleBOX CLI')
    parser.add_argument("-f", "--file_path",
                        help=_("Path of the video file for which subtitles should be looked for"))
    parser.add_argument("-lang", "--language_code",
                        help=_("Language code for subtitles. Can be en, es, fr, it, nl, pl, pt, ro, sv, tr"))

    args = parser.parse_args()

    main(args.file_path, args.language_code)
