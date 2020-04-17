# coded by sameera madushan
import argparse
import os
import re
import time
import hashlib
import requests
import sys
import gettext
import locale
from pathlib import Path
from os import path
from tkinter import Tk, filedialog

user_locale = locale.getdefaultlocale()[0]
lang = gettext.translation('messages', localedir='locales', languages=[user_locale])
lang.install()
_ = lang.gettext


def tk_get_file_path():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    try:
        with open(file_path, 'r'):
            pass
    except IOError:
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


def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
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
    header = {"user-agent": "SubDB/1.0 (SubtitleBOX/1.0; https://github.com/sameera-madushan/SubtitleBOX.git)"}
    req = requests.get(url, headers=header)
    if req.status_code == 200:
        k = req.content.decode('utf-8')
        available_languages = k.split(",")
        print(_("Subtitle files are available in following languages..."))
        for i in available_languages:
            for k, v in languages.items():
                if i == k:
                    print("     " + k + " (" + v + ")")
        return available_languages
    else:
        print(_("Oops!! Subtitle not found."))
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
        file_path = tk_get_file_path()
    else:
        file_path = cli_file_path
        if not path.exists(cli_file_path):
            print(_("File does not exist."))
            sys.exit()

    available_languages = request_subtitle_languages(file_path)

    # If no language code was given as CLI argument, ask it to the user
    if language_code_cli is None:
        selected_language = input(_("Choose your language (Please use language codes): ")).lower()
    else:
        selected_language = language_code_cli

    if selected_language in available_languages:
        url = create_url(file_path)
        search = re.sub(r'search', "download", url)
        final_url = search + "&language={}".format(selected_language)
        header = {"user-agent": "SubDB/1.0 (SubtitleBOX/1.0; https://github.com/sameera-madushan/SubtitleBOX.git)"}
        req = requests.get(final_url, headers=header)
        if req.status_code == 200:
            data = req.content
            download(file_path=file_path, data=data)
            print(_("Subtitle downloaded successfully"))
        else:
            print(_("Unknown Error"))
    else:
        print(_("Invalid language code selected. Please try again."))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SubtitleBOX CLI')
    parser.add_argument("-f", "--file_path",
                        help=_("Path of the video file for which subtitles should be looked for"))
    parser.add_argument("-lang", "--language_code",
                        help=_("Language code for subtitles. Can be en, es, fr, it, nl, pl, pt, ro, sv, tr"))

    args = parser.parse_args()

    main(args.file_path, args.language_code)
