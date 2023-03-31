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