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



function MGMX_JsonToTable(json)
{
	// From JSON to Javascript object
	var myObj = JSON.parse(json);
	
	// Setting up the data structures to build the table section 
	const table = document.createElement("table");
	
	// keys => simply the description (wrote in left column) of the content in the right column
	var keys = ["Megamix name:", "Download link:", "Video preview:", "Customs:"]
	
	// values => the data content of the JSON that we are going to write in the right column
	var values = [myObj.Name, myObj.DownloadLink, myObj.VideoPreview];
	
	// Creating the table structure
	for(let c = 0; c < 4; c++)
	{
		const row = document.createElement("tr");
		const frstCol = document.createElement("td");
		const sndCool = document.createElement("td");
		
		if(c < 3)
		{
			frstCol.appendChild(document.createTextNode(keys[c]));
			row.appendChild(frstCol);
			
			sndCol.appendChild(document.createTextNode(values[c]));
			row.appendChild(sndCol);
		}
		else
		{
			frstCol.appendChild(document.createTextNode(keys[c]));
			row.appendChild(frstCol);
			
			const customs = document.createElement("ul");
			for(x in myObj.Customs)
			{
				const ls = document.createElement("li");
				ls.appendChild(document.createTextNode(x))
				customs.appendChild()
			}
			sndCol.appendChild(customs);
			row.appendChild(sndCol);
		}
		table.appendChild(row);
		
	}
	
	//In the end, append the table
	document.getElementById("show").appendChild(table);
}