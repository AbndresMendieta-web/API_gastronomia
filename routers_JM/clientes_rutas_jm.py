from fastapi import APIRouter, Depends, HTTPException, status
from security_JM.seguridad_jm import jm_verificar_token, jm_requerir_rol
from models_JM.models_jm import JmClienteEsquema, JmClienteUpdateEsquema
from controller_JM import controller_jm as jm_controlador

jm_router_clientes = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)

@jm_router_clientes.get("/", summary="Listar todos los clientes")
@jm_router_clientes.get("", include_in_schema=False)
def jm_get_clientes(jm_usuario=Depends(jm_verificar_token)):
    return jm_controlador.jm_listar_clientes()


@jm_router_clientes.get("/{jm_id}/pedidos", summary="Consultar pedidos asociados a un cliente")
def jm_get_pedidos_cliente(jm_id: int, jm_usuario=Depends(jm_verificar_token)):
    jm_cli = jm_controlador.jm_obtener_cliente(jm_id)
    if not jm_cli:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con ID {jm_id} no encontrado"
        )
    return jm_controlador.jm_pedidos_por_cliente(jm_id)


@jm_router_clientes.get("/{jm_id}", summary="Obtener cliente por ID")
def jm_get_cliente(jm_id: int, jm_usuario=Depends(jm_verificar_token)):
    jm_resultado = jm_controlador.jm_obtener_cliente(jm_id)
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con ID {jm_id} no encontrado"
        )
    return jm_resultado


@jm_router_clientes.post("/", status_code=status.HTTP_201_CREATED, summary="Registrar nuevo cliente")
@jm_router_clientes.post("", status_code=status.HTTP_201_CREATED, include_in_schema=False)
def jm_post_cliente(jm_datos: JmClienteEsquema, jm_usuario=Depends(jm_verificar_token)):
    return jm_controlador.jm_crear_cliente(jm_datos.model_dump())


@jm_router_clientes.put("/{jm_id}", summary="Actualizar datos del cliente")
def jm_put_cliente(jm_id: int, jm_datos: JmClienteUpdateEsquema, jm_usuario=Depends(jm_verificar_token)):
    jm_resultado = jm_controlador.jm_actualizar_cliente(jm_id, jm_datos.model_dump(exclude_unset=True))
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con ID {jm_id} no encontrado para actualizar"
        )
    return jm_resultado


@jm_router_clientes.delete("/{jm_id}", summary="Eliminar o inactivar cliente")
def jm_delete_cliente(jm_id: int, jm_usuario=Depends(jm_requerir_rol(["ADMIN"]))):
    jm_resultado = jm_controlador.jm_eliminar_cliente(jm_id)
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con ID {jm_id} no encontrado"
        )
    return jm_resultado
