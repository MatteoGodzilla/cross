function AddCustom(){
	//MISSING CHECK IMPORTANT PARAMETERS LOGIC
	alert("ADD")
}

function EditCustom(){
	//MISSING CHECK IMPORTANT PARAMETERS LOGIC
	alert("EDIT")
}

async function GetLatest(){
    latestCustoms = document.querySelector("#show")
    latestCustoms.innerHTML = ""

    ids = await fetch(`/api/v1/custom/latest/`).then(res => res.json())
    console.log(ids)
    for(id of ids){
        json = await fetch(`/api/v1/custom/${id}`).then(res => res.json());
        latestCustoms.appendChild(CustomToPage(json,id))
    }
}

function CustomToPage(custom,id){
    //console.log(custom)
    div = document.createElement("div")
    str = `${id}: ${custom.IDTag} / `
    for(song of custom.Songs){
        str += `${song.name} by ${song.artist}, `
    }
    div.innerText = str

    return div
}

function CSTM_JSONToTable(json)
{
	// From JSON to Javascript object
	var myObj = JSON.parse(json);

	// Initializing the row that will contain the JSON object
	const row = document.createElement("tr");

	// keys => simply the description of the content in the right column (PROBABLY DEPRECATED)
	//var keys = ["BPM:", "DownloadLink:", "Songs:", "Charter:", "Mixer:", "Difficulties:", "Charts:", "DeckSpeeds:", "VideoLink:", "Notes:"];

	// values => the data content of the JSON that we are going to write in the right column
	var values = [myObj.BPM, myObj.DownloadLink, myObj.Songs, myObj.Charter, myObj.Mixer, myObj.Difficulties, myObj.Charts, myObj.DeckSpeeds, myObj.VideoLink, myObj.Notes];

	// Creating the table structure
	for(let c = 0; c < 10; c++)
	{
		const col = document.createElement("td");

		if(c == 2 || (c >= 5 && c <= 7))
		{
			const customs = document.createElement("ul");
			for(x in values[c])
			{
				const ls = document.createElement("li");
				ls.appendChild(document.createTextNode(x));
				customs.appendChild(ls);
			}
			col.appendChild(customs);
			row.appendChild(col);
		}
		else
		{
			col.appendChild(document.createTextNode(values[c]));
			row.appendChild(col);
		}
	}

	//In the end, append the table
	document.getElementById("show").appendChild(row);
}

//DisableDeck() function disable fields that should remain empty (based on certain conditions)
function DisableDeck(name)
{
	var item = document.getElementById(name);
	if(item.disabled)
	{
		item.disabled = false;
	}
	else
	{
		item.disabled = true;
	}
}