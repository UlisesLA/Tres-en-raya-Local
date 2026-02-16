# Tic Tac Toe Multiplayer (Flask + JavaScript)

Aplicación web de Tres en Raya (Tic Tac Toe) con backend en Flask y frontend en JavaScript puro.

El sistema permite que dos dispositivos conectados en la misma red jueguen en tiempo real mediante un modelo simple basado en polling periódico al servidor.

---

## Descripción General

Este proyecto implementa:

- Servidor web con Flask.
- Estado global del juego en memoria.
- API REST para interacción del frontend.
- Cliente web dinámico con JavaScript.
- Sistema básico de control de conexiones.
- Sin base de datos.
- Sin WebSockets (usa polling).

El juego está diseñado para funcionar en red local (LAN).

---

## Tecnologías Utilizadas

### Backend
- Python 3
- Flask

### Frontend
- HTML
- CSS
- JavaScript (Vanilla JS)
- Fetch API

---

## Arquitectura del Sistema

El servidor mantiene el estado global del juego en memoria:

- board → lista de 9 posiciones.
- current_player → jugador actual ('X' u 'O').
- connected_users → contador de conexiones activas.

El frontend consulta periódicamente el estado mediante polling cada 700 ms.

---

## Estructura del Proyecto

```
/proyecto
│
├── app.py                # Servidor Flask
├── templates/
│   └── index.html        # Interfaz principal
├── static/
│   ├── script.js         # Lógica del cliente
│   └── style.css         # Estilos visuales
└── README.md
```

---

## Instalación y Ejecución

### 1. Crear entorno virtual (recomendado)

```
python -m venv .venv
source .venv/bin/activate       # Linux/Mac
.venv\Scripts\activate          # Windows
```

### 2. Instalar dependencias

```
pip install flask
```

O crear `requirements.txt`:

```
Flask
```

Y luego:

```
pip install -r requirements.txt
```

### 3. Ejecutar el servidor

```
python app.py
```

El servidor correrá en:

```
http://0.0.0.0:5000
```

Desde otro dispositivo en la misma red:

```
http://IP_DE_TU_COMPUTADORA:5000
```

---

## Endpoints del Backend

### GET /

Renderiza la interfaz principal.

---

### GET /health

Verifica que el servidor esté activo.

Respuesta:

```
{ "ok": true }
```

---

### GET /state

Devuelve el estado actual del juego:

```
{
  "board": [...],
  "current": "X",
  "winner": null,
  "connections": 2
}
```

---

### GET/POST /connect

Incrementa el contador de conexiones.

---

### POST /move

Recibe una jugada:

```
{
  "index": 4
}
```

Valida:

- Que el índice exista.
- Que esté dentro de 0–8.
- Que la casilla esté vacía.
- Que no haya ganador previo.

---

### POST /reset

Reinicia el tablero y el turno.

---

## Lógica del Juego

### Representación del tablero

Lista de 9 posiciones:

```
board = ['', '', '', '', '', '', '', '', '']
```

Índices:

```
0 | 1 | 2
3 | 4 | 5
6 | 7 | 8
```

---

### Verificación de Ganador

Se evalúan combinaciones ganadoras:

- Filas
- Columnas
- Diagonales

Si todas las posiciones están llenas sin ganador → empate.

---

## Sincronización

El sistema utiliza polling:

```
setInterval(updateBoard, 700);
```

Cada cliente consulta `/state` cada 700 ms.

Ventajas:
- Implementación simple.
- Sin WebSockets.
- Fácil de mantener.

Limitaciones:
- No es tiempo real puro.
- Consume más peticiones HTTP.

---

## Sistema de Conexiones

Cada cliente llama a `/connect` al cargar la página.

El servidor incrementa un contador global:

```
connected_users += 1
```

El frontend muestra:

- Número de jugadores conectados.
- Mensaje de espera si hay menos de 2 jugadores.

Nota: No existe autenticación ni identificación real de usuarios.

---

## Estado Global en Memoria

Importante:

- El juego vive en memoria.
- Si el servidor se reinicia, se pierde el estado.
- No es persistente.
- No es escalable para múltiples partidas simultáneas.

---

## Seguridad y Limitaciones

- No hay autenticación.
- No hay control de sesiones.
- No hay protección contra múltiples pestañas.
- No apto para producción.
- Pensado para aprendizaje y práctica de arquitectura cliente-servidor.

---

## Mejoras Futuras

- WebSockets en lugar de polling.
- Manejo de múltiples salas.
- Identificación de jugadores.
- Persistencia con base de datos.
- Sistema de ranking.
- Despliegue en la nube.
- Dockerización.
- Autenticación con tokens.

---

## Conceptos Aprendidos en el Proyecto

- Arquitectura cliente-servidor.
- REST API básica.
- Manejo de estado global.
- Validación backend.
- Sincronización mediante polling.
- Interacción frontend-backend con Fetch API.
- Control de flujo en Flask.
- Diseño de lógica de juego.

---

## Propósito Educativo

Este proyecto está diseñado para:

- Aprender Flask.
- Entender comunicación HTTP.
- Practicar lógica de juegos.
- Comprender sincronización básica entre clientes.
- Preparar el camino hacia WebSockets y sistemas en tiempo real.

---

## Autor

Desarrollado por Ulises Amezcua.

---

## Licencia

Uso educativo y experimental.