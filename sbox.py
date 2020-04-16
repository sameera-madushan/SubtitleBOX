# coded by sameera madushan
import argparse
import os
import re
import time
import hashlib
import requests
import sys
from pathlib import Path
from os import path
from tkinter import Tk, filedialog
import numpy as np


def tk_get_file_path():
    root = Tk()
    root.withdraw()
    
    file_path = root.tk.splitlist(
        filedialog.askopenfilenames(parent=root, title='Choose a file'))
    if not file_path:
        print("Cancelled")
        sys.exit()

    try:
        for file in file_path:
            with open(file, 'r') as f:
                pass
    except:
        print("Cancelled")
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
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()


def create_url(file_path):
    film_hash = get_hash(name=file_path)
    url = "http://api.thesubdb.com/?action=search&hash={}".format(film_hash)
    return url


def request_subtitle_languages(file_path):
    url = create_url(file_path)
    header = {
        "user-agent": "SubDB/1.0 (SubtitleBOX/1.0; https://github.com/sameera-madushan/SubtitleBOX.git)"}
    req = requests.get(url, headers=header)
    if req.status_code == 200:
        k = req.content.decode('utf-8')
        available_languages = k.split(",")
        return available_languages
    else:
        print("Oops!! Subtitle not found.")
        sys.exit()


def download(file_path, data):
    # from https://www.reddit.com/user/panzerex/
    filename = Path(file_path).with_suffix('.srt')
    with open(filename, 'wb') as f:
        f.write(data)
    f.close()


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
            print("File does not exist.")
            sys.exit()

    # Check, which languages appears in all requested episodes
    all_available_languages = []
    for file_path in files_path:
        all_available_languages.append(request_subtitle_languages(file_path))

    availability_in_all = []
    for _lang in lang:
        availability_in_all.append(all((_lang in x)
                                       for x in all_available_languages))
    available_languages = np.asarray(lang)[availability_in_all]

    try:
        if len(files_path) == 1:
            print("\nSubtitle file are available in following languages...\n")
        elif len(files_path) > 1:
            print(
                "\nSubtitle file for all selected files are available in following languages...\n")
    except:
        print("\nError\n")

    for i in available_languages:
        for k, v in languages.items():
            if i == k:
                print("     " + k + " (" + v + ")")

    # If no language code was given as CLI argument, ask it to the user
    if language_code_cli is None:
        selected_language = input(
            "\nChoose your language (Please use language codes): ").lower()
    else:
        selected_language = language_code_cli

    if selected_language in available_languages:
        for index, file_path in enumerate(files_path):
            url = create_url(file_path)
            search = re.sub(r'search', "download", url)
            final_url = search + "&language={}".format(selected_language)
            header = {
                "user-agent": "SubDB/1.0 (SubtitleBOX/1.0; https://github.com/sameera-madushan/SubtitleBOX.git)"}
            req = requests.get(final_url, headers=header)
            if req.status_code == 200:
                data = req.content
                download(file_path=file_path, data=data)
                print(
                    f"\n{index+1}/{len(files_path)} Subtitle downloaded successfully")
            else:
                print("\nUnknown Error")
    else:
        print("\nInvalid language code selected. Please try again.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SubtitleBOX CLI')
    parser.add_argument("-f", "--file_path",
                        help="Path of the video file for which subtitles should be looked for")
    parser.add_argument("-lang", "--language_code",
                        help="Language code for subtitles. Can be en, es, fr, it, nl, pl, pt, ro, sv, tr")

    args = parser.parse_args()

    main(args.file_path, args.language_code)
