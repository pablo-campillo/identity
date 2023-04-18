from fastapi import FastAPI

from identity.api.api import api_router

app = FastAPI()

app.include_router(api_router, prefix="/v1")

@app.get("/")
async def root():
    return {"alive": True}