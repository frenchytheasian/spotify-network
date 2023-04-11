from Song import Song


class DetailedSong(Song):
    def __init__(self, uri, name, playlist = "None"):
        super().__init__(uri, name, playlist)
        self.artist = ""
        self.album = ""
        self.explicit = False
        self.genres = []
        self.popularity = 0
        self.accousticness = 0
        self.danceability = 0
        self.energy = 0
        self.instrumentalness = 0
        self.liveness = 0
        self.loudness = 0
        self.speechiness = 0
        self.tempo = 0
        self.valence = 0
        self.time_signature = 0
        self.tempo = 0
        self.mode = -1
        self.key = -1

    def __str__(self):
        return f"{self.name} by {self.artist}"

    def __repr__(self):
        return self.__str__()

    def set_audio_features(self, audio_features):
        self.accousticness = audio_features["accousticness"]
        self.danceability = audio_features["danceability"]
        self.energy = audio_features["energy"]
        self.instrumentalness = audio_features["instrumentalness"]
        self.liveness = audio_features["liveness"]
        self.loudness = audio_features["loudness"]
        self.speechiness = audio_features["speechiness"]
        self.tempo = audio_features["tempo"]
        self.valence = audio_features["valence"]
        self.time_signature = audio_features["time_signature"]
        self.tempo = audio_features["tempo"]
        self.mode = audio_features["mode"]
        self.key = audio_features["key"]

    def set_metadata(self, metadata):
        self.genres = metadata["genres"]
        self.explicit = metadata["explicit"]
        self.artist = metadata["artist"]
        self.album = metadata["album"]
        self.popularity = metadata["popularity"]

    def to_json(self) -> dict:
        return {
            **super().to_json(),
            "artist": self.artist,
            "album": self.album,
            "explicit": self.explicit,
            "genres": self.genres,
            "popularity": self.popularity,
            "accousticness": self.accousticness,
            "danceability": self.danceability,
            "energy": self.energy,
            "instrumentalness": self.instrumentalness,
            "liveness": self.liveness,
            "loudness": self.loudness,
            "speechiness": self.speechiness,
            "tempo": self.tempo,
            "valence": self.valence,
            "time_signature": self.time_signature,
            "tempo": self.tempo,
            "mode": self.mode,
            "key": self.key,
        }
