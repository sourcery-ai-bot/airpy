class MusicFolderList:
    def __init__(self, music_folder_list):
        self.list = self.parse_music_folder_list(music_folder_list)

    def parse_music_folder_list(self, music_folder_list):
        music_folders = []
        for folder in music_folder_list:
            music_folders.append(MusicFolder(folders[folder][0]))
        return music_folders
        

class MusicFolder:
    def __init__(self, info):
        self.id = info.get('id')
        self.name = info.get('name')

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Music Folder: ' + self.name