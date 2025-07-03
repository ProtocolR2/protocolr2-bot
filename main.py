from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

class User(BaseModel):
    idioma: str = "es"
    dia_actual: int = 1
    completado: bool = False
    repeticiones: int = 0
    puntos: int = 0
    logros: list[str] = []

db_users: Dict[str, User] = {}

def get_user(user_id: str) -> User:
    if user_id not in db_users:
        db_users[user_id] = User()
    return db_users[user_id]

def check_logros(user: User):
    if user.puntos >= 3 and "Arranque feroz" not in user.logros:
        user.logros.append("Arranque feroz")

@app.get("/hoy/{user_id}")
def ver_dia_actual(user_id: str):
    user = get_user(user_id)
    return {
        "mensaje": f"📆 Hoy estás en el Día {user.dia_actual} del protocolo.",
        "contenido": f"Contenido del Día {user.dia_actual}...",
        "acciones": ["✅ Completar", "🔁 Repetir"]
    }

@app.post("/completar/{user_id}")
def completar_dia(user_id: str):
    user = get_user(user_id)
    if user.completado:
        raise HTTPException(status_code=400, detail="Ya completaste este día")
    user.completado = True
    user.puntos += 1
    check_logros(user)
    return {"mensaje": "✅ Día completado. ¡Buen trabajo, Jefe!", "puntos": user.puntos}

@app.post("/repetir/{user_id}")
def repetir_dia(user_id: str):
    user = get_user(user_id)
    user.repeticiones += 1
    user.completado = False
    return {"mensaje": f"🔁 Repetirás el Día {user.dia_actual} mañana. ¡Tú puedes!"}

@app.post("/avanzar/{user_id}")
def avanzar_dia(user_id: str):
    user = get_user(user_id)
    if not user.completado:
        raise HTTPException(status_code=403, detail="Primero debes completar el día actual")
    user.dia_actual += 1
    user.completado = False
    return {"mensaje": f"➡️ Avanzaste al Día {user.dia_actual}. ¡Vamos!"}

@app.get("/estado/{user_id}")
def ver_estado(user_id: str):
    user = get_user(user_id)
    fase = calcular_fase(user.dia_actual)
    return {
        "Día actual": user.dia_actual,
        "Fase": fase,
        "Días completados": user.puntos,
        "Repeticiones": user.repeticiones,
        "Logros": user.logros
    }

@app.get("/dia/{n}")
def ver_dia(n: int):
    if n < 1 or n > 35:
        raise HTTPException(status_code=404, detail="Día fuera de rango")
    return {"contenido": f"Contenido del Día {n}..."}

@app.get("/logros/{user_id}")
def ver_logros(user_id: str):
    user = get_user(user_id)
    return {
        "🎖️ Días completados": user.puntos,
        "🥇 Medallas": user.logros,
        "🔁 Repeticiones": user.repeticiones
    }

@app.get("/menu/{user_id}")
def ver_menu(user_id: str):
    user = get_user(user_id)
    return {
        "menu": [
            "📖 Qué es el Protocolo R2",
            f"🥗 Mi receta de hoy (📆 Día {user.dia_actual})",
            "📚 Recetario completo",
            "✍️ Mi agenda personal",
            "🛍️ Lista de compras",
            "💡 Tips y ayuda",
            "🎯 Mis logros",
            "📢 Recomendar programa",
            "⚙️ Ajustes"
        ]
    }

def calcular_fase(dia):
    if dia <= 5:
        return "Preparación"
    elif dia <= 30:
        return "Reto"
    else:
        return "Salida"
