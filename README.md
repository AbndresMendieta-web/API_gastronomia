# API REST - Unidad Productiva de Gastronomía (CGDSS)
**Centro de Gestión y Desarrollo Sostenible Surcolombiano (SENA)**  
**Programa:** Análisis y Desarrollo de Software (ADSO) — **Ficha:** 3312744  
**Evidencia EA4:** Prototipo de API REST con Python, MongoDB (NoSQL) y JWT.

---

## 1. Descripción del Proyecto

El presente proyecto implementa el backend completo de la API REST para centralizar, optimizar y controlar los procesos operativos de la Unidad Productiva de Gastronomía del CGDSS (SENA). El sistema gestiona recetas (fichas técnicas), compras de insumos a proveedores, control de existencias, cálculo automatizado de costos y márgenes de utilidad, toma y despacho de pedidos, generación de reportes financieros y recolección de calificaciones de satisfacción de comensales.

### Arquitectura 100% NoSQL Documental con MongoDB
La solución opera de manera íntegra sobre **MongoDB** (`bd_gastronomia_nosql`), eliminando dependencias de motores SQL relacionales:
- **Colecciones Maestras y de Operación:** `usuarios`, `categorias`, `productos`, `insumos`, `recetas`, `proveedores`, `clientes`.
- **Colecciones Transaccionales con Documentos Embebidos:** `compras` (con array de insumos y costos), `pedidos` (con array de ítems y precios calculados) y `calificaciones` (con array de puntuaciones individuales por producto).
- **Validación de Integridad:** Índices de unicidad (`correo`, `identificacion`, `codigo`, `nit`, `id_*`) y validación de esquemas `$jsonSchema`.

---

## 2. Tecnologías y Librerías Utilizadas

- **Lenguaje:** Python 3.11+ / Python 3.14
- **Framework Web:** FastAPI 0.143+
- **Servidor ASGI:** Uvicorn
- **Base de Datos:** MongoDB 7 / 8 (NoSQL Documental)
- **Driver de Conexión:** PyMongo
- **Validación y Modelado:** Pydantic V2 & Pydantic-Settings
- **Seguridad:** JWT (Python-Jose) + Hashing seguro con Bcrypt nativo (12 rondas de sal, RN06)
- **Contenedores:** Docker & Docker Compose (`mongo:7.0`)

---

## 3. Estructura del Proyecto

El código implementa la arquitectura modular y estándar del SENA establecida en los proyectos de referencia:

```
api_gastronomia_j/
├── controller_JM/
│   ├── __init__.py
│   └── controller_jm.py            # Lógica de negocio, consultas directas a MongoDB y reglas (RN01 - RN06)
├── database_JM/
│   ├── __init__.py
│   └── database_jm.py              # Conexión a MongoDB (PyMongo), IDs secuenciales y autoseeder al inicio
├── models_JM/
│   ├── __init__.py
│   └── models_jm.py                # Esquemas Pydantic V2 con validadores (@field_validator) y tipado estricto
├── routers_JM/
│   ├── __init__.py
│   ├── auth_rutas_jm.py            # Rutas de autenticación JWT y perfil (RF01)
│   ├── usuarios_rutas_jm.py        # Rutas de gestión de usuarios y roles RBAC (RF02)
│   ├── categorias_rutas_jm.py      # Rutas de categorías de menú (RF03)
│   ├── productos_rutas_jm.py       # Rutas de productos, recetas asociadas y costos (RF04, RF06)
│   ├── insumos_rutas_jm.py         # Rutas de insumos, alertas de stock bajo y por vencer (RF05, RF07)
│   ├── recetas_rutas_jm.py         # Rutas de fichas técnicas e insumos requeridos (RF06)
│   ├── proveedores_rutas_jm.py     # Rutas de proveedores y compras asociadas (RF08)
│   ├── compras_rutas_jm.py         # Rutas de compras con incremento automático de inventario (RF08, RN02)
│   ├── clientes_rutas_jm.py        # Rutas de comensales y pedidos históricos (RF09)
│   ├── pedidos_rutas_jm.py         # Rutas de comandas, cálculo de totales y deducción de stock (RF10, RN01, RN03, RN05)
│   ├── calificaciones_rutas_jm.py  # Rutas de satisfacción de comensales en MongoDB (RF12)
│   └── reportes_rutas_jm.py        # Rutas de reportes consolidados y ranking de productos (RF11)
├── security_JM/
│   ├── __init__.py
│   └── seguridad_jm.py             # Seguridad JWT Bearer, hashing Bcrypt (RN06) y dependencias de roles RBAC
├── database/
│   ├── 01_mongo_init.js            # Script para inicializar colecciones e índices en mongosh
├── main.py                         # Instancia central de FastAPI, lifespan y registro de todos los routers
├── docker-compose.yml              # Definición de contenedor MongoDB 7.0
├── requirements.txt                # Dependencias (FastAPI, PyMongo, Uvicorn, Jose, Bcrypt, Pydantic)
├── .env.example                    # Plantilla de variables de entorno (sin credenciales sensibles)
├── .env                            # Variables de entorno activas locales
├── postman_collection.json         # Colección exportada de Postman con pruebas de todos los servicios
├── Formato_6_Manual_de_Configuracion_de_Base_de_Datos.md # Anexo técnico oficial del SENA
└── README.md                       # Documentación principal
```

*Nota de Nomenclatura:* Se cumple rigurosamente con la convención del SENA y el proyecto de referencia de la clínica, donde los paquetes y archivos usan el sufijo del estudiante (`_JM` / `_jm`) y todas las funciones, esquemas y variables emplean el prefijo asignado (`jm_` / `Jm...`).

---

## 4. Reglas de Negocio Implementadas

| Código | Regla de Negocio | Implementación en la API |
|---|---|---|
| **RN01** | Subtotal y total calculados por la API | En `POST /api/v1/pedidos`, la API consulta el precio oficial de cada producto en MongoDB, calcula `subtotal = cantidad * precio_unitario` y asigna `total = sum(subtotales)`. El cliente no define los totales. |
| **RN02** | Registro de compra incrementa inventario y actualiza costo | En `POST /api/v1/compras`, cada ítem comprado incrementa el `stock_actual` del insumo en MongoDB y actualiza su `costo_unitario` ponderado. |
| **RN03** | Entrega de pedido descuenta insumos de recetas (Error 409 si falta stock) | En `PATCH /api/v1/pedidos/{id}/estado` al pasar a `ENTREGADO`, la API calcula los insumos requeridos según las fichas técnicas (`recetas`). Si no hay existencias suficientes, responde con **HTTP 409 Conflict** indicando el faltante. Si hay stock, descuenta automáticamente del inventario. |
| **RN04** | Borrado lógico si existen movimientos asociados | En los endpoints `DELETE`, si un usuario, cliente, producto, insumo o proveedor tiene transacciones previas (pedidos, recetas o compras), su estado cambia a `INACTIVO` en lugar de eliminarse físicamente de MongoDB. |
| **RN05** | Inmutabilidad de pedidos terminados | Un pedido en estado `ENTREGADO` o `ANULADO` no puede ser modificado ni eliminado (responde HTTP 400 Bad Request). |
| **RN06** | Contraseñas cifradas con Bcrypt y nunca expuestas | Todas las contraseñas se almacenan con sal y hash Bcrypt; ningún esquema o endpoint retorna el campo `password`. |

---

## 5. Matriz de Control de Acceso por Rol (RBAC)

Todos los endpoints (excepto `POST /api/v1/auth/login`) están protegidos mediante JWT en el encabezado `Authorization: Bearer <token>`.
- Token no proporcionado o expirado: **HTTP 401 Unauthorized**.
- Rol sin permisos para la operación: **HTTP 403 Forbidden**.

| Recurso / Operación | Prefijo | ADMIN | CAJERO | COCINERO |
|---|---|:---:|:---:|:---:|
| Autenticación (Login) | `/api/v1/auth/login` | Público | Público | Público |
| Usuarios (CRUD) | `/api/v1/usuarios` | ✅ Total | ❌ | ❌ |
| Categorías (Lectura) | `GET /api/v1/categorias` | ✅ | ✅ | ✅ |
| Categorías (Escritura/Borrado) | `POST, PUT, DELETE /categorias` | ✅ | ❌ | ❌ |
| Productos (Lectura) | `GET /api/v1/productos` | ✅ | ✅ | ✅ |
| Productos (Costos / Receta) | `GET /productos/{id}/costo` | ✅ | ❌ | ✅ |
| Productos (Escritura/Borrado) | `POST, PUT, DELETE /productos` | ✅ | ❌ | ❌ |
| Insumos (CRUD y Alertas) | `/api/v1/insumos` | ✅ Total | ❌ | ✅ Total |
| Recetas (CRUD) | `/api/v1/recetas` | ✅ Total | ❌ | ✅ Total |
| Proveedores (CRUD e Historial) | `/api/v1/proveedores` | ✅ Total | ❌ | ❌ |
| Compras (CRUD e Inventario) | `/api/v1/compras` | ✅ Total | ❌ | ❌ |
| Clientes (CRUD e Historial) | `/api/v1/clientes` | ✅ Total | ✅ Total | ❌ |
| Pedidos (Creación, Consulta, Edición) | `/api/v1/pedidos` | ✅ Total | ✅ Total | ❌ |
| Pedidos (Cambio de Estado) | `PATCH /pedidos/{id}/estado` | ✅ | ✅ | ✅ |
| Calificaciones MongoDB (CRUD) | `/api/v1/calificaciones` | ✅ Total | ✅ Total | ❌ |
| Reportes Financieros y Ventas | `/api/v1/reportes` | ✅ Total | ❌ | ❌ |

---

## 6. Puesta en Marcha y Ejecución

### Prerrequisitos
- MongoDB Server instalado localmente (puerto 27017) o Docker Desktop.
- Python 3.11 a 3.14 instalado.

### Paso 1: Configurar variables de entorno
Copie el archivo `.env.example` a `.env` (si aún no existe) y verifique la conexión a MongoDB:
```ini
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DB=bd_gastronomia_nosql
MONGO_USER=
MONGO_PASSWORD=
SECRET_KEY=clave_secreta_super_segura_gastronomia_sena_2026_adso
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480
```

### Paso 2: Inicializar el entorno virtual de Python e instalar librerías
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Paso 3: Inicializar y poblar la Base de Datos MongoDB
Las colecciones, índices y registros iniciales se crean automáticamente con `database/01_mongo_init.js` al levantar el contenedor (`docker compose up -d`) y, si la base está vacía, al iniciar la API.

### Paso 4: Iniciar el servidor de la API REST
```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Acceso al servicio:
- **API URL Base:** `http://localhost:8000/api/v1`
- **Documentación Interactiva Swagger (OpenAPI):** `http://localhost:8000/docs`
- **Documentación ReDoc:** `http://localhost:8000/redoc`

---

## 7. Usuarios de Prueba Preconfigurados

Todos los usuarios tienen la contraseña: `Admin123*`

| Rol | Correo Electrónico | Contraseña |
|---|---|---|
| **ADMIN** | `juan.admin@gastronomia.sena.edu.co` | `Admin123*` |
| **CAJERO** | `maria.cajero@gastronomia.sena.edu.co` | `Admin123*` |
| **COCINERO** | `carlos.cocina@gastronomia.sena.edu.co` | `Admin123*` |

---

## 8. Pruebas con Postman

1. Abra **Postman**.
2. Haga clic en **Import** y seleccione el archivo `postman_collection.json`.
3. Ejecute la petición `01. Autenticación -> 1.1 Login Admin (Obtener Token)`.
4. Copie el `access_token` retornado y péguelo en la variable de colección `token`.
5. Ejecute cualquiera de las peticiones agrupadas en las 12 carpetas funcionales.
