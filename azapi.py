from bs4 import BeautifulSoup
import requests
import json
import re

agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36'
headers = {'User-Agent': agent}
base = "https://www.azlyrics.com/"


def artists(letter):
    if letter.isalpha() and len(letter) is 1:
        letter = letter.lower()
        url = base+letter+".html"
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.content, "html.parser")
        data = []

        for div in soup.find_all("div", {"class": "container main-page"}):
            links = div.findAll('a')
            for a in links:
                data.append(a.text.strip())
        return json.dumps(data)
    else:
        raise Exception("Unexpected Input")


def songs(artist):
    artist = artist.lower().replace(" ", "")
    first_char = artist[0]
    url = base+first_char+"/"+artist+".html"
    req = requests.get(url, headers=headers)

    artist = {
        'artist': artist,
        'albums': {}
        }

    soup = BeautifulSoup(req.content, 'html.parser')

    all_albums = soup.find('div', id='listAlbum')
    first_album = all_albums.find('div', class_='album')
    album_name = first_album.b.text
    songs = []

    for tag in first_album.find_next_siblings(['a', 'div']):
        if tag.name == 'div':
            artist['albums'][album_name] = songs
            songs = []
            if tag.b is None:
                pass
            elif tag.b:
                album_name = tag.b.text

        else:
            if tag.text is "":
                pass
            elif tag.text:
                songs.append(tag.text)

    artist['albums'][album_name] = songs

    return json.dumps(artist)


def lyrics(artist, song):
    artist = artist.lower().replace(" ", "")
    artist = re.sub(r'[^a-z0-9]', '', artist)
    song = song.lower().replace(" ", "")
    song = re.sub(r'[^a-z0-9]', '', song)
    url = base+"lyrics/"+artist+"/"+song+".html"


def load_url(url, song='', artist=''):
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.content, "html.parser")
    lyrics = soup.find_all("div", attrs={"class": None, "id": None})
    if not lyrics:
        if song and artist:
            print('Error: Unable to find '+song+' by '+artist)
            return {'Error': 'Unable to find '+song+' by '+artist}
        else:
            print('Error: Unable to load ' + url)
            return {'Error: Unable to load ' + url}
    elif lyrics:
        lyrics = [x.getText() for x in lyrics]
        lyrics = lyrics[0].replace('\n', ' ')

        lyrics = lyrics.replace('.', '')
        lyrics = lyrics.replace(',', '')
        lyrics_list = lyrics.split(' ')
        lyrics_list = list(filter(lambda a: a != '' and a != '-', lyrics_list))
        return lyrics_list[1:]


