class MusicFolder:
    def __init__(self, info):
        self.id = info.get('id')
        self.name = info.get('name')

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Music Folder: ' + self.name