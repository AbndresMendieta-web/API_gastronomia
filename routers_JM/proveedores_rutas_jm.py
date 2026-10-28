from fastapi import APIRouter, Depends, HTTPException, status
from security_JM.seguridad_jm import jm_verificar_token, jm_requerir_rol
from models_JM.models_jm import JmProveedorEsquema, JmProveedorUpdateEsquema
from controller_JM import controller_jm as jm_controlador

jm_router_proveedores = APIRouter(
    prefix="/proveedores",
    tags=["Proveedores"]
)

@jm_router_proveedores.get("/", summary="Listar todos los proveedores")
@jm_router_proveedores.get("", include_in_schema=False)
def jm_get_proveedores(jm_usuario=Depends(jm_verificar_token)):
    return jm_controlador.jm_listar_proveedores()


@jm_router_proveedores.get("/{jm_id}/compras", summary="Consultar compras asociadas a un proveedor")
def jm_get_compras_proveedor(jm_id: int, jm_usuario=Depends(jm_verificar_token)):
    jm_prov = jm_controlador.jm_obtener_proveedor(jm_id)
    if not jm_prov:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proveedor con ID {jm_id} no encontrado"
        )
    return jm_controlador.jm_compras_por_proveedor(jm_id)


@jm_router_proveedores.get("/{jm_id}", summary="Obtener proveedor por ID")
def jm_get_proveedor(jm_id: int, jm_usuario=Depends(jm_verificar_token)):
    jm_resultado = jm_controlador.jm_obtener_proveedor(jm_id)
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proveedor con ID {jm_id} no encontrado"
        )
    return jm_resultado


@jm_router_proveedores.post("/", status_code=status.HTTP_201_CREATED, summary="Registrar nuevo proveedor")
@jm_router_proveedores.post("", status_code=status.HTTP_201_CREATED, include_in_schema=False)
def jm_post_proveedor(jm_datos: JmProveedorEsquema, jm_usuario=Depends(jm_requerir_rol(["ADMIN"]))):
    return jm_controlador.jm_crear_proveedor(jm_datos.model_dump())


@jm_router_proveedores.put("/{jm_id}", summary="Actualizar proveedor")
def jm_put_proveedor(jm_id: int, jm_datos: JmProveedorUpdateEsquema, jm_usuario=Depends(jm_requerir_rol(["ADMIN"]))):
    jm_resultado = jm_controlador.jm_actualizar_proveedor(jm_id, jm_datos.model_dump(exclude_unset=True))
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proveedor con ID {jm_id} no encontrado para actualizar"
        )
    return jm_resultado


@jm_router_proveedores.delete("/{jm_id}", summary="Eliminar o inactivar proveedor")
def jm_delete_proveedor(jm_id: int, jm_usuario=Depends(jm_requerir_rol(["ADMIN"]))):
    jm_resultado = jm_controlador.jm_eliminar_proveedor(jm_id)
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proveedor con ID {jm_id} no encontrado"
        )
    return jm_resultado
