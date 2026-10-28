from fastapi import APIRouter, Depends, HTTPException, status
from security_JM.seguridad_jm import jm_verificar_token, jm_requerir_rol
from models_JM.models_jm import JmLoginEsquema, JmUsuarioEsquema
from controller_JM import controller_jm as jm_controlador

jm_router_auth = APIRouter(
    prefix="/auth",
    tags=["Autenticación / Seguridad"]
)

@jm_router_auth.post("/login", summary="Iniciar sesión y generar Token JWT")
def jm_login(jm_credenciales: JmLoginEsquema):
    return jm_controlador.jm_login_usuario(jm_credenciales.correo, jm_credenciales.password)


@jm_router_auth.get("/perfil", summary="Obtener perfil del usuario autenticado")
def jm_perfil(jm_usuario=Depends(jm_verificar_token)):
    jm_id = jm_usuario.get("id_usuario")
    jm_perfil_data = jm_controlador.jm_obtener_perfil_usuario(jm_id)
    if not jm_perfil_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de usuario no encontrado"
        )
    return jm_perfil_data


@jm_router_auth.post("/registro", status_code=status.HTTP_201_CREATED, summary="Registrar usuario")
def jm_registro(jm_datos: JmUsuarioEsquema, jm_usuario=Depends(jm_requerir_rol(["ADMIN"]))):
    return jm_controlador.jm_crear_usuario(jm_datos.model_dump())

