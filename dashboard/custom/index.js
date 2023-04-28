async function GetLatestCustoms(){
    let customsTable = document.querySelector("#customs tbody")
    customsTable.innerHTML = ""

    ids = await fetch(`/api/v1/custom/latest/`).then(res => res.json())
    //console.log(ids)

    for(id of ids){
        json = await fetch(`/api/v1/custom/${id}`).then(res => res.json());
        //console.log(json)
        customsTable.appendChild(CustomToTable(json,id))
    }
}

function CustomToTable(json,id)
{
	// Initializing the row that will contain the JSON object
	const row = document.createElement("tr");

    //database id
    let data = document.createElement("td")
    data.textContent = id
    row.appendChild(data)

    //IDTag
    data = document.createElement("td")
    data.textContent = json.IDTag
    row.appendChild(data)

    //BPM
    data = document.createElement("td")
    data.textContent = json.BPM.toString()
    row.appendChild(data)

    //songs
    data = document.createElement("td")
    if(json.Songs.length > 0){
        for(let i = 0; i < json.Songs.length; i++){
            let song = json.Songs[i]
            data.textContent += `${song.name} / ${song.artist}`
            if(i + 1 <json.Songs.length )
                data.textContent += " ⇌\n"
        }
    } else {
        data.textContent = "empty"
    }
    row.appendChild(data)

    //Charter
    data = document.createElement("td")
    if(json.Charter){
        data.textContent = json.Charter
    } else {
        data.textContent = "null"
    }
    row.appendChild(data)

    //Mixer
    data = document.createElement("td")
    if(json.Charter){
        data.textContent = json.Mixer
    } else {
        data.textContent = "null"
    }
    row.appendChild(data)

    //Difficulties
    data = document.createElement("td")
    data.textContent = json.Difficulties.General
    row.appendChild(data)

    data = document.createElement("td")
    data.textContent = json.Difficulties.Tap
    row.appendChild(data)

    data = document.createElement("td")
    data.textContent = json.Difficulties.Crossfade
    row.appendChild(data)

    data = document.createElement("td")
    data.textContent = json.Difficulties.Scratch
    row.appendChild(data)

    //Charts
    data = document.createElement("td")
    if(json.Charts.Beginner)
        data.classList = "available"
    else
        data.classList = "notAvailable"
    data.textContent = json.DeckSpeeds.Beginner
    row.appendChild(data)

    data = document.createElement("td")
    if(json.Charts.Easy)
        data.classList = "available"
    else
        data.classList = "notAvailable"
    data.textContent = json.DeckSpeeds.Easy
    row.appendChild(data)

    data = document.createElement("td")
    if(json.Charts.Medium)
        data.classList = "available"
    else
        data.classList = "notAvailable"
    data.textContent = json.DeckSpeeds.Medium
    row.appendChild(data)

    data = document.createElement("td")
    if(json.Charts.Hard)
        data.classList = "available"
    else
        data.classList = "notAvailable"
    data.textContent = json.DeckSpeeds.Hard
    row.appendChild(data)

    data = document.createElement("td")
    if(json.Charts.Expert)
        data.classList = "available"
    else
        data.classList = "notAvailable"
    data.textContent = json.DeckSpeeds.Expert
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

    //Video link
    data = document.createElement("td")
    if(json.VideoLink){
        anchor = document.createElement("a")
        anchor.href = json.VideoLink
        anchor.text = "Video link"
        data.append(anchor)
    } else {
        data.textContent = "null"
    }
    row.appendChild(data)

    //notes
    data = document.createElement("td")
    data.textContent = json.Notes
    row.appendChild(data)

	//In the end, return the newly created row
	return row;
}

GetLatestCustoms()