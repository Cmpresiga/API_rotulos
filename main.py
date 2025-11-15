from fastapi import FastAPI
from routes.label_routes import router as label_router


app = FastAPI()


app.include_router(label_router)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Label Management API"}
