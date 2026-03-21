from fastapi import FastAPI
from database import engine, Base
import models # <--- CETTE LIGNE EST OBLIGATOIRE !

# COMMANDE MAGIQUE
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PFE Adaptive Learning API")

@app.get("/")
def read_root():
    return {"message": "Bienvenue !"}