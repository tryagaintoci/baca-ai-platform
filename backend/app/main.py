from fastapi import FastAPI

app = FastAPI(title="BACA AI Platform", version="0.1.0")


@app.get("/")
def root():
    return {"message": "Welcome to BACA AI Platform"}
