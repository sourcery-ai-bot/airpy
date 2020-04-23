class GenreList:
    def __init__(self, genre_list):
        self.list = self.parse_genres(genre_list)

    def parse_genres(self, genre_list):
        parsed_genres = []
        for genre in genre_list:
            parsed_genres.append(Genre(genre))
        return parsed_genres

    def by_name(self):
        genres = self.list
        return sorted(genres, key=lambda x: x.name.lower())

    def by_song_count(self):
        genres = self.list
        return sorted(genres, key=lambda x: x.song_count, reverse=True)

    def by_album_count(self):
        genres = self.list
        return sorted(genres, key=lambda x: x.album_count, reverse=True)


class Genre:
    def __init__(self, info):
        self.song_count = info.get('songCount')
        self.album_count = info.get('albumCount')
        self.name = info.get('value')

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name