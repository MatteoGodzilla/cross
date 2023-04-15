function AddCustom(){
    
}

function EditCustom(){

}

function AddMegamix(){

}

function EditMegamix(){

}

let count = 10;

async function GetLatest(){
    latestCustoms = document.querySelector("#latestCustoms")
    latestCustoms.innerHTML = ""

    ids = await fetch(`/api/v1/custom/latest/${count}`).then(res => res.json())
    console.log(ids)
    for(id of ids){
        json = await fetch(`/api/v1/custom/${id}`).then(res => res.json());
        latestCustoms.appendChild(CustomToPage(json,id))
    }

    count += 10
}

function CustomToPage(custom,id){
    console.log(custom)
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
	
	// Setting up the data structures to build the table section (FOR NOW INSIDE THE FUNCTION)
	const table = document.createElement("table");
	
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
	table.appendChild(row);

	//In the end, append the table
	document.getElementById("show").appendChild(table);
}

function MGMX_JSONToTable(json)
{
	// From JSON to Javascript object
	var myObj = JSON.parse(json);
	
	// Setting up the data structures to build the table section (FOR NOW INSIDE THE FUNCTION)
	const table = document.createElement("table");

	// Initializing the row that will contain the JSON object
	const row = document.createElement("tr");

	// keys => simply the description (wrote in left column) of the content in the right column (PROBABLY DEPRECATED)
	//var keys = ["Megamix name:", "Download link:", "Video preview:", "Customs:"] 
	
	// values => the data content of the JSON that we are going to write in the right column
	var values = [myObj.Name, myObj.DownloadLink, myObj.VideoPreview];
	
	// Creating the table structure
	for(let c = 0; c < 4; c++)
	{
		const col = document.createElement("td");
		
		if(c < 3)
		{
			col.appendChild(document.createTextNode(values[c]));
			row.appendChild(col);
		}
		else
		{
			const customs = document.createElement("ul");
			for(x in myObj.Customs)
			{
				const ls = document.createElement("li");
				ls.appendChild(document.createTextNode(x));
				customs.appendChild(ls);
			}
			col.appendChild(customs);
			row.appendChild(col);
		}		
	}
	table.appendChild(row);
	
	//In the end, append the table
	document.getElementById("show").appendChild(table);
}