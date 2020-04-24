from .album import Album

class Artist:
    def __init__(self, info):
        self.id = info.get('id')
        self.name = info.get('name')
        self.cover_art = info.get('coverArt')
        self.album_count = info.get('albumCount')
        self.albums = self.parse_albums(info.get('album'))
        self.albums_by_release = self.parse_albums_by_release()

    def parse_albums(self, albums):
        parsed_albums = []
        for album in albums:
            parsed_albums.append(Album(album))
        return parsed_albums

    def parse_albums_by_release(self):
        return sorted(self.albums, key=lambda x: x.year)
        

