from typing import Any
from pydantic import BaseModel

class Megamix(BaseModel):
    Name = ""
    Customs:list[int] = []
    DownloadLink:str|None = ""
    VideoPreview:str|None = ""

# info is only coming from the table `megamix`
def CreateMegamix(info:list[str]):
    megamix = Megamix()
    megamix.Name = info[1]
    megamix.DownloadLink = info[2]
    megamix.VideoPreview = info[3]
    # we cannot fill megamix.Customs just yet, we need another api request
    return megamix

# This does not consider the junction table `megamix-customs`
def MegamixToDBColumns(megamix:Megamix) -> list[str]:
    res = ["Name"]

    if megamix.DownloadLink != None:
        res.append("DownloadLink")

    if megamix.VideoPreview != None:
        res.append("VideoPreview")

    return res

# This does not consider the junction table `megamix-customs`
def MegamixToDBValues(megamix:Megamix)->list[Any]:
    res = [megamix.Name]

    if megamix.DownloadLink != None:
        res.append(megamix.DownloadLink)

    if megamix.VideoPreview != None:
        res.append(megamix.VideoPreview)

    return res
