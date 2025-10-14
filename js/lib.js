
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
    handleSpots()

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
    let str = ""
    let rowNumber = -1
    for (const row of sea) {
        rowNumber += 1
        let colNumber = -1
        for (const cell of row) {
            colNumber += 1
            str += `<div class="spot" data-row="${rowNumber}" data-col="${colNumber}">`

            if (cell === ".") {

            } else if (cell === "#") {
                str += '<div class="deck"></div>'

            } else if (cell === "~") {
                str += '<img src="/pictures/bubbles.png" class="bubble" alt="" />'

            } else if (cell === "X") {
                str += '<img src="/pictures/sinking_ship.png" class="sinking_ship" alt="" />'

            } else if (cell === "-") {
                str += '-'
            }

            str += "</div>"
        }
    }
    seaEl.innerHTML = str
    wrapperEl.append(seaEl)
}

const applyHidden = () => {

    if (!isHidden) {

        toggleBtn.textContent = "Hide Cheating"
        document.querySelectorAll("pre").forEach((element) => {
            element.style.display = "block"
            // element.style.visibility = "visible"

        })
        document.querySelector("#extra-board-wrapper").style.display = "block"

    } else {

        toggleBtn.textContent = "Show Cheating"
        document.querySelectorAll("pre").forEach((element) => {
            element.style.display = "none"
            // element.style.visibility = "hidden"
        })
        document.querySelector("#extra-board-wrapper").style.display = "none"
    }

}

const handleSpots = () => {
    document.querySelectorAll("#board-4 .spot").forEach((spot) => {
        spot.addEventListener("click", () => {
            const row = spot.getAttribute("data-row")
            const col = spot.getAttribute("data-col")
            const alphabet = "abcdefghij"
            let letter = alphabet[col]
            let num = +row + 1
            // row = int(coord[1:]) - 1
            // col = alphabet.index(coord[0])
            // alert(`Cell coordinates: (${row}, ${col}) or ${letter + num}`)
            document.getElementById("coord").value = `${letter}${num}`
            handleSubmitCoords()
            
        })
    })
}

const handleSubmitCoords = async () => {
      const coord = document.getElementById("coord").value.trim();
      if (!coord) return;

      const res = await fetch("/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ coordinate: coord })
      });

      document.getElementById("coord").value = "";
      await fetchState();
}