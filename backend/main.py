from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permitir CORS para pruebas web/futuras PWAs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Podés restringir luego
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base de datos simulada en memoria
usuarios = {}

# Datos de ejemplo para cada día
contenidos = {
    1: "🥣 Día 1 – Caldo ancestral detox",
    2: "🥗 Día 2 – Ensalada de hojas verdes",
    3: "🍵 Día 3 – Smoothie revitalizante",
    4: "🥒 Día 4 – Sopa fría de pepino",
    5: "🍲 Día 5 – Puré de raíces",
    6: "🍚 Día 6 – Arroz con vegetales",
    # … hasta 35
    35: "🍹 Día 35 – Licuado de salida",
}

# Obtener fase según el día
def obtener_fase(dia: int):
    if dia <= 5:
        return "Preparación"
    elif 6 <= dia <= 30:
        return "Reto"
    else:
        return "Salida"

# Inicializar usuario si no existe
def init_usuario(user_id: str):
    if user_id not in usuarios:
        usuarios[user_id] = {
            "idioma": "es",
            "dia_actual": 1,
            "completado": False,
            "puntos": 0,
            "repeticiones": 0,
            "logros": []
        }

@app.get("/")
def raiz():
    return {"mensaje": "API ProtocolR2 funcionando"}

@app.get("/estado/{user_id}")
def estado(user_id: str):
    init_usuario(user_id)
    u = usuarios[user_id]
    return {
        "Día actual": u["dia_actual"],
        "Fase": obtener_fase(u["dia_actual"]),
        "Días completados": u["puntos"],
        "Repeticiones": u["repeticiones"],
        "Logros": u["logros"]
    }

@app.get("/hoy/{user_id}")
def hoy(user_id: str):
    init_usuario(user_id)
    dia = usuarios[user_id]["dia_actual"]
    contenido = contenidos.get(dia, "No hay contenido para este día.")
    return {
        "mensaje": f"📆 Hoy es el Día {dia} del protocolo.",
        "contenido": contenido
    }

@app.post("/completar/{user_id}")
def completar(user_id: str):
    init_usuario(user_id)
    u = usuarios[user_id]
    if u["completado"]:
        raise HTTPException(status_code=400, detail="El día ya fue marcado como completado.")
    u["completado"] = True
    u["puntos"] += 1

    # Lógica de logros
    if u["puntos"] == 3 and "Arranque feroz" not in u["logros"]:
        u["logros"].append("Arranque feroz")
    return {
        "mensaje": "✅ Día completado. ¡Buen trabajo, Jefe!",
        "puntos": u["puntos"]
    }

@app.post("/repetir/{user_id}")
def repetir(user_id: str):
    init_usuario(user_id)
    u = usuarios[user_id]
    u["completado"] = False
    u["repeticiones"] += 1
    return {"mensaje": "🔁 Día repetido. Mañana verás el mismo contenido."}

@app.post("/avanzar/{user_id}")
def avanzar(user_id: str):
    init_usuario(user_id)
    u = usuarios[user_id]
    if not u["completado"]:
        raise HTTPException(status_code=403, detail="Primero debes completar el día actual.")
    if u["dia_actual"] >= 35:
        raise HTTPException(status_code=400, detail="¡Ya completaste todos los días!")
    u["dia_actual"] += 1
    u["completado"] = False
    return {"mensaje": f"➡️ Avanzaste al Día {u['dia_actual']}"}

@app.get("/logros/{user_id}")
def logros(user_id: str):
    init_usuario(user_id)
    u = usuarios[user_id]
    return {
        "🎖️ Días completados": u["puntos"],
        "🥇 Medallas": u["logros"],
        "🔁 Repeticiones": u["repeticiones"]
    }

@app.get("/dia/{n}")
def dia_especifico(n: int):
    if n < 1 or n > 35:
        raise HTTPException(status_code=404, detail="Día fuera de rango")
    return {
        "contenido": contenidos.get(n, "No hay contenido disponible.")
    }

@app.get("/menu/{user_id}")
def menu(user_id: str):
    init_usuario(user_id)
    u = usuarios[user_id]
    return {
        "menu": {
            "📖": "Qué es el Protocolo R2",
            "🥗": f"Mi receta de hoy (📆 Día {u['dia_actual']})",
            "📚": "Recetario completo",
            "✍️": "Mi agenda personal",
            "🛍️": "Lista de compras",
            "💡": "Tips y ayuda",
            "🎯": "Mis logros",
            "📢": "Recomendar programa",
            "⚙️": "Ajustes"
        }
    }
