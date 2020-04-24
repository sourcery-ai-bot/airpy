from .song import Song

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
        parsed_songs = []
        for song in songs:
            parsed_songs.append(Song(song))
        return sorted(parsed_songs, key=lambda x: x.track)