from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Backend de ProtocolR2 activo"}

@app.get("/estado")
def get_estado():
    return {
        "Día actual": 1,
        "Fase": "Preparación",
        "Días completados": 0,
        "Repeticiones": 0,
        "Logros": []
    }
@app.get("/ping")
def ping():
    return "OK"
