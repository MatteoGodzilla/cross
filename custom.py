import json

class Song:
    def __init__(self, values = []) -> None:
        if len(values) > 0:
            self.name : str = values[0]
            self.artist : str = values[1]
        else:
            self.name : str = ""
            self.artist : str = ""

class Difficulties:
    def __init__(self,values = []) -> None:
        if len(values) > 0:
            # 0 ... 255
            self.General = int(values[0])
            self.Tap = int(values[1])
            self.Crossfade = int(values[2])
            self.Scratch = int(values[3])
        else:
            self.General : int = 0
            self.Tap : int = 0
            self.Crossfade : int = 0
            self.Scratch : int = 0

class Charts:
    def __init__(self, values = []) -> None:
        if len(values) > 0:
            self.Beginner : bool = (values[0] == 1)
            self.Easy : bool = (values[1] == 1)
            self.Medium : bool = (values[2] == 1)
            self.Hard : bool = (values[3] == 1)
            self.Expert : bool = (values[4] == 1)
        else:
            self.Beginner = False
            self.Easy = False
            self.Medium = False
            self.Hard = False
            self.Expert = False

class DeckSpeeds:
    def __init__(self, values = []) -> None:
        if len(values) > 0:
            self.Beginner = float(values[0])
            self.Easy = float(values[1])
            self.Medium = float(values[2])
            self.Hard = float(values[3])
            self.Expert = float(values[4])
        else:
            self.Beginner = 1.0
            self.Easy = 1.0
            self.Medium = 1.0
            self.Hard = 1.0
            self.Expert = 1.0

class Custom:
    def __init__(self,values = []) -> None:
        print(values)
        # values should be the full row from the customs table
        # the filtering of values is done here
        if len(values) > 0:
            self.IDTag : str = values[1]
            self.BPM : float = values[2]
            self.DownloadLink : str = values[3]
            self.Songs : list[Song] = []
            if values[4] != "" and values[4] != None:
                self.Songs.append(Song(values[4:6]))
            if values[6] != "" and values[6] != None:
                self.Songs.append(Song(values[6:8]))
            if values[8] != "" and values[8] != None:
                self.Songs.append(Song(values[8:10]))
            self.Charter : str = values[10]
            self.Mixer : str = values[11]
            self.Difficulties : Difficulties = Difficulties(values[12:16])
            self.Charts : Charts = Charts(values[16:21])
            self.DeckSpeeds : DeckSpeeds = DeckSpeeds(values[21:26])
            self.VideoLink : str = values[26]
            self.Notes : str = values[27]
        else :
            # empty custom
            self.IDTag : str = ""
            self.BPM : float = ""
            self.DownloadLink : str = ""
            self.Songs : list[Song] = []
            self.Charter : str = ""
            self.Mixer : str = ""
            self.Difficulties : Difficulties = Difficulties()
            self.Charts : Charts = Charts()
            self.DeckSpeeds : DeckSpeeds = DeckSpeeds()
            self.VideoLink : str = ""
            self.Notes : str = ""

# JSON Encoders

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o,Custom):
            return {
                "IDTag" : o.IDTag,
                "BPM" : o.BPM,
                "DownloadLink" : o.DownloadLink,
                "Songs" : [vars(s) for s in o.Songs],
                "Charter" : o.Charter,
                "Mixer" : o.Mixer,
                "Difficulties" : vars(o.Difficulties),
                "Charts": vars(o.Charts),
                "DeckSpeeds" : vars(o.DeckSpeeds),
                "VideoLink" : o.VideoLink,
                "Notes" : o.Notes
            }
        return json.JSONEncoder.default(self,o)