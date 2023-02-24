from pydantic import BaseModel
from typing import Any

class Song(BaseModel):
    name = ""
    artist = ""

class Difficulties(BaseModel):
    General = 0
    Tap = 0
    Crossfade = 0
    Scratch = 0

class Charts(BaseModel):
    Beginner = False
    Easy = False
    Medium = False
    Hard = False
    Expert = False

class DeckSpeeds(BaseModel):
    Beginner:float = 1.1
    Easy:float = 1.1
    Medium:float = 1.1
    Hard:float = 1.1
    Expert:float = 1.1

class Custom(BaseModel):
    IDTag:str|None
    BPM:float|None
    DownloadLink:str|None
    Songs:list[Song]|None
    Charter:str|None
    Mixer:str|None
    Difficulties:Difficulties|None
    Charts:Charts|None
    DeckSpeeds:DeckSpeeds|None
    VideoLink:str|None
    Notes:str|None

def CreateCustom(info:list[str]):
    custom = Custom()
    custom.IDTag=info[1]
    custom.BPM = float(info[2])
    custom.DownloadLink = info[3]
    custom.Songs = []

    for i in range(3):
        if info[i+4] != None and info[i+5] != None:
            s = Song()
            s.name = info[i+4]
            s.artist = info[i+5]
            custom.Songs.append(s)

    custom.Charter = info[10]
    custom.Mixer = info[11]

    custom.Difficulties = Difficulties()
    custom.Difficulties.General = int(info[12])
    custom.Difficulties.Tap = int(info[13])
    custom.Difficulties.Crossfade = int(info[14])
    custom.Difficulties.Scratch = int(info[15])

    custom.Charts = Charts()
    custom.Charts.Beginner = bool(info[16])
    custom.Charts.Easy = bool(info[17])
    custom.Charts.Medium = bool(info[18])
    custom.Charts.Hard = bool(info[19])
    custom.Charts.Expert = bool(info[20])

    custom.DeckSpeeds = DeckSpeeds()
    custom.DeckSpeeds.Beginner = float(info[21])
    custom.DeckSpeeds.Easy = float(info[22])
    custom.DeckSpeeds.Medium = float(info[23])
    custom.DeckSpeeds.Hard = float(info[24])
    custom.DeckSpeeds.Expert = float(info[25])

    custom.VideoLink = info[26]
    custom.Notes = info[27]

    return custom
