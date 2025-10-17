const chat = document.querySelector("#chat")
const prompt = document.querySelector("#prompt")
const userInput = document.querySelector("#input")
const sendPrompt = document.querySelector("#send_prompt")
const openChat = document.querySelector("#open_chat")
const closeChat = document.querySelector("#close_chat")
const mainContent = document.querySelector("#maincontent")
const chatPage = document.querySelector("#chat_page")


openChat.addEventListener("click", e => {
    context = []
    mainContent.style.display = "none";
    openChat.style.display = "none";
    chatPage.style.display = "block";
    console.log("openchat")
})

closeChat.addEventListener("click", e => {
    chatPage.style.display = "none";
    mainContent.style.display = "block";
    openChat.style.display = "block";
    console.log("closechat")
})


sendPrompt.addEventListener("click", async (e) => {

    e.preventDefault() // indispensable pour éviter le rafraichiseement auto entrainant un "TypeError: NetworkError when attempting to fetch ressource"
    const inputData = userInput.value

    if (inputData != "") {
        const newUserBox = document.createElement("div")
        const newUserContent = document.createTextNode(inputData)
        newUserBox.appendChild(newUserContent)
        newUserBox.style.color = "#77a"
        chat.append(newUserBox)
        prompt.style.display = "none"

        const response = await fetch(endpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                prompt: inputData,
            })
        })

        const newLLMBox = document.createElement("div")
        chat.append(newLLMBox)

        const reader = response.body.getReader()
        let output = ""
        while (true) {
            const { done, value } = await reader.read()
            output = new TextDecoder().decode(value)
            const newLLMContent = document.createTextNode(output)
            newLLMBox.appendChild(newLLMContent)
            if (done) {
                prompt.style.display = "block"
                userInput.value = ""
                return
            }
        }

    } else {
        console.log("------ no inputData")
    }
})

