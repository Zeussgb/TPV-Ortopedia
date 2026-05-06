from fastapi import APIRouter, HTTPException
from app.database import get_connection

router = APIRouter(prefix="/caja", tags=["Caja"])

@router.post("/apertura")
def abrir_caja(usuario_id: int, dinero_apertura: float):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM caja WHERE usuario_id = %s AND fecha = CURDATE() AND dinero_cierre IS NULL",
        (usuario_id,)
    )
    caja_abierta = cursor.fetchone()
    if caja_abierta:
        raise HTTPException(status_code=400, detail="Ya hay una caja abierta hoy")
    cursor.execute(
        "INSERT INTO caja (usuario_id, fecha, dinero_apertura) VALUES (%s, CURDATE(), %s)",
        (usuario_id, dinero_apertura)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensaje": "Caja abierta correctamente ✅"}

@router.post("/cierre")
def cerrar_caja(usuario_id: int, dinero_cierre: float):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM caja WHERE usuario_id = %s AND fecha = CURDATE() AND dinero_cierre IS NULL",
        (usuario_id,)
    )
    caja = cursor.fetchone()
    if not caja:
        raise HTTPException(status_code=400, detail="No hay ninguna caja abierta hoy")
    cursor.execute(
        "UPDATE caja SET dinero_cierre = %s WHERE id = %s",
        (dinero_cierre, caja["id"])
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensaje": "Caja cerrada correctamente ✅", "diferencia": dinero_cierre - caja["dinero_apertura"]}

@router.get("/{usuario_id}")
def get_caja_hoy(usuario_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM caja WHERE usuario_id = %s AND fecha = CURDATE()",
        (usuario_id,)
    )
    caja = cursor.fetchone()
    cursor.close()
    conn.close()
    return caja