from datetime import datetime, timezone, date, timedelta
from typing import List, Optional, Dict, Any
from bson import ObjectId
from fastapi import HTTPException, status

from database_JM.database_jm import jm_obtener_db, jm_obtener_siguiente_id
from security_JM.seguridad_jm import jm_hash_password, jm_verificar_password, jm_crear_token_acceso


def _limpiar_doc(jm_doc: Optional[Dict[str, Any]], jm_incluir_password: bool = False) -> Optional[Dict[str, Any]]:
    if not jm_doc:
        return None
    jm_res = jm_doc.copy()
    if "_id" in jm_res:
        if isinstance(jm_res["_id"], ObjectId):
            jm_res["id_mongodb"] = str(jm_res["_id"])
        del jm_res["_id"]
    if not jm_incluir_password and "password" in jm_res:
        del jm_res["password"]
    return jm_res


def jm_login_usuario(jm_correo: str, jm_password: str) -> Dict[str, Any]:
    jm_db = jm_obtener_db()
    jm_usuario = jm_db.usuarios.find_one({"correo": jm_correo.strip().lower()})
    if not jm_usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Correo o contraseña incorrectos")

    if not jm_verificar_password(jm_password, jm_usuario.get("password", "")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Correo o contraseña incorrectos")

    if jm_usuario.get("estado") != "ACTIVO":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="El usuario se encuentra INACTIVO")

    jm_payload = {
        "sub": jm_usuario["correo"],
        "id_usuario": jm_usuario["id_usuario"],
        "rol": jm_usuario["rol"],
        "jm_usuario": f"{jm_usuario['nombres']} {jm_usuario['apellidos']}"
    }
    jm_token = jm_crear_token_acceso(jm_payload)
    return {
        "access_token": jm_token,
        "token_type": "bearer",
        "rol": jm_usuario["rol"],
        "usuario": _limpiar_doc(jm_usuario)
    }


def jm_obtener_perfil_usuario(jm_id_usuario: int) -> Optional[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    jm_doc = jm_db.usuarios.find_one({"id_usuario": jm_id_usuario})
    return _limpiar_doc(jm_doc)


def jm_listar_usuarios() -> List[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    return [_limpiar_doc(d) for d in jm_db.usuarios.find().sort("id_usuario", 1)]


def jm_obtener_usuario(jm_id: int) -> Optional[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    return _limpiar_doc(jm_db.usuarios.find_one({"id_usuario": jm_id}))


def jm_crear_usuario(jm_datos: dict) -> Dict[str, Any]:
    jm_db = jm_obtener_db()
    if jm_db.usuarios.find_one({"correo": jm_datos["correo"]}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo ya está registrado")
    if jm_db.usuarios.find_one({"identificacion": jm_datos["identificacion"]}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La identificación ya está registrada")

    jm_nuevo_id = jm_obtener_siguiente_id("usuarios", "id_usuario")
    jm_doc = jm_datos.copy()
    jm_doc["id_usuario"] = jm_nuevo_id
    jm_doc["password"] = jm_hash_password(jm_doc["password"])
    jm_doc["estado"] = jm_doc.get("estado", "ACTIVO")
    jm_db.usuarios.insert_one(jm_doc)
    return _limpiar_doc(jm_db.usuarios.find_one({"id_usuario": jm_nuevo_id}))


def jm_actualizar_usuario(jm_id: int, jm_datos: dict) -> Optional[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    jm_existente = jm_db.usuarios.find_one({"id_usuario": jm_id})
    if not jm_existente:
        return None

    jm_mod = {k: v for k, v in jm_datos.items() if v is not None}
    if "password" in jm_mod and jm_mod["password"]:
        jm_mod["password"] = jm_hash_password(jm_mod["password"])

    if "correo" in jm_mod and jm_mod["correo"] != jm_existente["correo"]:
        if jm_db.usuarios.find_one({"correo": jm_mod["correo"]}):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo ya está en uso")

    if jm_mod:
        jm_db.usuarios.update_one({"id_usuario": jm_id}, {"$set": jm_mod})
    return _limpiar_doc(jm_db.usuarios.find_one({"id_usuario": jm_id}))


def jm_eliminar_usuario(jm_id: int) -> Dict[str, Any]:
    jm_db = jm_obtener_db()
    jm_pedidos = jm_db.pedidos.count_documents({"id_usuario": jm_id})
    jm_compras = jm_db.compras.count_documents({"id_usuario": jm_id})
    if jm_pedidos > 0 or jm_compras > 0:
        jm_db.usuarios.update_one({"id_usuario": jm_id}, {"$set": {"estado": "INACTIVO"}})
        return {"mensaje": "Usuario inactivado por poseer transacciones registradas", "estado": "INACTIVO", "tipo": "inactivado"}
    jm_db.usuarios.delete_one({"id_usuario": jm_id})
    return {"mensaje": "Usuario eliminado físicamente con éxito", "tipo": "eliminado"}


def jm_listar_categorias() -> List[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    return [_limpiar_doc(d) for d in jm_db.categorias.find().sort("id_categoria", 1)]


def jm_obtener_categoria(jm_id: int) -> Optional[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    return _limpiar_doc(jm_db.categorias.find_one({"id_categoria": jm_id}))


def jm_crear_categoria(jm_datos: dict) -> Dict[str, Any]:
    jm_db = jm_obtener_db()
    if jm_db.categorias.find_one({"nombre": jm_datos["nombre"]}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La categoría ya existe")
    jm_nuevo_id = jm_obtener_siguiente_id("categorias", "id_categoria")
    jm_doc = jm_datos.copy()
    jm_doc["id_categoria"] = jm_nuevo_id
    jm_db.categorias.insert_one(jm_doc)
    return _limpiar_doc(jm_db.categorias.find_one({"id_categoria": jm_nuevo_id}))


def jm_actualizar_categoria(jm_id: int, jm_datos: dict) -> Optional[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    jm_mod = {k: v for k, v in jm_datos.items() if v is not None}
    if jm_mod:
        jm_db.categorias.update_one({"id_categoria": jm_id}, {"$set": jm_mod})
    return _limpiar_doc(jm_db.categorias.find_one({"id_categoria": jm_id}))


def jm_eliminar_categoria(jm_id: int) -> Dict[str, Any]:
    jm_db = jm_obtener_db()
    if jm_db.productos.count_documents({"id_categoria": jm_id}) > 0:
        jm_db.categorias.update_one({"id_categoria": jm_id}, {"$set": {"estado": "INACTIVO"}})
        return {"mensaje": "Categoría inactivada por tener productos asociados", "estado": "INACTIVO", "tipo": "inactivado"}
    jm_db.categorias.delete_one({"id_categoria": jm_id})
    return {"mensaje": "Categoría eliminada exitosamente", "tipo": "eliminado"}


def jm_listar_productos() -> List[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    return [_limpiar_doc(d) for d in jm_db.productos.find().sort("id_producto", 1)]


def jm_obtener_producto(jm_id: int) -> Optional[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    return _limpiar_doc(jm_db.productos.find_one({"id_producto": jm_id}))


def jm_crear_producto(jm_datos: dict) -> Dict[str, Any]:
    jm_db = jm_obtener_db()
    if jm_db.productos.find_one({"codigo": jm_datos["codigo"]}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El código de producto ya existe")
    jm_nuevo_id = jm_obtener_siguiente_id("productos", "id_producto")
    jm_doc = jm_datos.copy()
    jm_doc["id_producto"] = jm_nuevo_id
    jm_db.productos.insert_one(jm_doc)
    return _limpiar_doc(jm_db.productos.find_one({"id_producto": jm_nuevo_id}))


def jm_actualizar_producto(jm_id: int, jm_datos: dict) -> Optional[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    jm_mod = {k: v for k, v in jm_datos.items() if v is not None}
    if jm_mod:
        jm_db.productos.update_one({"id_producto": jm_id}, {"$set": jm_mod})
    return _limpiar_doc(jm_db.productos.find_one({"id_producto": jm_id}))


def jm_eliminar_producto(jm_id: int) -> Dict[str, Any]:
    jm_db = jm_obtener_db()
    jm_en_pedidos = jm_db.pedidos.count_documents({"items.id_producto": jm_id})
    jm_en_recetas = jm_db.recetas.count_documents({"id_producto": jm_id})
    if jm_en_pedidos > 0 or jm_en_recetas > 0:
        jm_db.productos.update_one({"id_producto": jm_id}, {"$set": {"estado": "INACTIVO"}})
        return {"mensaje": "Producto inactivado por tener transacciones históricas", "estado": "INACTIVO", "tipo": "inactivado"}
    jm_db.productos.delete_one({"id_producto": jm_id})
    return {"mensaje": "Producto eliminado físicamente con éxito", "tipo": "eliminado"}


def jm_productos_por_categoria(jm_id_categoria: int) -> List[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    return [_limpiar_doc(d) for d in jm_db.productos.find({"id_categoria": jm_id_categoria})]


def jm_receta_de_producto(jm_id_producto: int) -> List[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    jm_recetas = list(jm_db.recetas.find({"id_producto": jm_id_producto}))
    jm_res = []
    for r in jm_recetas:
        ins = jm_db.insumos.find_one({"id_insumo": r["id_insumo"]})
        r_limpio = _limpiar_doc(r)
        r_limpio["insumo_nombre"] = ins["nombre"] if ins else None
        r_limpio["unidad_medida"] = ins["unidad_medida"] if ins else None
        jm_res.append(r_limpio)
    return jm_res


def jm_costo_de_producto(jm_id_producto: int) -> Dict[str, Any]:
    jm_db = jm_obtener_db()
    jm_prod = jm_db.productos.find_one({"id_producto": jm_id_producto})
    if not jm_prod:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

    jm_recetas = list(jm_db.recetas.find({"id_producto": jm_id_producto}))
    jm_costo_total = 0.0
    jm_detalles = []
    for r in jm_recetas:
        ins = jm_db.insumos.find_one({"id_insumo": r["id_insumo"]})
        costo_u = float(ins.get("costo_unitario", 0.0)) if ins else 0.0
        cant = float(r.get("cantidad", 0.0))
        subtotal_ins = cant * costo_u
        jm_costo_total += subtotal_ins
        jm_detalles.append({
            "id_insumo": r["id_insumo"],
            "insumo_nombre": ins["nombre"] if ins else "Desconocido",
            "cantidad": cant,
            "unidad_medida": ins["unidad_medida"] if ins else "",
            "costo_unitario": costo_u,
            "costo_parcial": round(subtotal_ins, 2)
        })

    precio_v = float(jm_prod.get("precio_venta", 0.0))
    margen = precio_v - jm_costo_total
    pct = (margen / precio_v * 100.0) if precio_v > 0 else 0.0

    return {
        "id_producto": jm_id_producto,
        "nombre_producto": jm_prod["nombre"],
        "precio_venta": precio_v,
        "costo_produccion": round(jm_costo_total, 2),
        "margen_ganancia": round(margen, 2),
        "porcentaje_margen": round(pct, 2),
        "insumos": jm_detalles
    }


def jm_listar_insumos() -> List[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    return [_limpiar_doc(d) for d in jm_db.insumos.find().sort("id_insumo", 1)]


def jm_obtener_insumo(jm_id: int) -> Optional[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    return _limpiar_doc(jm_db.insumos.find_one({"id_insumo": jm_id}))


def jm_crear_insumo(jm_datos: dict) -> Dict[str, Any]:
    jm_db = jm_obtener_db()
    if jm_db.insumos.find_one({"nombre": jm_datos["nombre"]}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El insumo ya está registrado")
    jm_nuevo_id = jm_obtener_siguiente_id("insumos", "id_insumo")
    jm_doc = jm_datos.copy()
    jm_doc["id_insumo"] = jm_nuevo_id
    jm_db.insumos.insert_one(jm_doc)
    return _limpiar_doc(jm_db.insumos.find_one({"id_insumo": jm_nuevo_id}))


def jm_actualizar_insumo(jm_id: int, jm_datos: dict) -> Optional[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    jm_mod = {k: v for k, v in jm_datos.items() if v is not None}
    if jm_mod:
        jm_db.insumos.update_one({"id_insumo": jm_id}, {"$set": jm_mod})
    return _limpiar_doc(jm_db.insumos.find_one({"id_insumo": jm_id}))


def jm_eliminar_insumo(jm_id: int) -> Dict[str, Any]:
    jm_db = jm_obtener_db()
    jm_en_recetas = jm_db.recetas.count_documents({"id_insumo": jm_id})
    jm_en_compras = jm_db.compras.count_documents({"detalles.id_insumo": jm_id})
    if jm_en_recetas > 0 or jm_en_compras > 0:
        jm_db.insumos.update_one({"id_insumo": jm_id}, {"$set": {"estado": "INACTIVO"}})
        return {"mensaje": "Insumo inactivado por poseer movimientos asociados", "estado": "INACTIVO", "tipo": "inactivado"}
    jm_db.insumos.delete_one({"id_insumo": jm_id})
    return {"mensaje": "Insumo eliminado físicamente con éxito", "tipo": "eliminado"}


def jm_insumos_stock_bajo() -> List[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    cursor = jm_db.insumos.find({"$expr": {"$lte": ["$stock_actual", "$stock_minimo"]}})
    return [_limpiar_doc(d) for d in cursor]


def jm_insumos_por_vencer(dias: int = 7) -> List[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    hoy = date.today()
    limite = hoy + timedelta(days=dias)
    hoy_str = hoy.isoformat()
    limite_str = limite.isoformat()

    cursor = jm_db.insumos.find({
        "fecha_vencimiento": {"$gte": hoy_str, "$lte": limite_str},
        "estado": "ACTIVO"
    }).sort("fecha_vencimiento", 1)
    return [_limpiar_doc(d) for d in cursor]


def jm_listar_recetas() -> List[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    return [_limpiar_doc(d) for d in jm_db.recetas.find().sort("id_receta", 1)]


def jm_obtener_receta(jm_id: int) -> Optional[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    return _limpiar_doc(jm_db.recetas.find_one({"id_receta": jm_id}))


def jm_crear_receta(jm_datos: dict) -> Dict[str, Any]:
    jm_db = jm_obtener_db()
    jm_nuevo_id = jm_obtener_siguiente_id("recetas", "id_receta")
    jm_doc = jm_datos.copy()
    jm_doc["id_receta"] = jm_nuevo_id
    jm_db.recetas.insert_one(jm_doc)
    return _limpiar_doc(jm_db.recetas.find_one({"id_receta": jm_nuevo_id}))


def jm_actualizar_receta(jm_id: int, jm_datos: dict) -> Optional[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    jm_mod = {k: v for k, v in jm_datos.items() if v is not None}
    if jm_mod:
        jm_db.recetas.update_one({"id_receta": jm_id}, {"$set": jm_mod})
    return _limpiar_doc(jm_db.recetas.find_one({"id_receta": jm_id}))


def jm_eliminar_receta(jm_id: int) -> Dict[str, Any]:
    jm_db = jm_obtener_db()
    jm_db.recetas.delete_one({"id_receta": jm_id})
    return {"mensaje": "Receta eliminada exitosamente"}


def jm_listar_proveedores() -> List[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    return [_limpiar_doc(d) for d in jm_db.proveedores.find().sort("id_proveedor", 1)]


def jm_obtener_proveedor(jm_id: int) -> Optional[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    return _limpiar_doc(jm_db.proveedores.find_one({"id_proveedor": jm_id}))


def jm_crear_proveedor(jm_datos: dict) -> Dict[str, Any]:
    jm_db = jm_obtener_db()
    if jm_db.proveedores.find_one({"nit": jm_datos["nit"]}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El NIT ya está registrado")
    jm_nuevo_id = jm_obtener_siguiente_id("proveedores", "id_proveedor")
    jm_doc = jm_datos.copy()
    jm_doc["id_proveedor"] = jm_nuevo_id
    jm_db.proveedores.insert_one(jm_doc)
    return _limpiar_doc(jm_db.proveedores.find_one({"id_proveedor": jm_nuevo_id}))


def jm_actualizar_proveedor(jm_id: int, jm_datos: dict) -> Optional[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    jm_mod = {k: v for k, v in jm_datos.items() if v is not None}
    if jm_mod:
        jm_db.proveedores.update_one({"id_proveedor": jm_id}, {"$set": jm_mod})
    return _limpiar_doc(jm_db.proveedores.find_one({"id_proveedor": jm_id}))


def jm_eliminar_proveedor(jm_id: int) -> Dict[str, Any]:
    jm_db = jm_obtener_db()
    if jm_db.compras.count_documents({"id_proveedor": jm_id}) > 0:
        jm_db.proveedores.update_one({"id_proveedor": jm_id}, {"$set": {"estado": "INACTIVO"}})
        return {"mensaje": "Proveedor inactivado por tener compras asociadas", "estado": "INACTIVO", "tipo": "inactivado"}
    jm_db.proveedores.delete_one({"id_proveedor": jm_id})
    return {"mensaje": "Proveedor eliminado físicamente con éxito", "tipo": "eliminado"}


def jm_compras_por_proveedor(jm_id_proveedor: int) -> List[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    return [_limpiar_doc(d) for d in jm_db.compras.find({"id_proveedor": jm_id_proveedor}).sort("fecha_compra", -1)]


def jm_listar_compras() -> List[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    return [_limpiar_doc(d) for d in jm_db.compras.find().sort("fecha_compra", -1)]


def jm_obtener_compra(jm_id: int) -> Optional[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    return _limpiar_doc(jm_db.compras.find_one({"id_compra": jm_id}))


def jm_registrar_compra(jm_datos: dict, jm_items: list, jm_id_usuario: int) -> Dict[str, Any]:
    jm_db = jm_obtener_db()
    jm_prov = jm_db.proveedores.find_one({"id_proveedor": jm_datos["id_proveedor"]})
    if not jm_prov:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado")

    jm_total = 0.0
    jm_detalles_procesados = []
    jm_detalle_id = 1

    for it in jm_items:
        cant = float(it["cantidad"])
        costo_u = float(it["costo_unitario"])
        subt = cant * costo_u
        jm_total += subt

        jm_detalles_procesados.append({
            "id_detalle_compra": jm_detalle_id,
            "id_insumo": it["id_insumo"],
            "cantidad": cant,
            "costo_unitario": costo_u,
            "subtotal": round(subt, 2)
        })
        jm_detalle_id += 1

        jm_insumo = jm_db.insumos.find_one({"id_insumo": it["id_insumo"]})
        if jm_insumo:
            jm_db.insumos.update_one(
                {"id_insumo": it["id_insumo"]},
                {
                    "$inc": {"stock_actual": cant},
                    "$set": {"costo_unitario": costo_u}
                }
            )

    jm_nuevo_id = jm_obtener_siguiente_id("compras", "id_compra")
    jm_doc_compra = {
        "id_compra": jm_nuevo_id,
        "numero_factura": jm_datos["numero_factura"],
        "fecha_compra": datetime.now(timezone.utc),
        "id_proveedor": jm_datos["id_proveedor"],
        "id_usuario": jm_id_usuario,
        "total": round(jm_total, 2),
        "detalles": jm_detalles_procesados
    }
    jm_db.compras.insert_one(jm_doc_compra)
    return _limpiar_doc(jm_db.compras.find_one({"id_compra": jm_nuevo_id}))


def jm_actualizar_compra(jm_id: int, jm_datos: dict) -> Optional[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    jm_mod = {k: v for k, v in jm_datos.items() if v is not None and k not in ["id_compra", "detalles", "total"]}
    if jm_mod:
        jm_db.compras.update_one({"id_compra": jm_id}, {"$set": jm_mod})
    return _limpiar_doc(jm_db.compras.find_one({"id_compra": jm_id}))


def jm_eliminar_compra(jm_id: int) -> Dict[str, Any]:
    jm_db = jm_obtener_db()
    jm_db.compras.delete_one({"id_compra": jm_id})
    return {"mensaje": "Compra eliminada exitosamente"}


def jm_listar_clientes() -> List[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    return [_limpiar_doc(d) for d in jm_db.clientes.find().sort("id_cliente", 1)]


def jm_obtener_cliente(jm_id: int) -> Optional[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    return _limpiar_doc(jm_db.clientes.find_one({"id_cliente": jm_id}))


def jm_crear_cliente(jm_datos: dict) -> Dict[str, Any]:
    jm_db = jm_obtener_db()
    if jm_db.clientes.find_one({"identificacion": jm_datos["identificacion"]}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La identificación ya está registrada")
    jm_nuevo_id = jm_obtener_siguiente_id("clientes", "id_cliente")
    jm_doc = jm_datos.copy()
    jm_doc["id_cliente"] = jm_nuevo_id
    jm_db.clientes.insert_one(jm_doc)
    return _limpiar_doc(jm_db.clientes.find_one({"id_cliente": jm_nuevo_id}))


def jm_actualizar_cliente(jm_id: int, jm_datos: dict) -> Optional[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    jm_mod = {k: v for k, v in jm_datos.items() if v is not None}
    if jm_mod:
        jm_db.clientes.update_one({"id_cliente": jm_id}, {"$set": jm_mod})
    return _limpiar_doc(jm_db.clientes.find_one({"id_cliente": jm_id}))


def jm_eliminar_cliente(jm_id: int) -> Dict[str, Any]:
    jm_db = jm_obtener_db()
    if jm_db.pedidos.count_documents({"id_cliente": jm_id}) > 0:
        jm_db.clientes.update_one({"id_cliente": jm_id}, {"$set": {"estado": "INACTIVO"}})
        return {"mensaje": "Cliente inactivado por tener pedidos históricos", "estado": "INACTIVO", "tipo": "inactivado"}
    jm_db.clientes.delete_one({"id_cliente": jm_id})
    return {"mensaje": "Cliente eliminado físicamente con éxito", "tipo": "eliminado"}


def jm_pedidos_por_cliente(jm_id_cliente: int) -> List[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    return [_limpiar_doc(d) for d in jm_db.pedidos.find({"id_cliente": jm_id_cliente}).sort("fecha_pedido", -1)]


def jm_listar_pedidos() -> List[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    return [_limpiar_doc(d) for d in jm_db.pedidos.find().sort("fecha_pedido", -1)]


def jm_obtener_pedido(jm_id: int) -> Optional[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    return _limpiar_doc(jm_db.pedidos.find_one({"id_pedido": jm_id}))


def jm_crear_pedido(jm_datos: dict, jm_items: list, jm_id_usuario: int) -> Dict[str, Any]:
    jm_db = jm_obtener_db()
    jm_cli = jm_db.clientes.find_one({"id_cliente": jm_datos["id_cliente"]})
    if not jm_cli:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    if jm_cli.get("estado") == "INACTIVO":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El cliente está INACTIVO")

    jm_total_pedido = 0.0
    jm_items_procesados = []
    jm_det_id = 1

    for it in jm_items:
        prod = jm_db.productos.find_one({"id_producto": it["id_producto"]})
        if not prod:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Producto {it['id_producto']} no existe")

        precio_oficial = float(prod.get("precio_venta", 0.0))
        cant = float(it["cantidad"])
        subt = cant * precio_oficial
        jm_total_pedido += subt

        jm_items_procesados.append({
            "id_detalle": jm_det_id,
            "id_producto": it["id_producto"],
            "producto_nombre": prod["nombre"],
            "cantidad": cant,
            "precio_unitario": precio_oficial,
            "subtotal": round(subt, 2)
        })
        jm_det_id += 1

    jm_nuevo_id = jm_obtener_siguiente_id("pedidos", "id_pedido")
    jm_doc_pedido = {
        "id_pedido": jm_nuevo_id,
        "fecha_pedido": datetime.now(timezone.utc),
        "id_cliente": jm_datos["id_cliente"],
        "id_usuario": jm_id_usuario,
        "tipo_pedido": jm_datos.get("tipo_pedido", "MESA"),
        "estado": "PENDIENTE",
        "total": round(jm_total_pedido, 2),
        "observaciones": jm_datos.get("observaciones", ""),
        "items": jm_items_procesados
    }
    jm_db.pedidos.insert_one(jm_doc_pedido)
    return _limpiar_doc(jm_db.pedidos.find_one({"id_pedido": jm_nuevo_id}))


def jm_actualizar_pedido(jm_id: int, jm_datos: dict) -> Optional[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    jm_ped = jm_db.pedidos.find_one({"id_pedido": jm_id})
    if not jm_ped:
        return None
    if jm_ped.get("estado") in ["ENTREGADO", "ANULADO"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede modificar un pedido en estado '{jm_ped['estado']}'"
        )
    jm_mod = {k: v for k, v in jm_datos.items() if v is not None and k not in ["id_pedido", "estado", "total", "items"]}
    if jm_mod:
        jm_db.pedidos.update_one({"id_pedido": jm_id}, {"$set": jm_mod})
    return _limpiar_doc(jm_db.pedidos.find_one({"id_pedido": jm_id}))


def jm_eliminar_pedido(jm_id: int) -> Dict[str, Any]:
    jm_db = jm_obtener_db()
    jm_ped = jm_db.pedidos.find_one({"id_pedido": jm_id})
    if not jm_ped:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")
    if jm_ped.get("estado") in ["ENTREGADO", "ANULADO"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No se puede eliminar un pedido '{jm_ped['estado']}'")
    jm_db.pedidos.delete_one({"id_pedido": jm_id})
    return {"mensaje": "Pedido eliminado correctamente"}


def jm_pedidos_por_estado(jm_estado: str) -> List[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    return [_limpiar_doc(d) for d in jm_db.pedidos.find({"estado": jm_estado.upper()})]


def jm_cambiar_estado_pedido(jm_id: int, jm_nuevo_estado: str) -> Dict[str, Any]:
    jm_db = jm_obtener_db()
    jm_ped = jm_db.pedidos.find_one({"id_pedido": jm_id})
    if not jm_ped:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")

    jm_estado_actual = jm_ped.get("estado")
    if jm_estado_actual in ["ENTREGADO", "ANULADO"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede modificar un pedido en estado '{jm_estado_actual}'"
        )

    jm_nuevo_estado_upper = jm_nuevo_estado.upper()

    if jm_nuevo_estado_upper == "ENTREGADO":
        jm_insumos_requeridos: Dict[int, float] = {}
        for it in jm_ped.get("items", []):
            recetas = list(jm_db.recetas.find({"id_producto": it["id_producto"]}))
            for r in recetas:
                ins_id = r["id_insumo"]
                cant_necesaria = float(r["cantidad"]) * float(it["cantidad"])
                jm_insumos_requeridos[ins_id] = jm_insumos_requeridos.get(ins_id, 0.0) + cant_necesaria

        for ins_id, cant_total in jm_insumos_requeridos.items():
            ins = jm_db.insumos.find_one({"id_insumo": ins_id})
            if not ins:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Insumo {ins_id} no existe")
            stock_actual = float(ins.get("stock_actual", 0.0))
            if stock_actual < cant_total:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=(
                        f"Conflicto de stock para entregar el pedido. "
                        f"Insumo '{ins['nombre']}' tiene {ins['stock_actual']} disponible, "
                        f"pero se requieren {cant_total}."
                    )
                )

        for ins_id, cant_total in jm_insumos_requeridos.items():
            jm_db.insumos.update_one(
                {"id_insumo": ins_id},
                {"$inc": {"stock_actual": -cant_total}}
            )

    jm_db.pedidos.update_one({"id_pedido": jm_id}, {"$set": {"estado": jm_nuevo_estado_upper}})
    return _limpiar_doc(jm_db.pedidos.find_one({"id_pedido": jm_id}))


def jm_listar_calificaciones() -> List[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    return [_limpiar_doc(d) for d in jm_db.calificaciones.find().sort("fecha", -1)]


def jm_obtener_calificacion(jm_id: str) -> Optional[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    try:
        doc = jm_db.calificaciones.find_one({"_id": ObjectId(jm_id)})
    except Exception:
        doc = None
    return _limpiar_doc(doc)


def jm_crear_calificacion(jm_datos: dict) -> Dict[str, Any]:
    jm_db = jm_obtener_db()
    jm_doc = jm_datos.copy()
    if not jm_doc.get("fecha"):
        jm_doc["fecha"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    res = jm_db.calificaciones.insert_one(jm_doc)
    nuevo = jm_db.calificaciones.find_one({"_id": res.inserted_id})
    return _limpiar_doc(nuevo)


def jm_actualizar_calificacion(jm_id: str, jm_datos: dict) -> Optional[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    jm_mod = {k: v for k, v in jm_datos.items() if v is not None}
    if jm_mod:
        jm_db.calificaciones.update_one({"_id": ObjectId(jm_id)}, {"$set": jm_mod})
    return _limpiar_doc(jm_db.calificaciones.find_one({"_id": ObjectId(jm_id)}))


def jm_eliminar_calificacion(jm_id: str) -> Dict[str, Any]:
    jm_db = jm_obtener_db()
    jm_db.calificaciones.delete_one({"_id": ObjectId(jm_id)})
    return {"mensaje": "Calificación eliminada correctamente"}


def jm_calificaciones_por_producto(jm_id_producto: int) -> Dict[str, Any]:
    jm_db = jm_obtener_db()
    jm_prod = jm_db.productos.find_one({"id_producto": jm_id_producto})
    nombre_prod = jm_prod["nombre"] if jm_prod else f"Producto {jm_id_producto}"

    pipeline = [
        {"$unwind": "$productos"},
        {"$match": {"productos.id_producto": jm_id_producto}},
        {"$group": {
            "_id": "$productos.id_producto",
            "promedio": {"$avg": "$productos.calificacion"},
            "total_opiniones": {"$sum": 1}
        }}
    ]
    agregados = list(jm_db.calificaciones.aggregate(pipeline))
    promedio = float(agregados[0]["promedio"]) if agregados else 0.0
    total_evals = int(agregados[0]["total_opiniones"]) if agregados else 0

    cursor_comentarios = jm_db.calificaciones.find(
        {"productos.id_producto": jm_id_producto},
        {"fecha": 1, "calificacion_servicio": 1, "comentario": 1, "productos.$": 1}
    )
    opiniones = []
    for c in cursor_comentarios:
        c_limpio = _limpiar_doc(c)
        opiniones.append(c_limpio)

    return {
        "id_producto": jm_id_producto,
        "nombre_producto": nombre_prod,
        "promedio": round(promedio, 2),
        "promedio_calificacion": round(promedio, 2),
        "total_evaluaciones": total_evals,
        "opiniones": opiniones
    }


def jm_reporte_ventas(jm_desde: Optional[str] = None, jm_hasta: Optional[str] = None) -> Dict[str, Any]:
    jm_db = jm_obtener_db()
    filtro: Dict[str, Any] = {"estado": "ENTREGADO"}
    rango_fecha: Dict[str, Any] = {}
    if jm_desde:
        rango_fecha["$gte"] = datetime.fromisoformat(jm_desde)
    if jm_hasta:
        rango_fecha["$lte"] = datetime.fromisoformat(jm_hasta)
    if rango_fecha:
        filtro["fecha_pedido"] = rango_fecha

    pipeline = [
        {"$match": filtro},
        {"$group": {
            "_id": None,
            "total_ventas": {"$sum": "$total"},
            "numero_pedidos": {"$sum": 1}
        }}
    ]
    res = list(jm_db.pedidos.aggregate(pipeline))
    total = float(res[0]["total_ventas"]) if res else 0.0
    num = int(res[0]["numero_pedidos"]) if res else 0
    return {
        "periodo_desde": jm_desde,
        "periodo_hasta": jm_hasta,
        "total_ventas": round(total, 2),
        "numero_pedidos_entregados": num
    }


def jm_reporte_productos_mas_vendidos(jm_limite: int = 10) -> List[Dict[str, Any]]:
    jm_db = jm_obtener_db()
    pipeline = [
        {"$match": {"estado": "ENTREGADO"}},
        {"$unwind": "$items"},
        {"$group": {
            "_id": "$items.id_producto",
            "producto_nombre": {"$first": "$items.producto_nombre"},
            "total_cantidad_vendida": {"$sum": "$items.cantidad"},
            "total_recaudado": {"$sum": "$items.subtotal"}
        }},
        {"$sort": {"total_cantidad_vendida": -1}},
        {"$limit": jm_limite}
    ]
    agregados = list(jm_db.pedidos.aggregate(pipeline))
    resultado = []
    for a in agregados:
        resultado.append({
            "id_producto": a["_id"],
            "producto_nombre": a.get("producto_nombre", f"Producto {a['_id']}"),
            "cantidad_vendida": a["total_cantidad_vendida"],
            "total_recaudado": round(a["total_recaudado"], 2)
        })
    return resultado
