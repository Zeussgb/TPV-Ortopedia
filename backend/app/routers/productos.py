from fastapi import APIRouter
from app.database import get_connection

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.get("/")
def get_productos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return productos

@router.post("/")
def crear_producto(codigo: str, nombre: str, precio: float, stock: int, stock_minimo: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO productos (codigo, nombre, precio, stock, stock_minimo) VALUES (%s, %s, %s, %s, %s)",
        (codigo, nombre, precio, stock, stock_minimo)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensaje": "Producto creado correctamente"}

@router.get("/{producto_id}")
def get_producto(producto_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id = %s", (producto_id,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()
    return producto

@router.delete("/{producto_id}")
def eliminar_producto(producto_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensaje": "Producto eliminado correctamente"}

@router.put("/{producto_id}")
def editar_producto(producto_id: int, codigo: str, nombre: str, precio: float, stock: int, stock_minimo: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE productos SET codigo=%s, nombre=%s, precio=%s, stock=%s, stock_minimo=%s WHERE id=%s",
        (codigo, nombre, precio, stock, stock_minimo, producto_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensaje": "Producto actualizado correctamente ✅"}