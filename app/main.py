from fastapi import FastAPI

app = FastAPI(
    title="MedPark API",
    version="0.1.0",
    description="API para o sistema de gerenciamento de estacionamento MedPark."
)

# endpoint (rota) para raiz API
@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do MedPark!"}