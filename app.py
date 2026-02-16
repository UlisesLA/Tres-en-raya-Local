# app.py
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)  # usa carpetas: templates/ y static/

# ---- Estado global del juego ----
board = [''] * 9          # 9 casillas vacías
current_player = 'X'      # X empieza
connected_users = 0       # contador simple de conexiones

# ---- Utilidades ----
def check_winner(b):
    """Devuelve 'X', 'O', 'Draw' o None según el estado del tablero."""
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    for a, bb, c in wins:
        if b[a] and b[a] == b[bb] == b[c]:
            return b[a]
    if all(b):
        return 'Draw'
    return None

@app.before_request
def _log_req():
    # Log sencillo para ver quién llama a qué
    try:
        ip = request.remote_addr
    except Exception:
        ip = "?"
    print(f"[REQ] {ip} -> {request.method} {request.path}")

@app.after_request
def add_no_cache(resp):
    # Evita que navegadores cacheen /state y similares
    resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    resp.headers['Pragma'] = 'no-cache'
    return resp

# ---- Rutas ----
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({'ok': True})

@app.route('/state', methods=['GET'])
def get_state():
    return jsonify({
        'board': board,
        'current': current_player,
        'winner': check_winner(board),
        'connections': connected_users
    })

@app.route('/connect', methods=['GET', 'POST'])
def connect_user():
    global connected_users
    connected_users += 1
    print(f"[CONNECT] {request.remote_addr} -> total={connected_users}")
    return jsonify({'connections': connected_users})

@app.route('/move', methods=['POST'])
def move():
    global current_player
    data = request.get_json(silent=True) or {}

    if 'index' not in data:
        return jsonify({'error': 'Missing index'}), 400
    try:
        idx = int(data['index'])
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid index'}), 400
    if not (0 <= idx <= 8):
        return jsonify({'error': 'Index out of bounds'}), 400

    # Jugada inválida si ya hay algo en la casilla o ya terminó
    if board[idx] or check_winner(board):
        return jsonify({'error': 'Invalid move'}), 400

    board[idx] = current_player
    winner = check_winner(board)
    if not winner:
        current_player = 'O' if current_player == 'X' else 'X'

    return jsonify({
        'board': board,
        'current': current_player,
        'winner': winner,
        'connections': connected_users
    })

@app.route('/reset', methods=['POST'])
def reset():
    global board, current_player
    board = [''] * 9
    current_player = 'X'
    return jsonify({'status': 'OK', 'connections': connected_users})

# ---- Main ----
if __name__ == '__main__':
    # Importante: 0.0.0.0 para aceptar desde otros dispositivos de la LAN
    # y use_reloader=False para que no se duplique el proceso (globals estables)
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
