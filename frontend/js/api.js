const API_URL = "http://127.0.0.1:8000";

async function login(nombre, password) {
    const res = await fetch(`${API_URL}/usuarios/login?nombre=${nombre}&password=${password}`, {
        method: "POST"
    });
    return await res.json();
}

async function getProductos() {
    const res = await fetch(`${API_URL}/productos/`);
    return await res.json();
}

async function crearProducto(codigo, nombre, precio, stock, stock_minimo) {
    const res = await fetch(`${API_URL}/productos/?codigo=${codigo}&nombre=${nombre}&precio=${precio}&stock=${stock}&stock_minimo=${stock_minimo}`, {
        method: "POST"
    });
    return await res.json();
}

async function editarProducto(id, codigo, nombre, precio, stock, stock_minimo) {
    const res = await fetch(`${API_URL}/productos/${id}?codigo=${codigo}&nombre=${nombre}&precio=${precio}&stock=${stock}&stock_minimo=${stock_minimo}`, {
        method: "PUT"
    });
    return await res.json();
}

async function eliminarProducto(id) {
    const res = await fetch(`${API_URL}/productos/${id}`, {
        method: "DELETE"
    });
    return await res.json();
}

async function crearVenta(usuario_id, tipo_pago, dinero_entregado, lineas) {
    const res = await fetch(`${API_URL}/ventas/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ usuario_id, tipo_pago, dinero_entregado, lineas })
    });
    return await res.json();
}

async function getVentas() {
    const res = await fetch(`${API_URL}/ventas/`);
    return await res.json();
}