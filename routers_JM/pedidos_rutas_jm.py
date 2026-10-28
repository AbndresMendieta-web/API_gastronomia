from fastapi import APIRouter, Depends, HTTPException, status
from security_JM.seguridad_jm import jm_verificar_token, jm_requerir_rol
from models_JM.models_jm import JmPedidoEsquema, JmCambioEstadoPedidoEsquema
from controller_JM import controller_jm as jm_controlador

jm_router_pedidos = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos y Comandas"]
)

@jm_router_pedidos.get("/", summary="Listar todos los pedidos")
@jm_router_pedidos.get("", include_in_schema=False)
def jm_get_pedidos(jm_usuario=Depends(jm_verificar_token)):
    return jm_controlador.jm_listar_pedidos()


@jm_router_pedidos.get("/estado/{jm_estado}", summary="Filtrar pedidos por estado")
def jm_get_pedidos_por_estado(jm_estado: str, jm_usuario=Depends(jm_verificar_token)):
    return jm_controlador.jm_pedidos_por_estado(jm_estado)


@jm_router_pedidos.get("/{jm_id}", summary="Obtener pedido por ID")
def jm_get_pedido(jm_id: int, jm_usuario=Depends(jm_verificar_token)):
    jm_resultado = jm_controlador.jm_obtener_pedido(jm_id)
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido con ID {jm_id} no encontrado"
        )
    return jm_resultado


@jm_router_pedidos.post("/", status_code=status.HTTP_201_CREATED, summary="Crear pedido y calcular total")
@jm_router_pedidos.post("", status_code=status.HTTP_201_CREATED, include_in_schema=False)
def jm_post_pedido(jm_datos: JmPedidoEsquema, jm_usuario=Depends(jm_requerir_rol(["ADMIN", "CAJERO"]))):
    jm_id_usuario = jm_usuario.get("id_usuario", 1)
    jm_items_dict = [it.model_dump() for it in jm_datos.items]
    return jm_controlador.jm_crear_pedido(jm_datos.model_dump(), jm_items_dict, jm_id_usuario)


@jm_router_pedidos.patch("/{jm_id}/estado", summary="Actualizar estado del pedido")
def jm_patch_estado_pedido(
    jm_id: int,
    jm_cambio: JmCambioEstadoPedidoEsquema,
    jm_usuario=Depends(jm_requerir_rol(["ADMIN", "COCINERO", "CAJERO"]))
):
    return jm_controlador.jm_cambiar_estado_pedido(jm_id, jm_cambio.estado)


@jm_router_pedidos.put("/{jm_id}", summary="Actualizar pedido")
def jm_put_pedido(jm_id: int, jm_datos: dict, jm_usuario=Depends(jm_requerir_rol(["ADMIN", "CAJERO"]))):
    jm_resultado = jm_controlador.jm_actualizar_pedido(jm_id, jm_datos)
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido con ID {jm_id} no encontrado"
        )
    return jm_resultado


@jm_router_pedidos.delete("/{jm_id}", summary="Eliminar o cancelar pedido")
def jm_delete_pedido(jm_id: int, jm_usuario=Depends(jm_requerir_rol(["ADMIN"]))):
    jm_resultado = jm_controlador.jm_eliminar_pedido(jm_id)
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido con ID {jm_id} no encontrado"
        )
    return jm_resultado
