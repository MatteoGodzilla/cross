class Song:
    def __init__(self) -> None:
        self.name : str = ""
        self.artist : str = ""

class Difficulties:
    def __init__(self) -> None:
        # 0 ... 255
        self.General : int = 0
        self.Tap : int = 0
        self.Crossfade : int = 0
        self.Scratch : int = 0

class Charts:
    def __init__(self) -> None:
        self.Beginner : bool = False
        self.Easy : bool = False
        self.Medium : bool = False
        self.Hard : bool = False
        self.Expert : bool = False

class DeckSpeeds:
    def __init__(self) -> None:
        self.Beginner : float = 1
        self.Easy : float = 1
        self.Medium : float = 1
        self.Hard : float = 1
        self.Expert : float = 1

class Custom:
    def __init__(self) -> None:
        self.IDTag : str = ""
        self.BPM : float = 0.0
        self.DownloadLink : str = ""
        self.Songs : list[Song] = []
        self.Charter : str = ""
        self.Mixer : str = ""
        self.Difficulties : Difficulties = Difficulties()
        self.Charts : Charts = Charts()
        self.DeckSpeeds : DeckSpeeds = DeckSpeeds()
        self.VideoLink : str = ""
        self.Notes : str = ""
