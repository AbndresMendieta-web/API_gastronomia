from fastapi import APIRouter, Depends, HTTPException, status
from security_JM.seguridad_jm import jm_verificar_token, jm_requerir_rol
from models_JM.models_jm import JmCalificacionEsquema, JmCalificacionUpdateEsquema
from controller_JM import controller_jm as jm_controlador

jm_router_calificaciones = APIRouter(
    prefix="/calificaciones",
    tags=["Calificaciones de Clientes"]
)

@jm_router_calificaciones.get("/", summary="Listar todas las calificaciones")
@jm_router_calificaciones.get("", include_in_schema=False)
def jm_get_calificaciones(jm_usuario=Depends(jm_verificar_token)):
    return jm_controlador.jm_listar_calificaciones()


@jm_router_calificaciones.get("/producto/{jm_id_producto}", summary="Consultar calificaciones y promedio de un producto")
def jm_get_calificaciones_producto(jm_id_producto: int, jm_usuario=Depends(jm_verificar_token)):
    return jm_controlador.jm_calificaciones_por_producto(jm_id_producto)


@jm_router_calificaciones.get("/{jm_id}", summary="Obtener calificación por ID")
def jm_get_calificacion(jm_id: str, jm_usuario=Depends(jm_verificar_token)):
    jm_resultado = jm_controlador.jm_obtener_calificacion(jm_id)
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Calificación con ID '{jm_id}' no encontrada"
        )
    return jm_resultado


@jm_router_calificaciones.post("/", status_code=status.HTTP_201_CREATED, summary="Registrar calificación de pedido/productos")
@jm_router_calificaciones.post("", status_code=status.HTTP_201_CREATED, include_in_schema=False)
def jm_post_calificacion(jm_datos: JmCalificacionEsquema, jm_usuario=Depends(jm_verificar_token)):
    return jm_controlador.jm_crear_calificacion(jm_datos.model_dump())


@jm_router_calificaciones.put("/{jm_id}", summary="Actualizar calificación")
def jm_put_calificacion(jm_id: str, jm_datos: JmCalificacionUpdateEsquema, jm_usuario=Depends(jm_verificar_token)):
    jm_resultado = jm_controlador.jm_actualizar_calificacion(jm_id, jm_datos.model_dump(exclude_unset=True))
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Calificación con ID '{jm_id}' no encontrada para actualizar"
        )
    return jm_resultado


@jm_router_calificaciones.delete("/{jm_id}", summary="Eliminar calificación")
def jm_delete_calificacion(jm_id: str, jm_usuario=Depends(jm_requerir_rol(["ADMIN"]))):
    jm_resultado = jm_controlador.jm_eliminar_calificacion(jm_id)
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Calificación con ID '{jm_id}' no encontrada"
        )
    return jm_resultado
