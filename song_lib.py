import glob
import os
from itertools import *
import random
import re
from bs4 import BeautifulSoup
import requests


AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36'
HEADERS = {'User-Agent': AGENT}
BASE = "https://www.azlyrics.com/"


class Song:
    def __init__(self, artist, title, lyric):
        self.artist = artist
        self.title = title
        self.lyric = lyric


class SongLib:
    def __init__(self):
        self.songs = {}
        cwd = os.getcwd()
        os.chdir(cwd + "/song_library")
        for file in glob.glob("*.txt"):
            lines = [line.rstrip('\n') for line in open(file)]
            self.songs[file.split('.')[0]] = lines

    def get_random_song(self, artist=''):
        songs = self.songs
        keys = list(songs.keys())
        if not artist:
            rand_artist = random.randint(0, len(keys)-1)
            artist = keys[rand_artist]
        elif artist not in keys:
            print('Error: Unable to find ' + artist)
            return Song(artist, '', ['Error:', 'Unable to find ' + artist])

        song_list = songs.get(artist)
        rand_song = random.randint(0, len(song_list)-1)
        song = song_list[rand_song]
        return lyrics(artist, song)

    @staticmethod
    def get_song(artist, title):
        return lyrics(artist, title)

    def delete_song(self, song):
        file = song.artist + '.txt'
        try:
            f = open(file, 'r')
        except FileNotFoundError:
            return

        lines = f.readlines()
        f.close()
        f = open(file, 'w')

        for line in lines:
            if line != song.title + '\n':
                f.write(line)

    def get_song_from_url(self, url):
        return load_url(url)


def lyrics(artist, song):
    if artist.lower().startswith('the '):
        artist = artist[3:]
    artist = re.sub(r'[^a-z0-9]', '', artist)

    song = song.lower().replace(" ", "")
    song = re.sub(r'[^a-z0-9]', '', song)
    url = BASE + "lyrics/" + artist + "/" + song + ".html"
    return load_url(url, song=song, artist=artist)


def load_url(url, song='', artist=''):
    try:
        req = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(req.content, "html.parser")
        lyrics = soup.find_all("div", attrs={"class": None, "id": None})

    except Exception:
        print('Error: Unable to load ' + url)
        return Song(artist, song, ['Error:', 'Unable to load ' + url])
    if not lyrics:
        if song and artist:
            print('Error: Unable to find '+song+' by '+artist)
            return Song(artist, song, ['Error:', 'Unable to find '+song+' by '+artist])
        else:
            print('Error: Unable to load ' + url)
            return Song(artist, song, ['Error:', 'Unable to load ' + url])
    elif lyrics:
        song = ''
        if not song:
            head = soup.text.replace('\r', '').split('\n')[:50]
            artist = next((x for x in head if x.startswith('ArtistName')), None).split('"')[1]
            song = next((x for x in head if x.startswith('SongName')), None).split('"')[1]

        lyrics = [x.getText() for x in lyrics]
        lyrics = lyrics[0].replace('\n', ' ')

        lyrics = lyrics.replace('.', '')
        lyrics = lyrics.replace(',', '')
        lyrics_list = lyrics.split(' ')
        lyrics_list = list(filter(lambda a: a != '' and a != '-', lyrics_list))
        return Song(artist, song, lyrics_list[1:])



