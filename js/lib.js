
async function fetchState() {
    const res = await fetch("/state");
    const data = await res.json();

    const format = (sea) => sea.map(row => row.join(" ")).join("\n");

    document.getElementById("userSea").textContent = format(data.user_sea);
    const wrapperEl1 = document.querySelector("#board-1")
    renderSea(data.user_sea, wrapperEl1)
    console.log(data.user_sea)
    document.getElementById("userVisible").textContent = format(data.user_visible);
    const wrapperEl2 = document.querySelector('#board-2')
    renderSea(data.user_visible, wrapperEl2)
    document.getElementById("botSea").textContent = format(data.bot_sea);
    const wrapperEl3 = document.querySelector('#board-3')
    renderSea(data.bot_sea, wrapperEl3)
    document.getElementById("botVisible").textContent = format(data.bot_visible);
    const wrapperEl4 = document.querySelector('#board-4')
    renderSea(data.bot_visible, wrapperEl4)

    const status = document.getElementById("status");
    if (data.game_over) {
        status.textContent = "Game Over! Winner: " + data.winner.toUpperCase();
        document.getElementById("coord").disabled = true;
    } else if (data.is_user_turn) {
        status.textContent = "Your turn";
        document.getElementById("coord").disabled = false;
    } else {
        status.textContent = "Bot's turn...";
        document.getElementById("coord").disabled = true;
    }
}

const renderSea = (sea, wrapperEl) => {
    const prevSea = wrapperEl.querySelector('.sea')
    if (prevSea) {
        prevSea.remove()
    }
    const seaEl = document.createElement("div")
    seaEl.classList.add("sea")
    seaEl.innerHTML = ""
    for (const row of sea) {
        for (const cell of row) {
            if (cell === ".") {
                seaEl.innerHTML += '<div class="spot"></div>'

            } else if (cell === "#") {
                seaEl.innerHTML += '<div class="spot"><div class="deck"></div></div>'

            } else if (cell === "~") {
                seaEl.innerHTML += '<div class="spot"><img src="/pictures/bubbles.png" class="bubble" alt="" /></div>'

            } else if (cell === "X") {
                seaEl.innerHTML += '<div class="spot"><img src="/pictures/sinking_ship.png" class="sinking_ship" alt="" /></div>'

            } else if (cell === "-") {
                seaEl.innerHTML += '<div class="spot">-</div>'
            }
        }
    }
    wrapperEl.append(seaEl)
}

const applyHidden = () => {

    if (!isHidden) {

        toggleBtn.textContent = "Hide Cheating"
        document.querySelectorAll("pre").forEach((element) => {
            element.style.display = "block"
            // element.style.visibility = "visible"

        })

    } else {

        toggleBtn.textContent = "Show Cheating"
        document.querySelectorAll("pre").forEach((element) => {
            element.style.display = "none"
            // element.style.visibility = "hidden"
        })
    }

}

