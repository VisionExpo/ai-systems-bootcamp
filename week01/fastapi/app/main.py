from fastapi import FastAPI
from app.routers import items

app = FastAPI(title="Items API")

app.include_router(items.router)

@app.get("/")
def root():
    return {"status": "ok"}