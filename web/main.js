const ws = new WebSocket("ws://localhost:8765");
const instr_queue = new Array();

ws.addEventListener("open", (event) => {
  console.log("open");
  ws.send("reg client");
  showMask("Receiving Data...");
});

ws.addEventListener("message", (event) => {
  try {
    const data = JSON.parse(event.data);
    instr_queue.push(data);
  } catch (e) {
    console.log("Failed to parse server data");
    return;
  }
});

ws.addEventListener("close", (event) => {
  console.log("Connection closed");
});

ws.addEventListener("error", (event) => {
  console.log("Error in connection");
  console.log(event);
});

function showMask(content) {
  document.getElementById("gameboard-mask-title").innerText = content;
  document.getElementsByClassName("gameboard-mask")[0].style["display"] = "flex";
}

function hideMask() {
  document.getElementsByClassName("gameboard-mask")[0].style["display"] = "none";
}

function appendColumn(prob = 0.5) {
  const a_per = parseInt(prob * 100);
  const b_per = 100 - a_per;
  html = `
  <div class="round__container">
    <div class="round-column b" style="height: ${b_per}%;">
      <span class="round-column-num">${b_per}</span>
    </div>
    <div class="round-column a" style="height: ${a_per}%;">
      <span class="round-column-num">${a_per}</span>
    </div>
  </div>
  `;
  document.querySelector(".rounds").insertAdjacentHTML("beforeend", html);
}

let init_balance, prob_seq;
let last_data;
function initBoard(data = last_data) {
  last_data = data;
  init_balance = data["init_balance"];
  setBalance(init_balance);
  prob_seq = data["seq"];
  document.querySelector(".rounds").innerHTML = "";
  for (const prob of prob_seq) {
    appendColumn(prob);
  }
}

function setBalance(balance) {
  document.getElementById("balance-a").innerText = balance[0];
  document.getElementById("balance-b").innerText = balance[1];
}

const player_names = Array(2);
function setPlayer(data) {
  if (data["side"] == "A") {
    document.getElementById("name-a").innerText = data["name"];
    player_names[0] = data["name"];
  } else if (data["side"] == "B") {
    document.getElementById("name-b").innerText = data["name"];
    player_names[1] = data["name"];
  }
}

function setBet(data) {
  const round = data["round"];
  const side = data["side"].toLowerCase();
  const amount = data["amount"];
  const target = document.querySelector(`.round__container:nth-child(${round + 1}) > .${side}`).getElementsByClassName("round-column-num")[0];
  target.classList.add("round-column-bet");
  target.classList.remove("round-column-num");
  if (amount < 1000) {
    target.innerHTML = amount;
  } else {
    target.classList.add("thousand");
    target.innerHTML = `${parseInt(amount / 1000)}<span>${String(amount % 1000).padStart(3, 0)}</span>`;
  }
  setScroll(round);
}

let target_scroll = 0;
function setScroll(round) {
  target_scroll = round * 70;
}

const scroll_timer = window.setInterval(() => {
  const target = document.querySelector(".rounds");
  const current_scroll = target.scrollLeft;
  if (Math.abs(target_scroll - current_scroll) > 10) {
    target.scrollTo((target_scroll + current_scroll) / 2, 0);
  } else {
    target.scrollTo(target_scroll, 0);
  }
}, 20);

function setResult(data) {
  const round = data["round"];
  const winner = data["winner"].toLowerCase();
  const loser = winner == "a" ? "b" : "a";
  const result = data["result"];
  const balance = data["balance"];
  setBalance(balance);
  // const column = document.querySelector(`.round__container:nth-child(${round + 1})`);
  // column.insertAdjacentHTML("beforeend", `
  //   <div class="round-decider" style="bottom: calc(${parseInt(result * 80)}% + 40px);">${result.toFixed(2)}</div>
  // `);
  const loser_column = document.querySelector(`.round__container:nth-child(${round + 1}) > .${loser}`);
  loser_column.classList.add("gray");
  setScroll(round);
}

function switchSides(balance_diff) {
  window.setTimeout(() => {
    showMask("Switching Sides...");
    setScroll(0);
    document.getElementById("name-a").style.opacity = 0;
    document.getElementById("name-b").style.opacity = 0;
    window.setTimeout(() => {
      document.getElementById("name-a").innerText = player_names[1];
      document.getElementById("name-b").innerText = player_names[0];
      document.getElementById("name-a").style.opacity = 1;
      document.getElementById("name-b").style.opacity = 1;
    }, 500);
    if (balance_diff > 0) {
      document.getElementById("lead-count-a").innerText = balance_diff;
      document.querySelector(".player-extension.a").style["top"] = "40px";
    } else if (balance_diff < 0) {
      document.getElementById("lead-count-b").innerText = -balance_diff;
      document.querySelector(".player-extension.b").style["bottom"] = "40px";
    }
    [init_balance[0], init_balance[1]] = [init_balance[1], init_balance[0]];
    initBoard();
    window.setTimeout(() => {
      hideMask();
    }, 1000);
  }, 1000);
}

let timeout = window.setTimeout(processInstr, 30);

function processInstr() {
  let ms = 20;
  window.clearTimeout(timeout);
  if (instr_queue.length) {
    let instr = instr_queue[0];
    instr_queue.shift();
    switch (instr["type"]) {
      case "info":
        initBoard(instr["data"]);
        hideMask();
        break;
      case "playerjoin":
        setPlayer(instr["data"]);
        ms = 1000;
        break;
      case "bet":
        setBet(instr["data"]);
        break;
      case "result":
        setResult(instr["data"]);
        break;
      case "switchsides":
        ms = 3500;
        switchSides(instr["data"]);
        break;
      case "gameover":
        window.clearInterval(scroll_timer);
        break;
    }
  }
  timeout = window.setTimeout(processInstr, ms);
}