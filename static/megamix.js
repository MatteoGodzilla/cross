function AddMegamix(){
    alert("ADD")
}

function EditMegamix(){
    alert("EDIT")
}

function GetLatest(){
    alert("LATEST")
}

function MGMX_JSONToTable(json)
{
	// From JSON to Javascript object
	var myObj = JSON.parse(json);

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

	//In the end, append the row
	document.getElementById("show").appendChild(row);
}