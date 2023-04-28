const maindiv = document.querySelector("#login")
const usernameInput = document.querySelector("#username")
const passwordInput = document.querySelector("#password")

//Submit button
async function Login(){
    if(usernameInput.value == "" || passwordInput.value == "")
        return;
    let credentials = btoa(`${usernameInput.value}:${passwordInput.value}`)

    let headers = new Headers()
    headers.append("Authorization",`Basic ${credentials}`)
    let result = await fetch("/api/v1/login",{
        headers: headers
    })

    if(result.status == 200){
        let id = await result.json()
        window.localStorage.setItem("Bearer", id)
        CloseLogin()
    }
}

function CloseLogin(){
    maindiv.classList.add("hidden")
}

function OpenLogin(){
    maindiv.classList.remove("hidden")
}

async function OnStart(){
    let code = window.localStorage.getItem("Bearer")
    let headers = new Headers()
    headers.append("Authorization",`Bearer ${code}`)
    let result = await fetch("/api/v1/login/check",{
        headers:headers,
    }).then(res => res.json())

    if(!result) OpenLogin()
}

OnStart()