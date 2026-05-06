from fastapi import APIRouter, HTTPException
from app.database import get_connection
from passlib.context import CryptContext

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

@router.post("/")
def crear_usuario(nombre: str, password: str, rol: str):
    conn = get_connection()
    cursor = conn.cursor()
    password_hash = pwd_context.hash(password)
    cursor.execute(
        "INSERT INTO usuarios (nombre, password, rol) VALUES (%s, %s, %s)",
        (nombre, password_hash, rol)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensaje": "Usuario creado correctamente ✅"}

@router.post("/login")
def login(nombre: str, password: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE nombre = %s", (nombre,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    if not usuario or not pwd_context.verify(password, usuario["password"]):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    return {"mensaje": "Login correcto ✅", "rol": usuario["rol"], "id": usuario["id"]}

@router.get("/")
def get_usuarios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, rol FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return usuarios