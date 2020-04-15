# coded by sameera madushan

import os
import re
import time
import hashlib
import requests
import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog


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

def tk_get_file_path():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    try:
        with open(file_path, 'r') as f:
            pass
    except:
        print("Cancelled")
        sys.exit()

    return file_path


file_path = tk_get_file_path()

languages = {
    "en" : "English",
    "es" : "Spanish",
    "fr" : "French",
    "it" : "Italian",
    "nl" : "Dutch",
    "pl" : "Polish",
    "pt" : "Portuguese",
    "ro" : "Romanian",
    "sv" : "Swedish",
    "tr" : "Turkish"
}

def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()

def create_url():
    film_hash = get_hash(name=file_path)
    url = "http://api.thesubdb.com/?action=search&hash={}".format(film_hash)
    return url

def request_subtitile():
    url = create_url()
    header = { "user-agent": "SubDB/1.0 (SubtitleBOX/1.0; https://github.com/sameera-madushan/SubtitleBOX.git)" }
    req = requests.get(url, headers=header)
    if req.status_code == 200:
        k = req.content.decode('utf-8')
        global l 
        l = k.split(",")
        print("\nSubtitle files are available in following languages...\n")
        for i in l:
            for k,v in languages.items():
                if i == k:
                    print("     " + k + " (" + v + ")")
    else:
        print("Oops!! Subtitle not found.")
        exit()

def download(data):
    # from https://www.reddit.com/user/panzerex/
    filename = Path(file_path).with_suffix('.srt')
    with open(filename, 'wb') as f:
        f.write(data)
    f.close()

request_subtitile()

while True:
    try:
        select_langauge = input("\nChoose your langauge (Please use language codes): ").lower()
        if select_langauge in l:
            url = create_url()
            search = re.sub(r'search', "download", url)
            final_url = search + "&language={}".format(select_langauge)
            header = { "user-agent": "SubDB/1.0 (SubtitleBOX/1.0; https://github.com/sameera-madushan/SubtitleBOX.git)" }
            req = requests.get(final_url, headers=header)
            if req.status_code == 200:
                data = req.content
                download(data=data)
                print("\nSubtitle downloaded successfully")
                break
            else:
                print("\nUnknown Error")
                break
        else:
            print("\nInvalid language code selected. Please try again.")
            
    except KeyboardInterrupt:
        print("\nProgramme Interrupted")
        break
        
