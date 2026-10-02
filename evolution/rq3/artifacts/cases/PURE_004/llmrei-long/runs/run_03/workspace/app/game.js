(() => {
  const STORAGE_KEY = 'qheadache-save-v1';
  const HISTORY_KEY = 'qheadache-history-v1';
  const puzzle = {
    width: 4,
    height: 4,
    initial: [
      ['#', '#', '#', '#'],
      ['#', 'A', '.', '#'],
      ['#', 'A', 'G', '#'],
      ['#', '#', '#', '#'],
    ],
  };

  const el = (id) => document.getElementById(id);
  const boardEl = el('board');
  const timeEl = el('time');
  const movesEl = el('moves');
  const scoreEl = el('score');
  const stateEl = el('state');
  const messageEl = el('message');
  const historyListEl = el('historyList');
  const resetBtn = el('resetBtn');
  const clearBtn = el('clearBtn');

  let state = loadState() || freshState();
  let timer = null;

  function freshState() {
    return { board: cloneBoard(puzzle.initial), moves: 0, startedAt: Date.now(), elapsedMs: 0, solved: false };
  }
  function cloneBoard(b) { return b.map(r => [...r]); }
  function saveState() { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }
  function loadState() { try { const v = JSON.parse(localStorage.getItem(STORAGE_KEY)); return v && v.board ? v : null; } catch { return null; } }
  function loadHistory() { try { return JSON.parse(localStorage.getItem(HISTORY_KEY)) || []; } catch { return []; } }
  function saveHistory(items) { localStorage.setItem(HISTORY_KEY, JSON.stringify(items)); }
  function elapsed() { return state.elapsedMs + (state.solved ? 0 : Date.now() - state.startedAt); }
  function format(ms) { const s = Math.floor(ms / 1000); return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`; }
  function score() { return Math.max(0, 1000 - state.moves * 10 - Math.floor(elapsed() / 1000)); }

  function renderHistory() {
    const items = loadHistory();
    historyListEl.innerHTML = items.length ? items.map(i => `<li>${i.time} time, ${i.moves} moves, score ${i.score}</li>`).join('') : '<li>No completed puzzles yet.</li>';
  }

  function render() {
    boardEl.innerHTML = '';
    for (let y = 0; y < puzzle.height; y++) {
      for (let x = 0; x < puzzle.width; x++) {
        const value = state.board[y][x];
        const btn = document.createElement('button');
        btn.className = 'tile ' + (value === '#' ? 'empty' : value === 'A' ? 'block' : value === 'G' ? 'goal' : '');
        btn.textContent = value === 'A' ? 'Block' : value === 'G' ? 'Goal' : '';
        btn.disabled = value === '#';
        btn.dataset.x = x; btn.dataset.y = y;
        btn.addEventListener('click', () => tryMove(x, y));
        boardEl.appendChild(btn);
      }
    }
    timeEl.textContent = format(elapsed());
    movesEl.textContent = state.moves;
    scoreEl.textContent = score();
    stateEl.textContent = state.solved ? 'Solved' : 'In progress';
    stateEl.className = state.solved ? 'win' : '';
  }

  function tryMove(x, y) {
    if (state.solved) return;
    const dirs = [[1,0],[-1,0],[0,1],[0,-1]];
    const current = state.board[y][x];
    if (current === 'A') return invalid('Select an adjacent empty space to move into.');
    if (current !== '.') return invalid('That tile cannot be moved.');
    for (const [dx, dy] of dirs) {
      const ax = x + dx, ay = y + dy;
      if (state.board[ay]?.[ax] === 'A') {
        const next = cloneBoard(state.board);
        next[y][x] = 'A';
        next[ay][ax] = '.';
        state.board = next;
        state.moves += 1;
        state.startedAt = Date.now() - elapsed();
        if (isSolved()) finish();
        saveState(); render(); messageEl.textContent = 'Move accepted.';
        return;
      }
    }
    invalid('No adjacent block to move into that space.');
  }

  function invalid(msg) {
    messageEl.textContent = msg;
    boardEl.classList.remove('flash'); void boardEl.offsetWidth; boardEl.classList.add('flash');
    const firstTile = boardEl.querySelector('.tile');
    if (firstTile) firstTile.classList.add('invalid');
    setTimeout(() => boardEl.querySelectorAll('.invalid').forEach(n => n.classList.remove('invalid')), 350);
  }

  function isSolved() { return state.board[2][2] === 'A'; }
  function finish() {
    state.solved = true;
    state.elapsedMs = elapsed();
    const entry = { time: format(state.elapsedMs), moves: state.moves, score: score() };
    const history = loadHistory(); history.unshift(entry); saveHistory(history.slice(0, 10));
    localStorage.removeItem(STORAGE_KEY);
    renderHistory();
    messageEl.textContent = 'Puzzle completed! Nice job.';
  }

  resetBtn.addEventListener('click', () => { state = freshState(); saveState(); messageEl.textContent = 'Puzzle reset.'; render(); });
  clearBtn.addEventListener('click', () => { localStorage.removeItem(STORAGE_KEY); messageEl.textContent = 'Saved progress cleared.'; });

  setInterval(() => { if (!state.solved) { timeEl.textContent = format(elapsed()); scoreEl.textContent = score(); } }, 250);
  renderHistory(); render(); saveState();
})();
