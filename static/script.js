let xWins = 0;
let oWins = 0;
let dWins = 0;

const boardEl   = document.getElementById('board');
const statusEl  = document.getElementById('status');
const xWinsEl   = document.getElementById('xWins');
const oWinsEl   = document.getElementById('oWins');
const dWinsEl = document.getElementById('dWins'); 
const resetBtn  = document.getElementById('resetBtn');
const connEl    = document.getElementById('connections');
const waitingEl = document.getElementById('waiting');

const UPDATE_MS = 700;   // frecuencia de polling (~1s)

function createBoard() {
  boardEl.innerHTML = '';
  for (let i = 0; i < 9; i++) {
    const cell = document.createElement('div');
    cell.classList.add('cell');
    cell.dataset.index = i;
    cell.addEventListener('click', () => makeMove(i));
    boardEl.appendChild(cell);
  }
}

async function registerConnect() {
  const res  = await fetch('/connect', { cache: 'no-store' });
  const json = await res.json();
  connEl.textContent = json.connections ?? 0;
  waitingEl.style.display = (json.connections < 2) ? 'block' : 'none';
}

async function fetchState() {
  const res = await fetch('/state', { cache: 'no-store' });
  return await res.json();
}

async function updateBoard() {
  const { board, current, winner, connections } = await fetchState();

  // Refresca celdas
  document.querySelectorAll('.cell').forEach(cell => {
    const v = board[cell.dataset.index];
  cell.textContent = v;
  cell.classList.toggle('x', v === 'X');
  cell.classList.toggle('o', v === 'O');
  });

  // Estado de partida
  if (winner) {
    if (winner === 'X') xWins++;
    else if (winner === 'O') oWins++;
    statusEl.textContent = winner === 'Draw' ? '¡Empate!' : `¡${winner} gana!`;
    xWinsEl.textContent = xWins;
    oWinsEl.textContent = oWins;
  } else {
    statusEl.textContent = `Turno de ${current}`;
  }

  // Conexiones
  connEl.textContent = connections ?? 0;
  waitingEl.style.display = (connections < 2) ? 'block' : 'none';
}

async function makeMove(i) {
  try {
    const res = await fetch('/move', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      cache: 'no-store',
      body: JSON.stringify({ index: i })
    });
    // Aunque mi jugada ya actualiza, el polling asegurará que el otro cliente lo vea
    if (!res.ok) {
      // Si fue jugada inválida, igual sincroniza
      await updateBoard();
      return;
    }
    await updateBoard();
  } catch (e) {
    console.error('Error en move:', e);
  }
}

resetBtn.addEventListener('click', async () => {
  await fetch('/reset', { method: 'POST', cache: 'no-store' });
  statusEl.textContent = '';
  await updateBoard();
});

window.addEventListener('load', async () => {
  createBoard();
  await registerConnect();
  await updateBoard();
  // 🔁 Polling continuo para ver jugadas del otro dispositivo
  setInterval(updateBoard, UPDATE_MS);
});
