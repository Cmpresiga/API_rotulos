from pydantic import BaseModel


class Label(BaseModel):
    name_prod: str
    lot_format: str
    lot_detail: str
    expiration_format: str
    expiration_detail: str
