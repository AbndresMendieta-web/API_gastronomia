from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator


class JmLoginEsquema(BaseModel):
    correo: str
    password: str

    @field_validator('correo')
    @classmethod
    def jm_validar_correo(cls, valor: str) -> str:
        if '@' not in valor or '.' not in valor:
            raise ValueError("El correo debe tener un formato válido con '@' y '.'")
        return valor.strip().lower()

    @field_validator('password')
    @classmethod
    def jm_validar_password(cls, valor: str) -> str:
        if len(valor) < 4:
            raise ValueError("La contraseña debe tener al menos 4 caracteres")
        return valor


class JmUsuarioEsquema(BaseModel):
    identificacion: str
    nombres: str
    apellidos: str
    correo: str
    password: str
    rol: str = "CAJERO"
    estado: Optional[str] = "ACTIVO"

    @field_validator('correo')
    @classmethod
    def jm_validar_correo_usuario(cls, valor: str) -> str:
        if '@' not in valor:
            raise ValueError("El correo es inválido")
        return valor.strip().lower()

    @field_validator('rol')
    @classmethod
    def jm_validar_rol(cls, valor: str) -> str:
        roles_validos = ["ADMIN", "CAJERO", "COCINERO"]
        if valor.upper() not in roles_validos:
            raise ValueError(f"Rol no válido. Permitidos: {roles_validos}")
        return valor.upper()


class JmUsuarioUpdateEsquema(BaseModel):
    identificacion: Optional[str] = None
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    correo: Optional[str] = None
    password: Optional[str] = None
    rol: Optional[str] = None
    estado: Optional[str] = None


class JmCategoriaEsquema(BaseModel):
    nombre: str
    descripcion: Optional[str] = ""
    estado: Optional[str] = "ACTIVO"

    @field_validator('nombre')
    @classmethod
    def jm_validar_nombre_categoria(cls, valor: str) -> str:
        if len(valor.strip()) < 3:
            raise ValueError("El nombre de la categoría debe tener al menos 3 caracteres")
        return valor.strip()


class JmCategoriaUpdateEsquema(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[str] = None


class JmProductoEsquema(BaseModel):
    codigo: str
    nombre: str
    descripcion: Optional[str] = ""
    precio_venta: float = Field(..., gt=0)
    unidad_venta: str = "Porción"
    id_categoria: int
    estado: Optional[str] = "DISPONIBLE"


class JmProductoUpdateEsquema(BaseModel):
    codigo: Optional[str] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio_venta: Optional[float] = None
    unidad_venta: Optional[str] = None
    id_categoria: Optional[int] = None
    estado: Optional[str] = None


class JmInsumoEsquema(BaseModel):
    nombre: str
    unidad_medida: str
    stock_actual: float = Field(0.0, ge=0)
    stock_minimo: float = Field(0.0, ge=0)
    costo_unitario: float = Field(0.0, ge=0)
    fecha_vencimiento: Optional[str] = None
    estado: Optional[str] = "ACTIVO"


class JmInsumoUpdateEsquema(BaseModel):
    nombre: Optional[str] = None
    unidad_medida: Optional[str] = None
    stock_actual: Optional[float] = None
    stock_minimo: Optional[float] = None
    costo_unitario: Optional[float] = None
    fecha_vencimiento: Optional[str] = None
    estado: Optional[str] = None


class JmRecetaEsquema(BaseModel):
    id_producto: int
    id_insumo: int
    cantidad: float = Field(..., gt=0)


class JmRecetaUpdateEsquema(BaseModel):
    cantidad: Optional[float] = None


class JmProveedorEsquema(BaseModel):
    nit: str
    razon_social: str
    telefono: Optional[str] = ""
    correo: Optional[str] = ""
    direccion: Optional[str] = ""
    estado: Optional[str] = "ACTIVO"


class JmProveedorUpdateEsquema(BaseModel):
    nit: Optional[str] = None
    razon_social: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    direccion: Optional[str] = None
    estado: Optional[str] = None


class JmDetalleCompraItemEsquema(BaseModel):
    id_insumo: int
    cantidad: float = Field(..., gt=0)
    costo_unitario: float = Field(..., ge=0)


class JmCompraEsquema(BaseModel):
    numero_factura: str
    id_proveedor: int
    items: List[JmDetalleCompraItemEsquema]


class JmCompraUpdateEsquema(BaseModel):
    numero_factura: Optional[str] = None
    id_proveedor: Optional[int] = None


class JmClienteEsquema(BaseModel):
    identificacion: str
    nombres: str
    apellidos: str
    telefono: Optional[str] = ""
    correo: Optional[str] = ""
    tipo_cliente: str = "APRENDIZ"
    estado: Optional[str] = "ACTIVO"

    @field_validator('tipo_cliente')
    @classmethod
    def jm_validar_tipo_cliente(cls, valor: str) -> str:
        tipos = ["APRENDIZ", "INSTRUCTOR", "FUNCIONARIO", "EXTERNO"]
        if valor.upper() not in tipos:
            raise ValueError(f"Tipo de cliente no válido. Permitidos: {tipos}")
        return valor.upper()


class JmClienteUpdateEsquema(BaseModel):
    identificacion: Optional[str] = None
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    tipo_cliente: Optional[str] = None
    estado: Optional[str] = None


class JmItemPedidoEsquema(BaseModel):
    id_producto: int
    cantidad: float = Field(..., gt=0)


class JmPedidoEsquema(BaseModel):
    id_cliente: int
    tipo_pedido: str = "MESA"
    observaciones: Optional[str] = ""
    items: List[JmItemPedidoEsquema]


class JmCambioEstadoPedidoEsquema(BaseModel):
    estado: str

    @field_validator('estado')
    @classmethod
    def jm_validar_estado_pedido(cls, valor: str) -> str:
        estados = ["PENDIENTE", "EN_PREPARACION", "ENTREGADO", "ANULADO"]
        if valor.upper() not in estados:
            raise ValueError(f"Estado de pedido no válido. Permitidos: {estados}")
        return valor.upper()


class JmItemCalificacionProductoEsquema(BaseModel):
    id_producto: int
    nombre: str
    calificacion: int = Field(..., ge=1, le=5)


class JmCalificacionEsquema(BaseModel):
    id_pedido: int
    id_cliente: int
    fecha: Optional[str] = None
    calificacion_servicio: int = Field(..., ge=1, le=5)
    comentario: str
    productos: List[JmItemCalificacionProductoEsquema]


class JmCalificacionUpdateEsquema(BaseModel):
    calificacion_servicio: Optional[int] = Field(None, ge=1, le=5)
    comentario: Optional[str] = None
