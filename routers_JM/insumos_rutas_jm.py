from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from security_JM.seguridad_jm import jm_verificar_token, jm_requerir_rol
from models_JM.models_jm import JmInsumoEsquema, JmInsumoUpdateEsquema
from controller_JM import controller_jm as jm_controlador

jm_router_insumos = APIRouter(
    prefix="/insumos",
    tags=["Insumos e Inventario"]
)

@jm_router_insumos.get("/", summary="Listar todos los insumos")
@jm_router_insumos.get("", include_in_schema=False)
def jm_get_insumos(jm_usuario=Depends(jm_verificar_token)):
    return jm_controlador.jm_listar_insumos()


@jm_router_insumos.get("/stock-bajo", summary="Insumos con stock crítico bajo")
def jm_get_insumos_stock_bajo(jm_usuario=Depends(jm_verificar_token)):
    return jm_controlador.jm_insumos_stock_bajo()


@jm_router_insumos.get("/por-vencer", summary="Insumos próximos a vencer")
def jm_get_insumos_por_vencer(dias: int = Query(7, ge=1, description="Días hacia adelante a consultar"), jm_usuario=Depends(jm_verificar_token)):
    return jm_controlador.jm_insumos_por_vencer(dias=dias)


@jm_router_insumos.get("/{jm_id}", summary="Obtener insumo por ID")
def jm_get_insumo(jm_id: int, jm_usuario=Depends(jm_verificar_token)):
    jm_resultado = jm_controlador.jm_obtener_insumo(jm_id)
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Insumo con ID {jm_id} no encontrado"
        )
    return jm_resultado


@jm_router_insumos.post("/", status_code=status.HTTP_201_CREATED, summary="Registrar nuevo insumo")
@jm_router_insumos.post("", status_code=status.HTTP_201_CREATED, include_in_schema=False)
def jm_post_insumo(jm_datos: JmInsumoEsquema, jm_usuario=Depends(jm_requerir_rol(["ADMIN", "COCINERO"]))):
    return jm_controlador.jm_crear_insumo(jm_datos.model_dump())


@jm_router_insumos.put("/{jm_id}", summary="Actualizar insumo")
def jm_put_insumo(jm_id: int, jm_datos: JmInsumoUpdateEsquema, jm_usuario=Depends(jm_requerir_rol(["ADMIN", "COCINERO"]))):
    jm_resultado = jm_controlador.jm_actualizar_insumo(jm_id, jm_datos.model_dump(exclude_unset=True))
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Insumo con ID {jm_id} no encontrado para actualizar"
        )
    return jm_resultado


@jm_router_insumos.delete("/{jm_id}", summary="Eliminar o inactivar insumo")
def jm_delete_insumo(jm_id: int, jm_usuario=Depends(jm_requerir_rol(["ADMIN"]))):
    jm_resultado = jm_controlador.jm_eliminar_insumo(jm_id)
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Insumo con ID {jm_id} no encontrado"
        )
    return jm_resultado
