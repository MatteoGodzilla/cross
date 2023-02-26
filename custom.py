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

def CustomToDBColumns(custom:Custom) -> list[str]:
    columns = []
    if custom.IDTag != None:
        columns.append("IDTag")

    if custom.BPM != None:
        columns.append("BPM")

    if custom.DownloadLink != None:
        columns.append("DownloadLink")

    Songs = custom.Songs
    if Songs != None:
        for i in range(min(3,len(Songs))):
            if Songs[i].name != None:
                columns.append(f"Name{i+1}")
            if Songs[i].artist != None:
                columns.append(f"Artist{i+1}")

    if custom.Charter != None:
        columns.append("Charter")

    if custom.Mixer != None:
        columns.append("Mixer")

    diff = custom.Difficulties
    if diff != None:
        if diff.General != None:
            columns.append("DiffGeneral")
        if diff.Tap != None:
            columns.append("DiffTap")
        if diff.Crossfade != None:
            columns.append("DiffCrossfade")
        if diff.Scratch != None:
            columns.append("DiffScratch")

    Charts = custom.Charts
    if Charts != None:
        if Charts.Beginner != None:
            columns.append("HasBeginnerChart")
        if Charts.Easy != None:
            columns.append("HasEasyChart")
        if Charts.Medium != None:
            columns.append("HasMediumChart")
        if Charts.Hard != None:
            columns.append("HasHardChart")
        if Charts.Expert != None:
            columns.append("HasExpertChart")

    DeckSpeeds = custom.DeckSpeeds
    if DeckSpeeds != None:
        if DeckSpeeds.Beginner != None:
            columns.append("DeckSpeedBeginner")
        if DeckSpeeds.Easy != None:
            columns.append("DeckSpeedEasy")
        if DeckSpeeds.Medium != None:
            columns.append("DeckSpeedMedium")
        if DeckSpeeds.Hard != None:
            columns.append("DeckSpeedHard")
        if DeckSpeeds.Expert != None:
            columns.append("DeckSpeedExpert")

    if custom.VideoLink != None:
        columns.append("VideoLink")

    if custom.Notes != None:
        columns.append("Notes")

    return columns

def CustomToDBValues(custom:Custom) -> list[Any]:
    values = []
    if custom.IDTag != None:
        values.append(custom.IDTag)

    if custom.BPM != None:
        values.append(custom.BPM)

    if custom.DownloadLink != None:
        values.append(custom.DownloadLink)

    Songs = custom.Songs
    if Songs != None:
        for i in range(min(3,len(Songs))):
            if Songs[i].name != None:
                values.append(Songs[i].name)
            if Songs[i].artist != None:
                values.append(Songs[i].artist)

    if custom.Charter != None:
        values.append(custom.Charter)

    if custom.Mixer != None:
        values.append(custom.Mixer)

    diff = custom.Difficulties
    if diff != None:
        if diff.General != None:
            values.append(diff.General)
        if diff.Tap != None:
            values.append(diff.Tap)
        if diff.Crossfade != None:
            values.append(diff.Crossfade)
        if diff.Scratch != None:
            values.append(diff.Scratch)

    Charts = custom.Charts
    if Charts != None:
        if Charts.Beginner != None:
            values.append(Charts.Beginner)
        if Charts.Easy != None:
            values.append(Charts.Easy)
        if Charts.Medium != None:
            values.append(Charts.Medium)
        if Charts.Hard != None:
            values.append(Charts.Hard)
        if Charts.Expert != None:
            values.append(Charts.Expert)

    DeckSpeeds = custom.DeckSpeeds
    if DeckSpeeds != None:
        if DeckSpeeds.Beginner != None:
            values.append(DeckSpeeds.Beginner)
        if DeckSpeeds.Easy != None:
            values.append(DeckSpeeds.Easy)
        if DeckSpeeds.Medium != None:
            values.append(DeckSpeeds.Medium)
        if DeckSpeeds.Hard != None:
            values.append(DeckSpeeds.Hard)
        if DeckSpeeds.Expert != None:
            values.append(DeckSpeeds.Expert)

    if custom.VideoLink != None:
        values.append(custom.VideoLink)

    if custom.Notes != None:
        values.append(custom.Notes)

    return values