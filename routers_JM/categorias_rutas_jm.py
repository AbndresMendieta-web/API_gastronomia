from fastapi import APIRouter, Depends, HTTPException, status
from security_JM.seguridad_jm import jm_verificar_token, jm_requerir_rol
from models_JM.models_jm import JmCategoriaEsquema, JmCategoriaUpdateEsquema
from controller_JM import controller_jm as jm_controlador

jm_router_categorias = APIRouter(
    prefix="/categorias",
    tags=["Categorías"]
)

@jm_router_categorias.get("/", summary="Listar todas las categorías")
@jm_router_categorias.get("", include_in_schema=False)
def jm_get_categorias(jm_usuario=Depends(jm_verificar_token)):
    return jm_controlador.jm_listar_categorias()


@jm_router_categorias.get("/{jm_id}", summary="Obtener categoría por ID")
def jm_get_categoria(jm_id: int, jm_usuario=Depends(jm_verificar_token)):
    jm_resultado = jm_controlador.jm_obtener_categoria(jm_id)
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {jm_id} no encontrada"
        )
    return jm_resultado


@jm_router_categorias.post("/", status_code=status.HTTP_201_CREATED, summary="Crear categoría")
@jm_router_categorias.post("", status_code=status.HTTP_201_CREATED, include_in_schema=False)
def jm_post_categoria(jm_datos: JmCategoriaEsquema, jm_usuario=Depends(jm_requerir_rol(["ADMIN"]))):
    return jm_controlador.jm_crear_categoria(jm_datos.model_dump())


@jm_router_categorias.put("/{jm_id}", summary="Actualizar categoría")
def jm_put_categoria(jm_id: int, jm_datos: JmCategoriaUpdateEsquema, jm_usuario=Depends(jm_requerir_rol(["ADMIN"]))):
    jm_resultado = jm_controlador.jm_actualizar_categoria(jm_id, jm_datos.model_dump(exclude_unset=True))
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {jm_id} no encontrada para actualizar"
        )
    return jm_resultado


@jm_router_categorias.delete("/{jm_id}", summary="Eliminar categoría")
def jm_delete_categoria(jm_id: int, jm_usuario=Depends(jm_requerir_rol(["ADMIN"]))):
    jm_resultado = jm_controlador.jm_eliminar_categoria(jm_id)
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {jm_id} no encontrada"
        )
    return jm_resultado

