class Song:
    def __init__(self, uri, name, playlist):
        self.uri = uri
        self.name = name
        self.playlist = playlist

    def __eq__(self, other):
        return self.uri == other.uri

    def __hash__(self):
        return hash(self.uri)

    def to_json(self) -> dict:
        return {"name": self.name, "playlist": self.playlist}
