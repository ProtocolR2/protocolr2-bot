from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Protocolo R2 API funcionando"}

# Aquí va el resto de tus endpoints actuales...
