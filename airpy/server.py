import hashlib
import json
import requests
import os
import sys

import settings as setting

from pathlib import Path

class Server:
    def __init__(self):
        self.api_version = "1.15.0"
        self.app = "airpy"
        self.host = setting.host
        self.username = setting.username
        self.password = setting.password
        self.salt = setting.salt
        self.pass_and_salt = self.password + self.salt
        self.token = hashlib.md5(self.pass_and_salt.encode("utf-8")).hexdigest()
        self.format = "mp3"
        self.estimate_content_length = "true"
        self.max_bitrate = "128"
        self.music_path = setting.music_path

    def __str__(self):
        return self.host

    def __repr__(self):
        return self.host

    def param_builder(self, **kwargs):
        params = []
        username = 'u=' + self.username
        token = 't=' + self.token
        salt = 's=' + self.salt
        api_version = 'v=' + self.api_version
        app = 'c=' + self.app
        style = 'f=json'
        params.extend((username, token, salt, api_version, app, style))
        parsed_additional_params = self.additional_param_parser(**kwargs)
        if parsed_additional_params != '':
            params.append(parsed_additional_params)
        return '&'.join(params)

    def additional_param_parser(self, **kwargs):
        parsed_params = [
            param + '=' + str(kwargs[param])
            for param in kwargs
            if kwargs[param] is not None
        ]

        return '&'.join(parsed_params)

    def get(self, action, **kwargs):
        params = self.param_builder(**kwargs)
        url = self.host + '/rest/' + action + '?' + params
        r = requests.get(url).json()
        if r['subsonic-response']['status'] == 'ok':
            return r['subsonic-response']
        else:
            print(r['subsonic-response'])
            sys.exit()

    def get_stream(self, action, **kwargs):
        params = self.param_builder(**kwargs)
        url = self.host + '/rest/' + action + '?' + params
        return requests.get(url, stream=True).content

    def ping(self):
        action = 'ping'
        return self.get(action)

    def get_music_folders(self):
        return MusicFolderList(self.get('getMusicFolders')['musicFolders'])

    def get_indexes(self, **kwargs):
        return Index(self.get('getIndexes', **kwargs)['indexes'])

    def get_music_directory(self, *, id):
        return self.get('getMusicDirectory', id=id)

    def get_genres(self):
        return GenreList(self.get('getGenres')['genres']['genre'])

    def get_artists(self, **kwargs):
        return ArtistList(self.get('getArtists')['artists'])

    def get_artist(self, *, id):
        return Artist(self.get('getArtist', id=id)['artist'])

    def get_album(self, *, id):
        return Album(self.get('getAlbum', id=id)['album'])

    def get_song(self, *, id):
        return Song(self.get('getSong', id=id)['song'])


class Album:
    def __init__(self, info):
        self.id = info.get('id')
        self.name = info.get('name')
        self.artist = info.get('artist')
        self.artist_id = info.get('artistId')
        self.cover_art = info.get('coverArt')
        self.song_count = info.get('songCount')
        self.duration = info.get('duration')
        self.created = info.get('created')
        self.year = info.get('year')
        self.genre = info.get('genre')
        self.songs = self.parse_songs(info.get('song', []))

    def __str__(self):
        return self.name

    def parse_songs(self, songs):
        parsed_songs = [Song(song) for song in songs]
        return sorted(parsed_songs, key=lambda x: x.track)


class Artist:
    def __init__(self, info):
        self.id = info.get('id')
        self.name = info.get('name')
        self.cover_art = info.get('coverArt')
        self.album_count = info.get('albumCount')
        self.albums = self.parse_albums(info.get('album'))
        self.albums_by_release = self.parse_albums_by_release()

    def parse_albums(self, albums):
        return [Album(album) for album in albums]

    def parse_albums_by_release(self):
        return sorted(self.albums, key=lambda x: x.year)
        
class ArtistList:
    def __init__(self, info):
        self.ignored_articles = info.get('ignoredArticles')
        self.alpha_list = self.parse_letters(info.get('index'))
        self.list = self.drop_letter_index()

    def parse_letters(self, index):
        return [Letter(letter) for letter in index]

    def drop_letter_index(self):
        artists = []
        for letter in self.alpha_list:
            for artist in letter.artists:
                artists.append(artist)
        return artists

class GenreList:
    def __init__(self, genre_list):
        self.list = self.parse_genres(genre_list)

    def parse_genres(self, genre_list):
        return [Genre(genre) for genre in genre_list]

    def by_name(self):
        return sorted(self.list, key=lambda x: x.name.lower())

    def by_song_count(self):
        return sorted(self.list, key=lambda x: x.song_count, reverse=True)

    def by_album_count(self):
        return sorted(self.list, key=lambda x: x.album_count, reverse=True)


class Genre:
    def __init__(self, info):
        self.song_count = info.get('songCount')
        self.album_count = info.get('albumCount')
        self.name = info.get('value')

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Index:
    def __init__(self, info):
        self.last_modified = info.get('lastModified', None)
        self.ignored_articles = info.get('ignoredArticles', None)
        self.letters = self.parse_letters(info.get('index', [{}]))

    def parse_letters(self, alpha_list):
        return [Letter(letter) for letter in alpha_list]


class IndexArtist:
    def __init__(self, info):
        self.id = info.get('id')
        self.name = info.get('name')

    def __str__(self):
        return self.name


class Letter:
    def __init__(self, info):
        self.name = info.get('name')
        self.artists = self.parse_artists(info.get('artist'))

    def __str__(self):
        return self.name

    def parse_artists(self, artists):
        return [IndexArtist(artist) for artist in artists]


class MusicFolder:
    def __init__(self, info):
        self.id = info.get('id')
        self.name = info.get('name')

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Music Folder: ' + self.name


class MusicFolderList:
    def __init__(self, music_folder_list):
        self.list = self.parse_music_folder_list(music_folder_list)

    def parse_music_folder_list(self, folders):
        return [MusicFolder(folders[folder][0]) for folder in folders]
        

class Song:
    def __init__(self, info):
        self.id = info.get('id')
        self.parent = info.get('parent')
        self.is_dir = info.get('isDir')
        self.title = info.get('title')
        self.album = info.get('album')
        self.artist = info.get('artist')
        self.track = info.get('track')
        self.year = info.get('year')
        self.genre = info.get('genre')
        self.cover_art = info.get('coverArt')
        self.size = info.get('size')
        self.content_type = info.get('contentType')
        self.suffix = info.get('suffix')
        self.transcoded_content_type = info.get('transcodedContentType')
        self.transcoded_suffix = info.get('transcodedSuffix')
        self.duration = info.get('duration')
        self.bitrate = info.get('bitRate')
        self.path = info.get('path')
        self.is_video = info.get('isVideo')
        self.play_count = info.get('playCount')
        self.disc_number = info.get('discNumber')
        self.created = info.get('created')
        self.album_id = info.get('albumId')
        self.artist_id = info.get('artistId')
        self.type = info.get('type')
        self.cache_dir = './.songs'
        self.cache_file = self._cached_file()
        self.cached = False

    def __str__(self):
        return self.title
           
    def _cached_file(self):
        server = Server()
        return (self.cache_dir + '/' +
                       self.artist + ' - ' + 
                       self.album + ' - ' +
                       str(self.track) + ' - ' +
                       self.title + '.' + 
                       server.format)

    
    def play(self):
        if self.cached:
            cache_file = '"' + self.cache_file + '"'
            os.system('play -q ' + cache_file)
        else:
            self.cache()
            self.play()

    def cache(self):
        if not os.path.exists(self.cache_file):
            Path(self.cache_file).touch()
            if not os.path.exists(self.cache_dir):
                os.mkdir(self.cache_dir)
            server = Server()
            data = server.get_stream('stream',
                                    id=self.id,
                                    format=server.format,
                                    maxBitRate=server.max_bitrate)
            with open (self.cache_file, 'wb') as fd:
                fd.write(data)
                fd.close()
        self.cached = True 