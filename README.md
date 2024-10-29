# SBOX - Subtitle Box

SBOX is a python script to download subtitles for your movies from [SubDB](http://thesubdb.com/) database using their API. SubDB is a free, centralized subtitle database intended to be used only by opensource and non-commercial softwares. 

Please Note: Subtitle file will be downloaded in to the same folder as the correspondent video file.

## Features
- [x] Download subtitle files of different languages.
- [x] Download subtitles for multiple movies at once.
- [x] Command line mode for terminal users.

![ezgif com-gif-maker](https://user-images.githubusercontent.com/55880211/79194420-21ebc280-7e4a-11ea-84b2-f155d43dcd0a.gif)

## Git Installation
```
# clone the repo
$ git clone https://github.com/sameera-madushan/SubtitleBOX.git

# change the working directory to SubtitleBOX
$ cd SubtitleBOX

# install the requirements
$ pip3 install -r requirements.txt
```
## (OSX/Linux only) Install tkinter
If you are running python 3.7 or later, nothing has to be done. Earlier python3 versions require installation.
```
# Debian/Ubuntu
$ sudo apt install python3-tk

# macOS
# Follow the instructions on https://tkdocs.com/tutorial/install.html
```

## Usage

```
python sbox.py
```

```
usage: sbox.py [-h] [-f FILE_PATH] [-lang LANGUAGE_CODE]

SubtitleBOX CLI

optional arguments:
  -h, --help            show this help message and exit
  -f FILE_PATH, --file_path FILE_PATH
                        Path of the video file for which subtitles should be
                        looked for
  -lang LANGUAGE_CODE, --language_code LANGUAGE_CODE
                        Language code for subtitles. Can be en, es, fr, it,
                        nl, pl, pt, ro, sv, tr
```
## Contributors

Thanks goes to these wonderful people. :heart:

<table>
  <tr>
    <td align="center"><a href="https://github.com/JonathanPartain"><img src="https://avatars0.githubusercontent.com/u/12885700?s=400&u=242fea5b8de20586e1ae174056b7aa9fc04d95d6&v=4" width="100px;" alt=""/><br /><sub><b>Jonathan Partain</b></sub></a></td>
    <td align="center"><a href="https://github.com/AlexMV12"><img src="https://avatars1.githubusercontent.com/u/36054651?s=400&v=4" width="100px;" alt=""/><br /><sub><b>Alessandro Falcetta</b></sub></a></td>
    <td align="center"><a href="https://github.com/DarkCeptor44"><img src="https://avatars2.githubusercontent.com/u/16278483?s=400&u=1ebc14a87bd6f2e4df0cb1ff90f178cb1ea1beef&v=4" width="100px;" alt=""/><br /><sub><b>Murilo Pagliuso</b></sub></a></td>
    <td align="center"><a href="https://github.com/mihakodric"><img src="https://avatars0.githubusercontent.com/u/32506231?s=400&v=4" width="100px;" alt=""/><br /><sub><b>mihakodric</b></sub></a></td>
    <td align="center"><a href="https://github.com/NBrown140"><img src="https://avatars1.githubusercontent.com/u/9956767?s=400&u=e4f68c09d01d986fa133a713ce4e8013c68db3a2&v=4" width="100px;" alt=""/><br /><sub><b>Nicolas Brown</b></sub></a></td>

</table>
