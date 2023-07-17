let state = undefined
function initialCheck() {
	const confirmButton = document.querySelector(".btnConfirm")
	const params = new Proxy(new URLSearchParams(window.location.search), {
		get: (searchParams, prop) => searchParams.get(prop)
	});
	let id = params.id
	if (id != null) {
		//set to edit
		fetch(`/api/v1/custom/${id}`)
			.then(res => res.json())
			.then(CustomToForm)
		confirmButton.textContent = "EDIT CUSTOM"
		state = "EDIT"
	} else {
		//set to create
		confirmButton.textContent = "ADD CUSTOM"
		state = "ADD"
	}
}

initialCheck()

function ConfirmAction() {
	if (state == "EDIT") EditCustom()
	else if (state == "ADD") AddCustom()
}

async function AddCustom() {
	try {
		let custom = FormToCustomJSON()
		// upload to database

		let code = window.localStorage.getItem("Bearer")

		let headers = new Headers()
		headers.append("Authorization", `Bearer ${code}`)
		headers.append("Content-Type", "application/json")
		let result = await fetch("/api/v1/custom/create", {
			body: JSON.stringify(custom),
			method: "POST",
			headers: headers
		})
		if (result.status == 201) {
			window.location = "../custom/index.html"
		}
	} catch (error) {
		alert(error);
	}
}

async function EditCustom() {
	//MISSING CHECK IMPORTANT PARAMETERS LOGIC
	try {
		let custom = FormToCustomJSON()
		// upload to database
		const params = new Proxy(new URLSearchParams(window.location.search), {
			get: (searchParams, prop) => searchParams.get(prop)
		});

		let code = window.localStorage.getItem("Bearer")

		let headers = new Headers()
		headers.append("Authorization", `Bearer ${code}`)
		headers.append("Content-Type", "application/json")
		let result = await fetch(`/api/v1/custom/${params.id}`, {
			body: JSON.stringify(custom),
			method: "PATCH",
			headers: headers
		})
		if (result.status == 200) {
			window.location = "../custom/index.html"
		}
	} catch (error) {
		alert(error);
	}
}

async function DeleteCustom() {
	const params = new Proxy(new URLSearchParams(window.location.search), {
		get: (searchParams, prop) => searchParams.get(prop)
	});
	let id = params.id
	if (id != null) {
		if (confirm("Are you sure about that?")) {
			let code = window.localStorage.getItem("Bearer")

			let headers = new Headers()
			headers.append("Authorization", `Bearer ${code}`)
			let result = await fetch(`/api/v1/custom/${params.id}`, {
				method: "DELETE",
				headers: headers
			})
			if (result.status == 204) {
				window.location = "../custom/index.html"
			}
		}
	}
}

function FormToCustomJSON() {
	//MISSING CHECK IMPORTANT PARAMETERS LOGIC
	let custom = {}

	//IDTAG (Required)
	let IDTagInput = document.querySelector("#IDTag")
	custom.IDTag = IDTagInput.value.trim()
	if (custom.IDTag.length <= 0)
		throw "IDTag must not be empty"

	//BPM (Required)
	let BPMInput = document.querySelector("#BPM")
	custom.BPM = Number(BPMInput.value.trim())
	if (custom.BPM <= 0)
		throw "BPM cannot be empty or less than zero"

	//DOWNLOAD LINK (Required)
	let downloadInput = document.querySelector("#DownloadLink")
	custom.DownloadLink = downloadInput.value.trim()
	//TODO: more robust url check
	if (custom.DownloadLink.length <= 0)
		throw "Download Link must not be empty"

	custom.Songs = []
	for (let i = 1; i <= 3; i++) {
		let songNameInput = document.querySelector(`#SongName${i}`)
		let songArtistInput = document.querySelector(`#ArtistName${i}`)

		if (songNameInput.value.trim().length > 0) {
			let song = {}
			song.Name = songNameInput.value.trim()
			song.Artist = songArtistInput.value.trim()
			custom.Songs.push(song)
		}
	}
	if (custom.Songs.length == 0)
		throw "There must be at least one song in the custom"

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

function CustomToForm(json) {
	let IDTagInput = document.querySelector("#IDTag")
	IDTagInput.value = json.IDTag

	//BPM (Required)
	let BPMInput = document.querySelector("#BPM")
	BPMInput.value = json.BPM

	//DOWNLOAD LINK (Required)
	let downloadInput = document.querySelector("#DownloadLink")
	downloadInput.value = json.DownloadLink

	let songNames = document.querySelectorAll("[id^=SongName]")
	let songArtists = document.querySelectorAll("[id^=ArtistName]")

	for (let i = 0; i < 3 && i < json.Songs.length; i++) {
		let song = json.Songs[i]
		songNames[i].value = song.Name
		songArtists[i].value = song.Artist
	}

	//CHARTER
	let charterInput = document.querySelector("#Charter")
	charterInput.value = json.Charter

	//MIXER
	let mixerInput = document.querySelector("#Mixer")
	mixerInput.value = json.Mixer

	//DIFFICULTY
	//GENERAL
	let GeneralDiffInput = document.querySelector("#GeneralDiff")
	GeneralDiffInput.value = json.Difficulties.General

	//TAP
	let TapDiffInput = document.querySelector("#TapDiff")
	TapDiffInput.value = json.Difficulties.Tap

	//CROSSFADE
	let CrossfadeDiffInput = document.querySelector("#CrossfadeDiff")
	CrossfadeDiffInput.value = json.Difficulties.Crossfade

	//SCRATCH
	let ScratchDiffInput = document.querySelector("#ScratchDiff")
	ScratchDiffInput.value = json.Difficulties.Scratch

	//AVAILABLE CHARTS
	//BEGINNER
	let beginnerInput = document.querySelector("#Beginner")
	beginnerInput.checked = json.Charts.Beginner

	//EASY
	let EasyInput = document.querySelector("#Easy")
	EasyInput.checked = json.Charts.Easy

	//MEDIUM
	let MediumInput = document.querySelector("#Medium")
	MediumInput.checked = json.Charts.Medium

	//HARD
	let HardInput = document.querySelector("#Hard")
	HardInput.checked = json.Charts.Hard

	//EXPERT
	let ExpertInput = document.querySelector("#Expert")
	ExpertInput.checked = json.Charts.Expert

	//DECKSPEEDS
	//BEGINNER
	let beginnerDSInput = document.querySelector("#BeginnerDS")
	beginnerDSInput.value = json.DeckSpeeds.Beginner

	//EASY
	let EasyDSInput = document.querySelector("#EasyDS")
	EasyDSInput.value = json.DeckSpeeds.Easy

	//MEDIUM
	let MediumDSInput = document.querySelector("#MediumDS")
	MediumDSInput.value = json.DeckSpeeds.Medium

	//HARD
	let HardDSInput = document.querySelector("#HardDS")
	HardDSInput.value = json.DeckSpeeds.Hard

	//EXPERT
	let ExpertDSInput = document.querySelector("#ExpertDS")
	ExpertDSInput.value = json.DeckSpeeds.Expert

	//VIDEO LINK
	let videoLinkInput = document.querySelector("#VideoLink")
	videoLinkInput.value = json.VideoLink;

	//NOTES
	let notesInput = document.querySelector("#Notes")
	notesInput.value = json.Notes
	BlockFields()
}

function BlockFields() {
	let elms = ["Beginner", "Easy", "Medium", "Hard", "Expert"]
	for (let name of elms) {
		let checkbox = document.getElementById(name)
		let dsfield = document.getElementById(name + "DS")

		dsfield.disabled = !checkbox.checked
	}
}