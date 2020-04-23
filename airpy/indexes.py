class Indexes:
    def __init__(self, info):
        self.last_modified = info.get('lastModified')
        self.ignored_articles = info.get('ignoredArticles', None)
        self.alphabetical_list = info.get('index', [{}])

    def parse_index(self):
        for letter in self.alphabetical_list:
            Index(letter)


class Index:
    def __init__(self, info):
        self.name = info.get('name')
        self.artists = info.get('artist')
