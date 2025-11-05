from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import psycopg2

dbname = "rotulos"
user = "publico"
password = "Abcd1234"
host = "localhost"
port = "5432"

app = FastAPI()


class Label(BaseModel):
    name_prod: str
    lot_format: str
    lot_detail: str
    expiration_format: str
    expiration_detail: str


@app.get("/labels")
def get_labels():
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM labeling_guide")
        rows = cur.fetchall()
        return JSONResponse(status_code=200, content={"data": rows})
    except psycopg2.Error as error:
        print("Error establishing connection", error)
        return JSONResponse(
            status_code=500,
            content={"message": "An error occurred"}
        )
    finally:
        if conn is not None:
            conn.close()


@app.get("/label/{id}")
def get_label_by_id(id: int):
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM labeling_guide WHERE id = %s", (id,))
        row = cur.fetchone()

        if row is None:
            return JSONResponse(
                status_code=404,
                content={"message": "Label not found"}
            )

        return JSONResponse(status_code=200, content={"data": row})
    except psycopg2.Error as error:
        print("Error establishing connection", error)
        return JSONResponse(
            status_code=500,
            content={"message": "An error occurred"}
        )
    finally:
        if conn is not None:
            conn.close()


@app.post("/label")
def create_label(label: Label):
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cur = conn.cursor()

        insert_query = """
            INSERT INTO labeling_guide(
                name_prod,
                lot_format,
                lot_detail,
                expiration_format,
                expiration_detail
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """
        values = (
            label.name_prod,
            label.lot_format,
            label.lot_detail,
            label.expiration_format,
            label.expiration_detail
        )

        cur.execute(insert_query, values)
        new_id = cur.fetchone()[0]
        conn.commit()

        return JSONResponse(
            status_code=201,
            content={
                "message": "Label created successfully",
                "id": new_id
            }
        )
    except psycopg2.Error as error:
        print("Error in database operation:", error)
        conn.rollback()
        return JSONResponse(
            status_code=500,
            content={"message": "An error occurred while creating the label"}
        )
    finally:
        if conn is not None:
            conn.close()


@app.put("/label/{id}")
def update_label(id: int, label: Label):
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cur = conn.cursor()

        # First check if the label exists
        cur.execute("SELECT id FROM labeling_guide WHERE id = %s", (id,))
        if cur.fetchone() is None:
            return JSONResponse(
                status_code=404,
                content={"message": f"Label with id {id} not found"}
            )

        update_query = """
            UPDATE labeling_guide
            SET name_prod = %s,
                lot_format = %s,
                lot_detail = %s,
                expiration_format = %s,
                expiration_detail = %s
            WHERE id = %s
        """
        values = (
            label.name_prod,
            label.lot_format,
            label.lot_detail,
            label.expiration_format,
            label.expiration_detail,
            id
        )

        cur.execute(update_query, values)
        conn.commit()

        return JSONResponse(
            status_code=200,
            content={
                "message": "Label updated successfully",
                "id": id
            }
        )
    except psycopg2.Error as error:
        print("Error in database operation:", error)
        conn.rollback()
        return JSONResponse(
            status_code=500,
            content={"message": "An error occurred while updating the label"}
        )
    finally:
        if conn is not None:
            conn.close()


@app.delete("/label/{id}")
def delete_label(id: int):
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cur = conn.cursor()

        # First check if the label exists
        cur.execute("SELECT id FROM labeling_guide WHERE id = %s", (id,))
        if cur.fetchone() is None:
            return JSONResponse(
                status_code=404,
                content={"message": f"Label with id {id} not found"}
            )

        cur.execute("DELETE FROM labeling_guide WHERE id = %s", (id,))
        conn.commit()

        return JSONResponse(
            status_code=200,
            content={
                "message": f"Label with id {id} deleted successfully"
            }
        )
    except psycopg2.Error as error:
        print("Error in database operation:", error)
        conn.rollback()
        return JSONResponse(
            status_code=500,
            content={"message": "An error occurred while deleting the label"}
        )
    finally:
        if conn is not None:
            conn.close()
