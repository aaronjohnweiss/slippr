
class User:
    name = ''
    tag = ''
    uri_name = ''
    rank = ''
    elo = 0

    def __init__(self, tag):
        self.tag = tag
        self.uri_name = tag.casefold().replace("#", "-")
