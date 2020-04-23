class Index:
    def __init__(self, info):
        self.last_modified = info.get('lastModified', None)
        self.ignored_articles = info.get('ignoredArticles', None)
        self.letters = self.parse_letters(info.get('index', [{}]))

    def parse_letters(self, alpha_list):
        letters = []
        for letter in alpha_list:
            letters.append(Letter(letter))
        return letters


class Letter:
    def __init__(self, info):
        self.name = info.get('name')
        self.artists = self.parse_artists(info.get('artist'))

    def __str__(self):
        return self.name

    def parse_artists(self, artists):
        parsed_artists = []
        for artist in artists:
            parsed_artists.append(ArtistByLetter(artist))
        return parsed_artists


class ArtistByLetter:
    def __init__(self, info):
        self.id = info.get('id')
        self.name = info.get('name')

    def __str__(self):
        return self.name