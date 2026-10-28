from fastapi import APIRouter, Depends, HTTPException, status
from security_JM.seguridad_jm import jm_verificar_token, jm_requerir_rol
from models_JM.models_jm import JmRecetaEsquema, JmRecetaUpdateEsquema
from controller_JM import controller_jm as jm_controlador

jm_router_recetas = APIRouter(
    prefix="/recetas",
    tags=["Recetas / Fichas Técnicas"]
)

@jm_router_recetas.get("/", summary="Listar todos los elementos de recetas")
@jm_router_recetas.get("", include_in_schema=False)
def jm_get_recetas(jm_usuario=Depends(jm_verificar_token)):
    return jm_controlador.jm_listar_recetas()


@jm_router_recetas.get("/{jm_id}", summary="Obtener receta por ID")
def jm_get_receta(jm_id: int, jm_usuario=Depends(jm_verificar_token)):
    jm_resultado = jm_controlador.jm_obtener_receta(jm_id)
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Receta con ID {jm_id} no encontrada"
        )
    return jm_resultado


@jm_router_recetas.post("/", status_code=status.HTTP_201_CREATED, summary="Asignar insumo a receta")
@jm_router_recetas.post("", status_code=status.HTTP_201_CREATED, include_in_schema=False)
def jm_post_receta(jm_datos: JmRecetaEsquema, jm_usuario=Depends(jm_requerir_rol(["ADMIN", "COCINERO"]))):
    return jm_controlador.jm_crear_receta(jm_datos.model_dump())


@jm_router_recetas.put("/{jm_id}", summary="Actualizar elemento de receta")
def jm_put_receta(jm_id: int, jm_datos: JmRecetaUpdateEsquema, jm_usuario=Depends(jm_requerir_rol(["ADMIN", "COCINERO"]))):
    jm_resultado = jm_controlador.jm_actualizar_receta(jm_id, jm_datos.model_dump(exclude_unset=True))
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Receta con ID {jm_id} no encontrada para actualizar"
        )
    return jm_resultado


@jm_router_recetas.delete("/{jm_id}", summary="Eliminar elemento de receta")
def jm_delete_receta(jm_id: int, jm_usuario=Depends(jm_requerir_rol(["ADMIN", "COCINERO"]))):
    jm_resultado = jm_controlador.jm_eliminar_receta(jm_id)
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Receta con ID {jm_id} no encontrada"
        )
    return jm_resultado
