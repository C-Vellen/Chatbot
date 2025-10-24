const form = document.querySelector('form')

// display update or new prompt form
function promptForm(e) {
    const promptItem = e.target.parentNode

    // highlight selected prompt
    form.querySelector("#prompt_list").querySelectorAll("p").forEach(
        p => p.classList.remove("border-4")
    )
    promptItem.querySelector("p").classList.add("border-4")


    // display prompt form
    form.querySelector("#presentation").classList.add("hidden")
    const edition = form.querySelector("#prompt-edition")
    edition.classList.remove("hidden")

    // validation activation
    form.querySelector(".validation-btn").classList.remove("hidden")
    form.querySelector(".disabled-btn").classList.add("hidden")


    // pre-fill form with current values
    edition.querySelector(".prompt-id").value = promptItem.dataset.id
    edition.querySelector(".prompt-name").value = promptItem.dataset.name
    edition.querySelector(".prompt-name").required = true
    edition.querySelector(".prompt-target").querySelectorAll("option").forEach(op => {
        if (op.value == promptItem.dataset.target) {
            op.selected = true
        } else {
            op.selected = false
        }
    })
    edition.querySelector(".prompt-target").required = true

    edition.querySelector(".prompt-text").innerHTML = promptItem.dataset.promptText
    edition.querySelector(".prompt-active").checked = promptItem.dataset.active == 'True'
    promptItem.querySelector("input").checked = false

    // reactivate delete cross for no selected prompts
    form.querySelectorAll(".inactive-prompt").forEach(prompt => {
        prompt.querySelector(".disabled-delete-prompt").classList.add("hidden")
        prompt.querySelector(".confirmed-delete-prompt").classList.add("hidden")
        prompt.querySelector(".delete-prompt").classList.add("hidden")

        if (prompt.querySelector("input").checked) {
            prompt.querySelector(".confirmed-delete-prompt").classList.remove("hidden")
        } else {
            prompt.querySelector(".delete-prompt").classList.remove("hidden")
        }
    })

    // deactivate delete cross for selected prompt
    promptItem.querySelector(".disabled-delete-prompt").classList.remove("hidden")
    promptItem.querySelector(".delete-prompt").classList.add("hidden")
    promptItem.querySelector(".confirmed-delete-prompt").classList.add("hidden")
    promptItem.querySelector("p").classList.remove("text-red-500", "line-through")

}

form.addEventListener('click', e => {
    // update prompt
    if (e.target.classList.contains("update-prompt")) { promptForm(e) }
    // create new prompt
    if (e.target.classList.contains("create-prompt")) { promptForm(e) }
    // delete prompt
    if (e.target.classList.contains("delete-prompt")) {
        const promptItem = e.target.parentNode
        // display red delete cross
        promptItem.querySelector(".disabled-delete-prompt").classList.add("hidden")
        promptItem.querySelector(".delete-prompt").classList.add("hidden")
        promptItem.querySelector(".confirmed-delete-prompt").classList.remove("hidden")
        promptItem.querySelector("input").checked = true

        // validation activation
        form.querySelector(".validation-btn").classList.remove("hidden")
        form.querySelector(".disabled-btn").classList.add("hidden")

        // title in red
        promptItem.querySelector("p").classList.add("text-red-500", "line-through")

    }
    // cancel prompt deletion
    if (e.target.classList.contains("confirmed-delete-prompt")) {
        const promptItem = e.target.parentNode
        // display white delete cross
        promptItem.querySelector(".disabled-delete-prompt").classList.add("hidden")
        promptItem.querySelector(".delete-prompt").classList.remove("hidden")
        promptItem.querySelector(".confirmed-delete-prompt").classList.add("hidden")
        promptItem.querySelector("input").checked = false

        // restore title
        promptItem.querySelector("p").classList.remove("text-red-500", "line-through")

    }
})
