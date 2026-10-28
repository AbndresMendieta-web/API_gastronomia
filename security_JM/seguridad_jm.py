import os
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, List
import bcrypt
from dotenv import load_dotenv
from jose import JWTError, jwt
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()
jm_esquema_seguridad = HTTPBearer(auto_error=True)
jm_clave_secreta = os.getenv("SECRET_KEY")
if not jm_clave_secreta:
    raise RuntimeError("Falta la variable de entorno SECRET_KEY (defínala en el archivo .env)")
jm_algoritmo = os.getenv("ALGORITHM", "HS256")
jm_tiempo_expiracion_minutos = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "480"))


def jm_hash_password(jm_password: str) -> str:
    jm_pwd_bytes = jm_password.encode("utf-8")
    jm_sal = bcrypt.gensalt(rounds=12)
    jm_hasheada = bcrypt.hashpw(jm_pwd_bytes, jm_sal)
    return jm_hasheada.decode("utf-8")


def jm_verificar_password(jm_plain: str, jm_hashed: str) -> bool:
    try:
        return bcrypt.checkpw(jm_plain.encode("utf-8"), jm_hashed.encode("utf-8"))
    except Exception:
        return False


def jm_crear_token_acceso(jm_datos: Dict[str, Any], jm_expira_delta: Optional[timedelta] = None) -> str:
    jm_payload = jm_datos.copy()
    jm_ahora = datetime.now(timezone.utc)
    if jm_expira_delta:
        jm_expiracion = jm_ahora + jm_expira_delta
    else:
        jm_expiracion = jm_ahora + timedelta(minutes=jm_tiempo_expiracion_minutos)

    jm_payload.update({
        "exp": jm_expiracion,
        "iat": jm_ahora
    })
    return jwt.encode(jm_payload, jm_clave_secreta, algorithm=jm_algoritmo)


def jm_verificar_token(jm_credenciales: HTTPAuthorizationCredentials = Security(jm_esquema_seguridad)) -> Dict[str, Any]:
    if not jm_credenciales:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no proporcionado. Debe incluir 'Authorization: Bearer <token>'",
            headers={"WWW-Authenticate": "Bearer"}
        )

    jm_token = jm_credenciales.credentials
    try:
        jm_payload = jwt.decode(jm_token, jm_clave_secreta, algorithms=[jm_algoritmo])
        return jm_payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado. Inicie sesión nuevamente.",
            headers={"WWW-Authenticate": "Bearer"}
        )


def jm_requerir_rol(jm_roles_permitidos: List[str]):
    def jm_validador_rol(jm_usuario: Dict[str, Any] = Security(jm_verificar_token)) -> Dict[str, Any]:
        jm_rol_usuario = jm_usuario.get("rol") or jm_usuario.get("jm_rol")
        if not jm_rol_usuario or jm_rol_usuario not in jm_roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Se requiere uno de los roles: {jm_roles_permitidos}. Rol actual: '{jm_rol_usuario}'"
            )
        return jm_usuario
    return jm_validador_rol
