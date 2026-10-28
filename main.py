from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from database_JM.database_jm import jm_inicializar_bd_si_esta_vacia
from routers_JM.auth_rutas_jm import jm_router_auth
from routers_JM.usuarios_rutas_jm import jm_router_usuarios
from routers_JM.categorias_rutas_jm import jm_router_categorias
from routers_JM.productos_rutas_jm import jm_router_productos
from routers_JM.insumos_rutas_jm import jm_router_insumos
from routers_JM.recetas_rutas_jm import jm_router_recetas
from routers_JM.proveedores_rutas_jm import jm_router_proveedores
from routers_JM.compras_rutas_jm import jm_router_compras
from routers_JM.clientes_rutas_jm import jm_router_clientes
from routers_JM.pedidos_rutas_jm import jm_router_pedidos
from routers_JM.calificaciones_rutas_jm import jm_router_calificaciones
from routers_JM.reportes_rutas_jm import jm_router_reportes


@asynccontextmanager
async def lifespan(app: FastAPI):
    jm_inicializar_bd_si_esta_vacia()
    yield


app = FastAPI(
    title="API REST Gastronomía - SENA CGDSS",
    version="1.0.0",
    lifespan=lifespan
)

jm_routers = [
    jm_router_auth,
    jm_router_usuarios,
    jm_router_categorias,
    jm_router_productos,
    jm_router_insumos,
    jm_router_recetas,
    jm_router_proveedores,
    jm_router_compras,
    jm_router_clientes,
    jm_router_pedidos,
    jm_router_calificaciones,
    jm_router_reportes
]

for router in jm_routers:
    app.include_router(router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
