class ArtistList:
    def __init__(self, info):
        self.ignored_articles = info.get('ignoredArticles')
        self.alpha_list = self.parse_letters(info.get('index'))
        self.list = self.drop_letter_index()

    def parse_letters(self, index):
        parsed_letters = []
        for letter in index:
            parsed_letters.append(Letter(letter))
        return parsed_letters

    def drop_letter_index(self):
        artists = []
        for letter in self.alpha_list:
            for artist in letter.artists:
                artists.append(artist)
        return artists

class Letter:
    def __init__(self, info):
        self.name = info.get('name')
        self.artists = self.parse_artists(info.get('artist'))

    def __str__(self):
        return self.name

    def parse_artists(self, artists):
        parsed_artists = []
        for artist in artists:
            parsed_artists.append(Artist(artist))
        return parsed_artists

class Artist:
    def __init__(self, info):
        self.id = info.get('id')
        self.name = info.get('name')
        self.cover_art = info.get('coverArt')
        self.album_count = info.get('albumCount')

    def __str__(self):
        return self.name