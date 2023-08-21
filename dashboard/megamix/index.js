async function GetLatestMegamixes(){
    let megamixTable = document.querySelector("#megamixes tbody")
    megamixTable.innerHTML = ""

    ids = await fetch(`/api/v1/megamix/latest/`).then(res => res.json())
    console.log(ids)

    for(id of ids){
        json = await fetch(`/api/v1/megamix/${id}`).then(res => res.json())
        console.log(json)
        megamixTable.appendChild(await MegamixToTable(json,id))
    }
}

async function MegamixToTable(json,id){
    let row = document.createElement("tr")

    //Id
    let data = document.createElement("td")
    data.textContent = id
    row.appendChild(data)

    //Name
    data = document.createElement("td")
    data.textContent = json.Name
    row.appendChild(data)

    //Customs
    data = document.createElement("td")
    data.textContent = ""
    for(let id of json.Customs){
        let customJson = await fetch(`/api/v1/custom/${id}`).then(res => res.json())
        if(data.textContent != "")
            data.textContent += ", "
        data.textContent += customJson.IDTag
    }
    row.appendChild(data)

    //Download Link
    data = document.createElement("td")
    if(json.DownloadLink){
        let anchor = document.createElement("a")
        anchor.href = json.DownloadLink
        anchor.text = "Download Link"
        data.append(anchor)
    } else{
        data.textContent = "null"
    }
    row.appendChild(data)

    //Video Link
    data = document.createElement("td")
    if(json.VideoPreview){
        let a = document.createElement("a")
        a.href = json.VideoPreview
        a.text = "Video Link"
        data.appendChild(a)
    } else {
        data.textContent = "null"
    }
    row.appendChild(data)

    return row
}

GetLatestMegamixes()