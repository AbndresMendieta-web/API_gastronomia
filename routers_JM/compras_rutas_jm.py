from fastapi import APIRouter, Depends, HTTPException, status
from security_JM.seguridad_jm import jm_verificar_token, jm_requerir_rol
from models_JM.models_jm import JmCompraEsquema, JmCompraUpdateEsquema
from controller_JM import controller_jm as jm_controlador

jm_router_compras = APIRouter(
    prefix="/compras",
    tags=["Compras e Insumos"]
)

@jm_router_compras.get("/", summary="Listar todas las compras")
@jm_router_compras.get("", include_in_schema=False)
def jm_get_compras(jm_usuario=Depends(jm_verificar_token)):
    return jm_controlador.jm_listar_compras()


@jm_router_compras.get("/{jm_id}", summary="Obtener detalle de compra por ID")
def jm_get_compra(jm_id: int, jm_usuario=Depends(jm_verificar_token)):
    jm_resultado = jm_controlador.jm_obtener_compra(jm_id)
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Compra con ID {jm_id} no encontrada"
        )
    return jm_resultado


@jm_router_compras.post("/", status_code=status.HTTP_201_CREATED, summary="Registrar compra e incrementar inventario")
@jm_router_compras.post("", status_code=status.HTTP_201_CREATED, include_in_schema=False)
def jm_post_compra(jm_datos: JmCompraEsquema, jm_usuario=Depends(jm_requerir_rol(["ADMIN"]))):
    jm_id_usuario = jm_usuario.get("id_usuario", 1)
    jm_items_dict = [it.model_dump() for it in jm_datos.items]
    return jm_controlador.jm_registrar_compra(jm_datos.model_dump(), jm_items_dict, jm_id_usuario)


@jm_router_compras.put("/{jm_id}", summary="Actualizar datos de la compra")
def jm_put_compra(jm_id: int, jm_datos: JmCompraUpdateEsquema, jm_usuario=Depends(jm_requerir_rol(["ADMIN"]))):
    jm_resultado = jm_controlador.jm_actualizar_compra(jm_id, jm_datos.model_dump(exclude_unset=True))
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Compra con ID {jm_id} no encontrada para actualizar"
        )
    return jm_resultado


@jm_router_compras.delete("/{jm_id}", summary="Eliminar compra")
def jm_delete_compra(jm_id: int, jm_usuario=Depends(jm_requerir_rol(["ADMIN"]))):
    jm_resultado = jm_controlador.jm_eliminar_compra(jm_id)
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Compra con ID {jm_id} no encontrada"
        )
    return jm_resultado
