from fastapi import APIRouter, Depends, HTTPException, status
from security_JM.seguridad_jm import jm_verificar_token, jm_requerir_rol
from models_JM.models_jm import JmProductoEsquema, JmProductoUpdateEsquema
from controller_JM import controller_jm as jm_controlador

jm_router_productos = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)

@jm_router_productos.get("/", summary="Listar todos los productos")
@jm_router_productos.get("", include_in_schema=False)
def jm_get_productos(jm_usuario=Depends(jm_verificar_token)):
    return jm_controlador.jm_listar_productos()


@jm_router_productos.get("/categoria/{jm_id_categoria}", summary="Listar productos por categoría")
def jm_get_productos_por_categoria(jm_id_categoria: int, jm_usuario=Depends(jm_verificar_token)):
    return jm_controlador.jm_productos_por_categoria(jm_id_categoria)


@jm_router_productos.get("/{jm_id}/receta", summary="Consultar insumos de la receta de un producto")
def jm_get_receta_producto(jm_id: int, jm_usuario=Depends(jm_verificar_token)):
    jm_prod = jm_controlador.jm_obtener_producto(jm_id)
    if not jm_prod:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {jm_id} no encontrado"
        )
    return jm_controlador.jm_receta_de_producto(jm_id)


@jm_router_productos.get("/{jm_id}/costo", summary="Calcular costo de producción y margen")
def jm_get_costo_producto(jm_id: int, jm_usuario=Depends(jm_verificar_token)):
    return jm_controlador.jm_costo_de_producto(jm_id)


@jm_router_productos.get("/{jm_id}", summary="Obtener producto por ID")
def jm_get_producto(jm_id: int, jm_usuario=Depends(jm_verificar_token)):
    jm_resultado = jm_controlador.jm_obtener_producto(jm_id)
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {jm_id} no encontrado"
        )
    return jm_resultado


@jm_router_productos.post("/", status_code=status.HTTP_201_CREATED, summary="Crear un nuevo producto")
@jm_router_productos.post("", status_code=status.HTTP_201_CREATED, include_in_schema=False)
def jm_post_producto(jm_datos: JmProductoEsquema, jm_usuario=Depends(jm_requerir_rol(["ADMIN"]))):
    return jm_controlador.jm_crear_producto(jm_datos.model_dump())


@jm_router_productos.put("/{jm_id}", summary="Actualizar producto")
def jm_put_producto(jm_id: int, jm_datos: JmProductoUpdateEsquema, jm_usuario=Depends(jm_requerir_rol(["ADMIN"]))):
    jm_resultado = jm_controlador.jm_actualizar_producto(jm_id, jm_datos.model_dump(exclude_unset=True))
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {jm_id} no encontrado para actualizar"
        )
    return jm_resultado


@jm_router_productos.delete("/{jm_id}", summary="Eliminar o inactivar producto")
def jm_delete_producto(jm_id: int, jm_usuario=Depends(jm_requerir_rol(["ADMIN"]))):
    jm_resultado = jm_controlador.jm_eliminar_producto(jm_id)
    if not jm_resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {jm_id} no encontrado"
        )
    return jm_resultado
