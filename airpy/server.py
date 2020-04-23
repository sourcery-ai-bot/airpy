import hashlib
import json
import requests
import os
import sys

from pathlib import Path
from .music_folder import MusicFolder
from .indexes import Indexes
from .genres import GenreList

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

    def param_builder(self, **additional_params):
        params = []
        username = 'u=' + self.username
        token = 't=' + self.token
        salt = 's=' + self.salt
        api_version = 'v=' + self.api_version
        app = 'c=' + self.app
        style = 'f=json'
        params.extend((username, token, salt, api_version, app, style))
        parsed_additional_params = self.additional_param_parser(**additional_params)
        if parsed_additional_params != '':
            params.append(parsed_additional_params)
        return '&'.join(params)

    def additional_param_parser(self, **additional_params):
        parsed_params = []
        for param in additional_params:
            if additional_params[param] is not None:
                parsed_params.append(param + '=' + str(additional_params[param]))
        return '&'.join(parsed_params)

    def get(self, action, **additional_params):
        params = self.param_builder(**additional_params)
        url = self.host + '/rest/' + action + '?' + params
        r = requests.get(url).json()
        if r['subsonic-response']['status'] == 'ok':
            return r['subsonic-response']
        sys.exit()

    def ping(self):
        action = 'ping'
        return self.get(action)

    def get_music_folders(self):
        music_folders = []
        action = 'getMusicFolders'
        folders = self.get(action)['musicFolders']
        for folder in folders:
            music_folders.append(MusicFolder(folders[folder][0]))
        return music_folders

    def get_indexes(self, music_folder_id=None, if_modified_since=None):
        action = 'getIndexes'
        indexes = Indexes(self.get(action, musicFolderId=music_folder_id, ifModifiedSince=if_modified_since)['indexes'])
        return indexes

    def get_music_directory(self, music_folder_id=None):
        action = 'getMusicDirectory'
        files = self.get(action, id=music_folder_id)
        return files

    def get_genres(self):
        action = 'getGenres'
        genres = GenreList(self.get(action)['genres']['genre'])
        return genres
        