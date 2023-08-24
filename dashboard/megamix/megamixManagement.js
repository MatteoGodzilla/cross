let dropdownOptions = []
let userChosenIDS = []

function initialCheck() {
	const addButtons = document.querySelector("#addButtons")
	const editButtons = document.querySelector("#editButtons")

	const params = new Proxy(new URLSearchParams(window.location.search), {
		get: (searchParams, prop) => searchParams.get(prop)
	})
	let id = params.id
	if (id != null) {
		//set to edit
		let code = window.localStorage.getItem("Bearer")

		let headers = new Headers()
		headers.append("Authorization", `Bearer ${code}`)
		fetch(`/api/v1/megamix/${id}`, { headers: headers })
			.then(res => res.json())
			.then(json => { console.log(json); return json })
			.then(async (json) => {
				await GetAllCustoms()
				MegamixToForm(json)
			})
		addButtons.style.display = "none"
	} else {
		//set to add
		editButtons.style.display = "none"
		GetAllCustoms().then(() => UpdateTracks([]))
	}
}

initialCheck()

async function AddMegamix() {
	try {
		let custom = FormToMegamix()

		let code = window.localStorage.getItem("Bearer")

		let headers = new Headers()
		headers.append("Authorization", `Bearer ${code}`)
		headers.append("Content-Type", "application/json")
		let result = await fetch(`/api/v1/megamix/create`, {
			body: JSON.stringify(custom),
			method: "POST",
			headers: headers
		})
		if (result.status == 201) {
			window.location = "../megamix/index.html"
		}
	} catch (error) {
		alert(error)
	}
}

async function EditMegamix() {
	try {
		let custom = FormToMegamix()
		// upload to database
		const params = new Proxy(new URLSearchParams(window.location.search), {
			get: (searchParams, prop) => searchParams.get(prop)
		})

		let code = window.localStorage.getItem("Bearer")

		let headers = new Headers()
		headers.append("Authorization", `Bearer ${code}`)
		headers.append("Content-Type", "application/json")
		let result = await fetch(`/api/v1/megamix/${params.id}`, {
			body: JSON.stringify(custom),
			method: "PATCH",
			headers: headers
		})
		if (result.status == 200) {
			window.location = "../megamix/index.html"
		}
	} catch (error) {
		alert(error)
	}
}

async function DeleteMegamix() {
	const params = new Proxy(new URLSearchParams(window.location.search), {
		get: (searchParams, prop) => searchParams.get(prop)
	})
	let id = params.id
	if (id != null) {
		if (confirm("Are you sure about that?")) {
			let code = window.localStorage.getItem("Bearer")
			let headers = new Headers()
			headers.append("Authorization", `Bearer ${code}`)

			let result = await fetch(`/api/v1/megamix/${params.id}`, {
				method: "DELETE",
				headers: headers
			})
			if (result.status == 204)
				window.location = "../megamix/index.html"
		}
	}
}

async function GetAllCustoms() {
	let code = window.localStorage.getItem("Bearer")
	let headers = new Headers()
	headers.append("Authorization", `Bearer ${code}`)

	let databaseIds = []
	let ids = await fetch(`/api/v1/custom/latest/`, { headers: headers }).then(res => res.json())
	while (ids.length > 0) {
		databaseIds = databaseIds.concat(ids)
		let lastId = ids[ids.length - 1]
		ids = await fetch(`/api/v1/custom/latest/?lastID=${lastId}`, { headers: headers }).then(res => res.json())
	}

	for (const id of databaseIds) {
		let custom = await fetch(`/api/v1/custom/${id}`, { headers: headers }).then(res => res.json())
		//allDatabaseCustoms.push(custom)
		const option = document.createElement("option")
		option.value = id
		option.text = `${id}: ${custom.IDTag}`

		dropdownOptions.push(option)
	}
}

function UpdateTracks(ids) {
	const tracksContainer = document.querySelector("#tracksContainer")
	tracksContainer.innerHTML = ""

	const count = Math.max(ids.length, 1)
	for (let i = 0; i < count; i++) {
		const select = document.createElement("select")
		for (let opt of dropdownOptions) {
			select.appendChild(opt.cloneNode(true))
		}
		select.value = ids[i]
		select.onchange = () => setId(i, select.value)
		const up = document.createElement("button")
		up.textContent = "⮝"
		up.onclick = () => moveUp(i)
		const down = document.createElement("button")
		down.textContent = "⮟"
		down.onclick = () => moveDown(i)
		const remove = document.createElement("button")
		remove.textContent = "-"
		remove.onclick = () => removeId(i)
		const add = document.createElement("button")
		add.textContent = "+"
		add.onclick = () => addId(i)

		tracksContainer.appendChild(select)
		tracksContainer.appendChild(up)
		tracksContainer.appendChild(down)
		tracksContainer.appendChild(remove)
		tracksContainer.appendChild(add)
	}

	userChosenIDS = ids
}

function setId(index, value) {
	userChosenIDS[index] = value
	UpdateTracks(userChosenIDS)
}

function moveUp(index) {
	if (index <= 0) return
	let a = userChosenIDS[index - 1]
	let b = userChosenIDS[index]
	userChosenIDS[index - 1] = b
	userChosenIDS[index] = a
	UpdateTracks(userChosenIDS)
}

function moveDown(index) {
	if (index >= userChosenIDS.length - 1) return
	let a = userChosenIDS[index]
	let b = userChosenIDS[index + 1]
	userChosenIDS[index] = b
	userChosenIDS[index + 1] = a
	UpdateTracks(userChosenIDS)
}

function removeId(index) {
	if (userChosenIDS.length <= 1) return
	userChosenIDS.splice(index, 1)
	UpdateTracks(userChosenIDS)
}

function addId(index) {
	userChosenIDS.splice(index + 1, 0, -1)
	UpdateTracks(userChosenIDS)
}

function MegamixToForm(json) {
	const nameInput = document.querySelector("#MegamixName")
	nameInput.value = json.Name ?? ""

	//tracks
	UpdateTracks(json.Customs)

	const downloadInput = document.querySelector("#MegamixDownload")
	downloadInput.value = json.DownloadLink ?? ""

	const videoInput = document.querySelector("#MegamixPreview")
	videoInput.value = json.videoPreview ?? ""
}

function FormToMegamix() {
	let megamix = {}
	const nameInput = document.querySelector("#MegamixName")
	megamix.Name = nameInput.value

	const selectInputs = document.querySelectorAll("#tracksContainer select")
	megamix.Customs = []
	for (let select of selectInputs) {
		megamix.Customs.push(select.value)
	}

	const downloadInput = document.querySelector("#MegamixDownload")
	megamix.DownloadLink = downloadInput.value

	const videoInput = document.querySelector("#MegamixPreview")
	megamix.VideoPreview = videoInput.value

	return megamix
}