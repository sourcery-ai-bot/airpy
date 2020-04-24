import hashlib
import json
import requests
import os
import sys

from pathlib import Path
from airpy.music_folder import MusicFolder
from airpy.index import Index
from airpy.genres import GenreList
from airpy.artistslist import ArtistList
from airpy.artist import Artist
from airpy.album import Album

import settings as setting


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
        parsed_params = []
        for param in kwargs:
            if kwargs[param] is not None:
                parsed_params.append(param + '=' + str(kwargs[param]))
        return '&'.join(parsed_params)

    def get(self, action, **kwargs):
        params = self.param_builder(**kwargs)
        url = self.host + '/rest/' + action + '?' + params
        r = requests.get(url).json()
        if r['subsonic-response']['status'] == 'ok':
            return r['subsonic-response']
        sys.exit()

    def ping(self):
        action = 'ping'
        return self.get(action)

    def get_music_folders(self):
        return self.get('getMusicFolders')['musicFolders']

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