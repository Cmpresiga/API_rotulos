from fastapi.responses import JSONResponse
from database import get_connection
from models.label_model import Label


async def get_labels():
    try:
        conn = await get_connection()
        rows = await conn.fetch("SELECT * FROM labeling_guide;")
        rows = [dict(row) for row in rows]
        return JSONResponse(status_code=200, content={"data": rows})
    except Exception as error:
        print("Error establishing connection", error)
        return JSONResponse(
            status_code=500,
            content={"message": "An error occurred"}
        )
    finally:
        if conn is not None:
            await conn.close()


async def get_label_by_id(id: int):
    try:
        conn = await get_connection()
        row = await conn.fetchrow(
            "SELECT * FROM labeling_guide WHERE id = $1;", id
        )

        if row is None:
            return JSONResponse(
                status_code=404,
                content={"message": "Label not found"}
            )

        row = dict(row)
        return JSONResponse(status_code=200, content={"data": row})
    except Exception as error:
        print("Error establishing connection", error)
        return JSONResponse(
            status_code=500,
            content={"message": "An error occurred"}
        )
    finally:
        if conn is not None:
            await conn.close()


async def create_label(label: Label):
    try:
        conn = await get_connection()
        await conn.execute("BEGIN")

        insert_query = """
            INSERT INTO labeling_guide(
                name_prod,
                lot_format,
                lot_detail,
                expiration_format,
                expiration_detail
            )
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id
        """
        values = [
            label.name_prod,
            label.lot_format,
            label.lot_detail,
            label.expiration_format,
            label.expiration_detail
        ]

        new_id = await conn.fetchval(insert_query, *values)
        await conn.execute("COMMIT")

        return JSONResponse(
            status_code=201,
            content={
                "message": "Label created successfully",
                "id": new_id
            }
        )
    except Exception as error:
        print("Error in database operation:", error)
        await conn.execute("ROLLBACK")
        return JSONResponse(
            status_code=500,
            content={"message": "An error occurred while creating the label"}
        )
    finally:
        if conn is not None:
            await conn.close()


async def update_label(id: int, label: Label):
    try:
        conn = await get_connection()
        await conn.execute("BEGIN")

        # First check if the label exists
        row = await conn.fetchval(
            "SELECT id FROM labeling_guide WHERE id = $1", id
        )
        if row is None:
            await conn.execute("ROLLBACK")
            return JSONResponse(
                status_code=404,
                content={"message": f"Label with id {id} not found"}
            )

        update_query = """
            UPDATE labeling_guide
            SET name_prod = $1,
                lot_format = $2,
                lot_detail = $3,
                expiration_format = $4,
                expiration_detail = $5
            WHERE id = $6
        """
        values = (
            label.name_prod,
            label.lot_format,
            label.lot_detail,
            label.expiration_format,
            label.expiration_detail,
            id
        )

        await conn.execute(update_query, *values)
        await conn.execute("COMMIT")

        return JSONResponse(
            status_code=200,
            content={
                "message": "Label updated successfully",
                "id": id
            }
        )
    except Exception as error:
        print("Error in database operation:", error)
        await conn.execute("ROLLBACK")
        return JSONResponse(
            status_code=500,
            content={"message": "An error occurred while updating the label"}
        )
    finally:
        if conn is not None:
            await conn.close()


async def delete_label(id: int):
    try:
        conn = await get_connection()
        await conn.execute("BEGIN")

        # First check if the label exists
        row = await conn.fetchval(
            "SELECT id FROM labeling_guide WHERE id = $1", id
        )
        if row is None:
            await conn.execute("ROLLBACK")
            return JSONResponse(
                status_code=404,
                content={"message": f"Label with id {id} not found"}
            )

        await conn.execute("DELETE FROM labeling_guide WHERE id = $1", id)
        await conn.execute("COMMIT")

        return JSONResponse(
            status_code=200,
            content={
                "message": f"Label with id {id} deleted successfully"
            }
        )
    except Exception as error:
        print("Error in database operation:", error)
        await conn.execute("ROLLBACK")
        return JSONResponse(
            status_code=500,
            content={"message": "An error occurred while deleting the label"}
        )
    finally:
        if conn is not None:
            await conn.close()
