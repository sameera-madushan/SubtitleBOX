# coded by sameera madushan

import os
import re
import time
import hashlib
import requests
import sys
import ctypes
import clr 
from System.Windows.Forms import OpenFileDialog


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

# got this from https://stackoverflow.com/a/58861718/13276219
def file_path():
    co_initialize = ctypes.windll.ole32.CoInitialize
    co_initialize(None)

    clr.AddReference('System.Windows.Forms')
    
    file_dialog = OpenFileDialog()
    ret = file_dialog.ShowDialog()
    if ret != 1:
        print("Cancelled")
        sys.exit()
    return file_dialog.FileName

file_path = file_path()

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

request_subtitile()

def download(data):
    filename = file_path[:-4]
    with open(filename + ".srt", 'wb') as f:
        f.write(data)
    f.close()

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
        

        
