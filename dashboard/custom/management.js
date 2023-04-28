async function AddCustom(){
	try {
		let custom = FormToCustomJSON()
		// upload to database

		let headers = new Headers()
		headers.append("Authorization","Bearer notontwyontxwyoxtwynoxtwnyo")
		headers.append("Content-Type","application/json")
		let result = await fetch("/api/v1/custom/create",{
			body:JSON.stringify(custom),
			method:"POST",
			headers:headers
		})
		if(result.status != 201){
			throw await result.text()
		} else {
			window.location = "/custom/index.html"
		}
	} catch (error) {
		alert(error);
	}
}

function EditCustom(){
	//MISSING CHECK IMPORTANT PARAMETERS LOGIC
	alert("EDIT")
}

function FormToCustomJSON(){
	//MISSING CHECK IMPORTANT PARAMETERS LOGIC
	let custom = {}

	//IDTAG (Required)
	let IDTagInput = document.querySelector("#IDTag")
	custom.IDTag = IDTagInput.value.trim()
	if(custom.IDTag.length <= 0)
		throw "IDTag must not be empty"

	//BPM (Required)
	let BPMInput = document.querySelector("#BPM")
	custom.BPM = Number(BPMInput.value.trim())
	if(custom.BPM <= 0)
		throw "BPM cannot be empty or less than zero"

	//DOWNLOAD LINK (Required)
	let downloadInput = document.querySelector("#DownloadLink")
	custom.DownloadLink = downloadInput.value.trim()
	//TODO: more robust url check
	if(custom.DownloadLink.length <= 0)
		throw "Download Link must not be empty"

	custom.Songs = []
	for(let i = 1; i <=3; i++){
		let songNameInput = document.querySelector(`#SongName${i}`)
		let songArtistInput = document.querySelector(`#ArtistName${i}`)

		if(songNameInput.value.trim().length > 0){
			let song = { }
			song.name = songNameInput.value.trim()
			song.artist = songArtistInput.value.trim()
			custom.Songs.push(song)
		}
	}
	if(custom.Songs.length == 0)
		throw "There must be at least one song in the custom"

	//SONG NAME 1 (Required)
	//SONG ARTIST 1 (Required)
	//SONG NAME 2
	//SONG ARTIST 2
	//SONG NAME 3
	//SONG ARTIST 3

	//CHARTER
	let charterInput = document.querySelector("#Charter")
	custom.Charter = charterInput.value.trim()

	//MIXER
	let mixerInput = document.querySelector("#Mixer")
	custom.Mixer = mixerInput.value.trim()

	//DIFFICULTY
	custom.Difficulties = {}
	//GENERAL
	let GeneralDiffInput = document.querySelector("#GeneralDiff")
	custom.Difficulties.General = Number(GeneralDiffInput.value.trim())

	//TAP
	let TapDiffInput = document.querySelector("#TapDiff")
	custom.Difficulties.Tap = Number(TapDiffInput.value.trim())

	//CROSSFADE
	let CrossfadeDiffInput = document.querySelector("#CrossfadeDiff")
	custom.Difficulties.Crossfade = Number(CrossfadeDiffInput.value.trim())

	//SCRATCH
	let ScratchDiffInput = document.querySelector("#ScratchDiff")
	custom.Difficulties.Scratch = Number(ScratchDiffInput.value.trim())

	//AVAILABLE CHARTS
	custom.Charts = {}
	//BEGINNER
	let beginnerInput = document.querySelector("#Beginner")
	custom.Charts.Beginner = beginnerInput.checked

	//EASY
	let EasyInput = document.querySelector("#Easy")
	custom.Charts.Easy = EasyInput.checked

	//MEDIUM
	let MediumInput = document.querySelector("#Medium")
	custom.Charts.Medium = MediumInput.checked

	//HARD
	let HardInput = document.querySelector("#Hard")
	custom.Charts.Hard = HardInput.checked

	//EXPERT
	let ExpertInput = document.querySelector("#Expert")
	custom.Charts.Expert = ExpertInput.checked

	//DECKSPEEDS
	custom.DeckSpeeds = {}
	//BEGINNER
	let beginnerDSInput = document.querySelector("#BeginnerDS")
	custom.DeckSpeeds.Beginner = Number(beginnerDSInput.value.trim())

	//EASY
	let EasyDSInput = document.querySelector("#EasyDS")
	custom.DeckSpeeds.Easy = Number(EasyDSInput.value.trim())

	//MEDIUM
	let MediumDSInput = document.querySelector("#MediumDS")
	custom.DeckSpeeds.Medium = Number(MediumDSInput.value.trim())

	//HARD
	let HardDSInput = document.querySelector("#HardDS")
	custom.DeckSpeeds.Hard = Number(HardDSInput.value.trim())

	//EXPERT
	let ExpertDSInput = document.querySelector("#ExpertDS")
	custom.DeckSpeeds.Expert = Number(ExpertDSInput.value.trim())

	//VIDEO LINK
	let videoLinkInput = document.querySelector("#VideoLink")
	custom.VideoLink = videoLinkInput.value.trim()

	//NOTES
	let notesInput = document.querySelector("#Notes")
	custom.Notes = notesInput.value.trim()

	return custom
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