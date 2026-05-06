from fastapi import APIRouter, HTTPException
from app.database import get_connection
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/ventas", tags=["Ventas"])

class LineaVenta(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: float

class VentaCreate(BaseModel):
    usuario_id: int
    tipo_pago: str
    dinero_entregado: float = None
    lineas: List[LineaVenta]

@router.post("/")
def crear_venta(venta: VentaCreate):
    conn = get_connection()
    cursor = conn.cursor()
    total = sum(l.cantidad * l.precio_unitario for l in venta.lineas)
    cambio = None
    if venta.tipo_pago == "efectivo" and venta.dinero_entregado:
        cambio = venta.dinero_entregado - total
    cursor.execute(
        "INSERT INTO ventas (usuario_id, total, tipo_pago, dinero_entregado, cambio) VALUES (%s, %s, %s, %s, %s)",
        (venta.usuario_id, total, venta.tipo_pago, venta.dinero_entregado, cambio)
    )
    venta_id = cursor.lastrowid
    for linea in venta.lineas:
        cursor.execute(
            "INSERT INTO lineas_venta (venta_id, producto_id, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)",
            (venta_id, linea.producto_id, linea.cantidad, linea.precio_unitario)
        )
        cursor.execute(
            "UPDATE productos SET stock = stock - %s WHERE id = %s",
            (linea.cantidad, linea.producto_id)
        )
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensaje": "Venta registrada correctamente ✅", "venta_id": venta_id, "total": total, "cambio": cambio}

@router.get("/")
def get_ventas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ventas ORDER BY fecha DESC")
    ventas = cursor.fetchall()
    cursor.close()
    conn.close()
    return ventas

@router.get("/{venta_id}")
def get_venta(venta_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ventas WHERE id = %s", (venta_id,))
    venta = cursor.fetchone()
    cursor.execute("SELECT * FROM lineas_venta WHERE venta_id = %s", (venta_id,))
    lineas = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"venta": venta, "lineas": lineas}