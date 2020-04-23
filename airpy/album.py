class AlbumList:
    def __init__(self, info):
        self.list = parse


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

    def __str__(self):
        return self.name
