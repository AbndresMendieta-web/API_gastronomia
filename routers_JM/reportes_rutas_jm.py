from typing import Optional
from fastapi import APIRouter, Depends, Query
from security_JM.seguridad_jm import jm_requerir_rol
from controller_JM import controller_jm as jm_controlador

jm_router_reportes = APIRouter(
    prefix="/reportes",
    tags=["Reportes y Estadísticas"]
)

@jm_router_reportes.get("/ventas", summary="Reporte general de ventas por rango de fechas")
def jm_get_reporte_ventas(
    desde: Optional[str] = Query(None, description="Fecha de inicio (YYYY-MM-DD)"),
    hasta: Optional[str] = Query(None, description="Fecha fin (YYYY-MM-DD)"),
    jm_usuario=Depends(jm_requerir_rol(["ADMIN", "CAJERO"]))
):
    return jm_controlador.jm_reporte_ventas(jm_desde=desde, jm_hasta=hasta)


@jm_router_reportes.get("/productos-mas-vendidos", summary="Ranking de productos más vendidos")
def jm_get_ranking_productos(
    limite: int = Query(10, ge=1, le=100, description="Cantidad máxima de productos a listar"),
    jm_usuario=Depends(jm_requerir_rol(["ADMIN", "CAJERO"]))
):
    return jm_controlador.jm_reporte_productos_mas_vendidos(jm_limite=limite)
