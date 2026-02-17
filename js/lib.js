const format = (sea) => sea.map(row => row.join(" ")).join("\n");

const sounds = {
    blryap: new Audio("/sounds/blryap.m4a"),
    waterBlorp: new Audio("/sounds/water_blorp.mp3"),
    cannonFire: new Audio("/sounds/cannon_fire.mp3"),
}


async function fetchState() {
    const res = await fetch("/state");
    const data = await res.json();

    document.getElementById("userSea").textContent = format(data.user_sea);
    const wrapperEl1 = document.querySelector("#board-1")
    renderPrettySea(transformVisibleSea(data.user_sea), wrapperEl1)
    console.log(data.user_sea)
    document.getElementById("userVisible").textContent = format(data.user_visible);
    const wrapperEl2 = document.querySelector('#board-2')
    renderPrettySea(transformOppositeSea(data.user_visible), wrapperEl2)
    document.getElementById("botSea").textContent = format(data.bot_sea);
    const wrapperEl3 = document.querySelector('#board-3')
    renderPrettySea(transformVisibleSea(data.bot_sea), wrapperEl3)
    document.getElementById("botVisible").textContent = format(data.bot_visible);
    const wrapperEl4 = document.querySelector('#board-4')
    renderPrettySea(transformOppositeSea(data.bot_visible), wrapperEl4)
    handleSpots()

    const status = document.getElementById("status");
    if (data.game_over) {
        status.textContent = "Game Over! Winner: "  + data.winner.toUpperCase();
        if (data.winner === "user") {
            throwConfetti(250)
            sounds.blryap.play()
        }
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

    for (let i = 0; i < 11; i++) {
        alphabet = " abcdefghij"
        str += `<div class="num_spot">${alphabet[i]}</div>`
        seaEl.innerHTML = str
        wrapperEl.append(seaEl)
    }

    for (const row of sea) {
        rowNumber += 1
        let colNumber = -1
        str += `<div class="num_spot">${rowNumber + 1}</div>`

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

const drawCell = (type, direction = "right") => {
    let innerType = type
    let condition = null
    if (type === "damaged_ship") {
        condition = "damaged"
        innerType = "alive_ship"
    } else if (type === "damaged_ship_nose") {
        condition = "damaged"
        innerType = "alive_ship_nose"
    } else if (type === "sunken_ship") {
        condition = "sunken"
        innerType = "alive_ship"
    } else if (type === "sunken_ship_nose") {
        condition = "sunken"
        innerType = "alive_ship_nose"
    }
    let cell = '<div class="cell">'
    // const cell = document.createElement("div")
    // cell.classList.add("cell")
    switch (innerType) {
        case "empty_sea":
            cell += '<img src = "/pictures/cell/just_sea.png"/>'
            break
        case "alive_ship":
            cell += '<img src = "/pictures/cell/just_sea.png"/>'
            cell += `<img src = "/pictures/cell/middle_deck.png" class = "direction-${direction}"/>`
            break
        case "alive_ship_nose":
            cell += '<img src = "/pictures/cell/just_sea.png"/>'
            cell += `<img src = "/pictures/cell/end_deck.png" class = "direction-${direction}"/>`
            break
        case "missed":
            cell += '<img src = "/pictures/cell/just_sea.png"/>'
            cell += `<img src = "/pictures/cell/dot.png"/>`//todo: better picture
            break
        case "unknown":
            cell += '<img src = "/pictures/cell/unknown.png"/>'
            break
        // case "damaged_ship":
        //     cell = '<img src = "/pictures/cell/just_sea.png"/>'
        //     cell += '<img src = "/pictures/cell/middle_deck.png"/>'
        //     cell += '<img src = "/pictures/cell/mark_of_defeat.png"/>'
        //     break
        // case "sunken_ship":
        //     cell = '<img src = "/pictures/cell/just_sea.png"/>'
        //     cell += '<img src = "/pictures/cell/middle_deck.png"/>'
        //     cell += '<img src = "/pictures/cell/explosion.png"/>'
        //     break
        case "no_ship":
            cell += '<img src = "/pictures/cell/just_sea.png"/>'
            cell += '<img src = "/pictures/cell/waves.png"/>'  //todo: better picture
            break
        default:
            cell += "default"
    }
    if (condition === "damaged") {
        cell += '<img src = "/pictures/cell/explosion.png"/>'
    } else if (condition === "sunken") {
        cell += '<img src = "/pictures/cell/mark_of_defeat.png"/>'
    }

    cell += "</div>"
    return cell
}

const transformVisibleSea = (sea) => {
    const tSea = []
    for (const row of sea) {
        const tRow = []
        for (const cell of row) {
            let tCell = cell
            if (cell === "X") {
                tCell = "@"
            }
            tRow.push(tCell)
        }
        tSea.push(tRow)
    }
    return tSea
}

const transformOppositeSea = (sea) => {
    const tSea = []
    for (const row of sea) {
        const tRow = []
        for (const cell of row) {
            let tCell = cell
            if (cell === ".") {
                tCell = "?"
            }
            if (cell === "#") {
                tCell = "@"
            }
            tRow.push(tCell)
        }
        tSea.push(tRow)
    }
    return tSea
}

const renderPrettySea = (sea, wrapperEl) => {
    const prevSea = wrapperEl.querySelector('.sea')
    if (prevSea) {
        prevSea.remove()
    }
    const seaEl = document.createElement("div")
    seaEl.classList.add("sea")
    let str = ""
    let rowNumber = -1

    for (let i = 0; i < 11; i++) {
        alphabet = " abcdefghij"
        str += `<div class="num_spot">${alphabet[i]}</div>`
        seaEl.innerHTML = str
        wrapperEl.append(seaEl)
    }

    for (const row of sea) {
        rowNumber += 1
        let colNumber = -1
        str += `<div class="num_spot">${rowNumber + 1}</div>`

        for (const cell of row) {
            colNumber += 1
            str += `<div class="spot" data-row="${rowNumber}" data-col="${colNumber}">`

            if (cell === ".") {
                str += drawCell("empty_sea")
            } else if (cell === "#") {
                str += drawCell("alive_ship")

            } else if (cell === "~") {
                str += drawCell("missed")

            } else if (cell === "X") {
                str += drawCell("sunken_ship")

            } else if (cell === "-") {
                str += drawCell("no_ship")

            } else if (cell === "@") {
                str += drawCell("damaged_ship")

            } else if (cell === "?") {
                str += drawCell("unknown")

            }

            str += "</div>"
        }
    }
    seaEl.innerHTML = str
    wrapperEl.append(seaEl)
}

const getRandom = (range, start = 0, unit = "") => {
    return start + Math.floor(Math.random() * range) + unit
}

const throwConfetti = (amount = 100) => {
    for (let i = 0; i < amount; i++) {
        const div = document.createElement("div")
        div.style.left = "20px"
        div.style.top = "1000px"
        div.classList.add("circle")
        div.style.backgroundColor = "rgb("
            + getRandom(256) + ", "
            + getRandom(256) + ", "
            + getRandom(256) + ")"
        const size = getRandom(30, 10)
        const speed = size / 10
        div.style.height = size + "px"
        div.style.width = size + "px"
        div.style.transition = speed + "s"
        document.body.append(div)
        setTimeout(() => {
            div.style.top = getRandom(800, -100, "px")
            div.style.left = getRandom(1100, 400, "px")

        }, getRandom(1500, 50))

        setTimeout(() => {
            div.style.top = 1200 + "px"
            div.style.opacity = 0
        }, 3500)

        setTimeout(() => {
            document.body.removeChild(div)
        }, 5500)
    }
}