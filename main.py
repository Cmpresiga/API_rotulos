from fastapi import FastAPI
from controllers.label_controller import get_labels, get_label_by_id, \
    create_label, update_label, delete_label
from models.label_model import Label


app = FastAPI()


@app.get("/labels")
async def read_labels():
    return await get_labels()


@app.get("/label/{id}")
async def read_label(id: int):
    return await get_label_by_id(id)


@app.post("/label")
async def add_label(label: 'Label'):
    return await create_label(label)


@app.put("/label/{id}")
async def modify_label(id: int, label: 'Label'):
    return await update_label(id, label)


@app.delete("/label/{id}")
async def remove_label(id: int):
    return await delete_label(id)
