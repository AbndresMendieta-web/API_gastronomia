from fastapi import APIRouter, Depends, HTTPException, status
from security_JM.seguridad_jm import jm_requerir_rol
from models_JM.models_jm import JmUsuarioEsquema, JmUsuarioUpdateEsquema
from controller_JM import controller_jm as jm_controlador

jm_router_usuarios = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

@jm_router_usuarios.get("/", summary="Listar todos los usuarios")
@jm_router_usuarios.get("", include_in_schema=False)
def jm_get_usuarios(jm_usuario=Depends(jm_requerir_rol(["ADMIN"]))):
    return jm_controlador.jm_listar_usuarios()


@jm_router_usuarios.get("/{jm_id}", summary="Obtener usuario por ID")
def jm_get_usuario(jm_id: int, jm_usuario=Depends(jm_requerir_rol(["ADMIN"]))):
    jm_resultado = jm_controlador.jm_obtener_usuario(jm_id)
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {jm_id} no encontrado"
        )
    return jm_resultado


@jm_router_usuarios.post("/", status_code=status.HTTP_201_CREATED, summary="Crear un nuevo usuario")
@jm_router_usuarios.post("", status_code=status.HTTP_201_CREATED, include_in_schema=False)
def jm_post_usuario(jm_datos: JmUsuarioEsquema, jm_usuario=Depends(jm_requerir_rol(["ADMIN"]))):
    return jm_controlador.jm_crear_usuario(jm_datos.model_dump())


@jm_router_usuarios.put("/{jm_id}", summary="Actualizar usuario existente")
def jm_put_usuario(jm_id: int, jm_datos: JmUsuarioUpdateEsquema, jm_usuario=Depends(jm_requerir_rol(["ADMIN"]))):
    jm_resultado = jm_controlador.jm_actualizar_usuario(jm_id, jm_datos.model_dump(exclude_unset=True))
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {jm_id} no encontrado para actualizar"
        )
    return jm_resultado


@jm_router_usuarios.delete("/{jm_id}", summary="Eliminar o inactivar usuario")
def jm_delete_usuario(jm_id: int, jm_usuario=Depends(jm_requerir_rol(["ADMIN"]))):
    jm_resultado = jm_controlador.jm_eliminar_usuario(jm_id)
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {jm_id} no encontrado"
        )
    return jm_resultado
