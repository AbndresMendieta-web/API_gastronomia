const dbName = "bd_gastronomia_nosql";
const dbTarget = db.getSiblingDB(dbName);

const colecciones = [
  "usuarios", "categorias", "productos", "insumos", "recetas",
  "proveedores", "clientes", "compras", "pedidos", "calificaciones"
];
colecciones.forEach(c => dbTarget[c].drop());

dbTarget.usuarios.createIndex({ correo: 1 }, { unique: true });
dbTarget.usuarios.createIndex({ identificacion: 1 }, { unique: true });
dbTarget.usuarios.createIndex({ id_usuario: 1 }, { unique: true });

dbTarget.categorias.createIndex({ nombre: 1 }, { unique: true });
dbTarget.categorias.createIndex({ id_categoria: 1 }, { unique: true });

dbTarget.productos.createIndex({ codigo: 1 }, { unique: true });
dbTarget.productos.createIndex({ id_producto: 1 }, { unique: true });

dbTarget.insumos.createIndex({ nombre: 1 }, { unique: true });
dbTarget.insumos.createIndex({ id_insumo: 1 }, { unique: true });

dbTarget.recetas.createIndex({ id_receta: 1 }, { unique: true });
dbTarget.recetas.createIndex({ id_producto: 1, id_insumo: 1 });

dbTarget.proveedores.createIndex({ nit: 1 }, { unique: true });
dbTarget.proveedores.createIndex({ id_proveedor: 1 }, { unique: true });

dbTarget.clientes.createIndex({ identificacion: 1 }, { unique: true });
dbTarget.clientes.createIndex({ id_cliente: 1 }, { unique: true });

dbTarget.compras.createIndex({ id_compra: 1 }, { unique: true });
dbTarget.pedidos.createIndex({ id_pedido: 1 }, { unique: true });

dbTarget.createCollection("calificaciones", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["id_pedido", "id_cliente", "fecha", "calificacion_servicio", "comentario", "productos"],
      properties: {
        id_pedido: { bsonType: "int" },
        id_cliente: { bsonType: "int" },
        fecha: { bsonType: "string" },
        calificacion_servicio: { bsonType: "int", minimum: 1, maximum: 5 },
        comentario: { bsonType: "string" },
        productos: {
          bsonType: "array",
          minItems: 1,
          items: {
            bsonType: "object",
            required: ["id_producto", "nombre", "calificacion"],
            properties: {
              id_producto: { bsonType: "int" },
              nombre: { bsonType: "string" },
              calificacion: { bsonType: "int", minimum: 1, maximum: 5 }
            }
          }
        }
      }
    }
  }
});

const PASS_HASH = "$2b$12$uVd/9GXppVuS1K/Na18cjOfxxVYRbuvKjh8nuGTMwo9303UOotrg6";

dbTarget.usuarios.insertMany([
  { id_usuario: 1, identificacion: "1075283941", nombres: "Juan Andres", apellidos: "MEndieta Palomino", correo: "juan.admin@gastronomia.sena.edu.co", password: PASS_HASH, rol: "ADMIN", estado: "ACTIVO" },
  { id_usuario: 2, identificacion: "1082491823", nombres: "María Alejandra", apellidos: "Gómez Castro", correo: "maria.cajero@gastronomia.sena.edu.co", password: PASS_HASH, rol: "CAJERO", estado: "ACTIVO" },
  { id_usuario: 3, identificacion: "1075981234", nombres: "Carlos Eduardo", apellidos: "López Vega", correo: "carlos.cocina@gastronomia.sena.edu.co", password: PASS_HASH, rol: "COCINERO", estado: "ACTIVO" },
  { id_usuario: 4, identificacion: "1076112233", nombres: "Laura Sofía", apellidos: "Ramírez Vargas", correo: "laura.admin2@gastronomia.sena.edu.co", password: PASS_HASH, rol: "ADMIN", estado: "ACTIVO" },
  { id_usuario: 5, identificacion: "1080334455", nombres: "Diego Fernando", apellidos: "Ortiz Morales", correo: "diego.cajero2@gastronomia.sena.edu.co", password: PASS_HASH, rol: "CAJERO", estado: "ACTIVO" },
  { id_usuario: 6, identificacion: "1077556677", nombres: "Ana Patricia", apellidos: "Mendoza Silva", correo: "ana.cocina2@gastronomia.sena.edu.co", password: PASS_HASH, rol: "COCINERO", estado: "ACTIVO" },
  { id_usuario: 7, identificacion: "1081778899", nombres: "Andrés Felipe", apellidos: "Torres Mora", correo: "andres.cajero3@gastronomia.sena.edu.co", password: PASS_HASH, rol: "CAJERO", estado: "ACTIVO" },
  { id_usuario: 8, identificacion: "1079990011", nombres: "Paola Andrea", apellidos: "Suárez Díaz", correo: "paola.cocina3@gastronomia.sena.edu.co", password: PASS_HASH, rol: "COCINERO", estado: "ACTIVO" },
  { id_usuario: 9, identificacion: "1083223344", nombres: "Julián David", apellidos: "Cabrera Ruiz", correo: "julian.admin3@gastronomia.sena.edu.co", password: PASS_HASH, rol: "ADMIN", estado: "ACTIVO" },
  { id_usuario: 10, identificacion: "1074445566", nombres: "Mónica Liceth", apellidos: "Perdomo Cruz", correo: "monica.inactivo@gastronomia.sena.edu.co", password: PASS_HASH, rol: "CAJERO", estado: "INACTIVO" }
]);

dbTarget.categorias.insertMany([
  { id_categoria: 1, nombre: "Platos Fuertes", descripcion: "Almuerzos y platos principales preparados al día", estado: "ACTIVO" },
  { id_categoria: 2, nombre: "Bebidas Frías", descripcion: "Jugos naturales, gaseosas y bebidas refrescantes", estado: "ACTIVO" },
  { id_categoria: 3, nombre: "Bebidas Calientes", descripcion: "Café especial, infusiones y chocolate caliente", estado: "ACTIVO" },
  { id_categoria: 4, nombre: "Panadería", descripcion: "Panes artesanales y tradicionales elaborados en el taller", estado: "ACTIVO" },
  { id_categoria: 5, nombre: "Repostería", descripcion: "Tortas, pasteles, brownies y postres de la casa", estado: "ACTIVO" },
  { id_categoria: 6, nombre: "Desayunos", descripcion: "Combos de desayuno campesino, americano y ligero", estado: "ACTIVO" },
  { id_categoria: 7, nombre: "Comidas Rápidas", descripcion: "Hamburguesas, sanduches y porciones rápidas", estado: "ACTIVO" },
  { id_categoria: 8, nombre: "Ensaladas", descripcion: "Ensaladas saludables y guarniciones frescas", estado: "ACTIVO" },
  { id_categoria: 9, nombre: "Sopas y Cremas", descripcion: "Sancocho, ajiaco y cremas del día", estado: "ACTIVO" },
  { id_categoria: 10, nombre: "Snacks y Pasabocas", descripcion: "Empanadas, buñuelos y refrigerios para eventos", estado: "ACTIVO" }
]);

dbTarget.productos.insertMany([
  { id_producto: 1, codigo: "PLT-001", nombre: "Almuerzo Ejecutivo Especial", descripcion: "Sopa, plato fuerte con proteína, arroz, ensalada y jugo", precio_venta: 14000.0, unidad_venta: "Porción", id_categoria: 1, estado: "DISPONIBLE" },
  { id_producto: 2, codigo: "PLT-002", nombre: "Bandeja Campesina Huilense", descripcion: "Carne asada, frijol, plátano maduro, huevo, arroz y arepa", precio_venta: 18000.0, unidad_venta: "Porción", id_categoria: 1, estado: "DISPONIBLE" },
  { id_producto: 3, codigo: "BEB-001", nombre: "Jugo Natural de Lulo", descripcion: "Jugo natural preparado en agua o leche", precio_venta: 4500.0, unidad_venta: "Vaso 12oz", id_categoria: 2, estado: "DISPONIBLE" },
  { id_producto: 4, codigo: "BEB-002", nombre: "Limonada de Coco", descripcion: "Limonada frapeada con leche de coco y azúcar orgánica", precio_venta: 6000.0, unidad_venta: "Vaso 14oz", id_categoria: 2, estado: "DISPONIBLE" },
  { id_producto: 5, codigo: "CAF-001", nombre: "Café Especial Americano", descripcion: "Café filtrado cultivado en fincas del Huila", precio_venta: 3500.0, unidad_venta: "Taza 8oz", id_categoria: 3, estado: "DISPONIBLE" },
  { id_producto: 6, codigo: "PAN-001", nombre: "Croissant de Mantequilla", descripcion: "Croissant hojaldrado horneado diariamente", precio_venta: 4000.0, unidad_venta: "Unidad", id_categoria: 4, estado: "DISPONIBLE" },
  { id_producto: 7, codigo: "REP-001", nombre: "Porción de Torta de Chocolate", descripcion: "Bizcocho húmedo de cacao al 70% relleno de arequipe", precio_venta: 6500.0, unidad_venta: "Porción", id_categoria: 5, estado: "DISPONIBLE" },
  { id_producto: 8, codigo: "DES-001", nombre: "Desayuno Tradicional con Huevos", descripcion: "Huevos al gusto, arepa con queso, chocolate o café", precio_venta: 9000.0, unidad_venta: "Porción", id_categoria: 6, estado: "DISPONIBLE" },
  { id_producto: 9, codigo: "RAP-001", nombre: "Hamburguesa Artesanal de Res", descripcion: "Carne de res 150g, queso holandés, tocineta y verduras", precio_venta: 16000.0, unidad_venta: "Unidad", id_categoria: 7, estado: "DISPONIBLE" },
  { id_producto: 10, codigo: "SNA-001", nombre: "Empanada de Carne y Papa", descripcion: "Empanada frita crocante con ají casero", precio_venta: 2500.0, unidad_venta: "Unidad", id_categoria: 10, estado: "DISPONIBLE" }
]);

dbTarget.insumos.insertMany([
  { id_insumo: 1, nombre: "Carne de Res Pulpa Molida", unidad_medida: "kg", stock_actual: 25.5, stock_minimo: 5.0, costo_unitario: 24000.0, fecha_vencimiento: "2026-11-15", estado: "ACTIVO" },
  { id_insumo: 2, nombre: "Pechuga de Pollo Fresca", unidad_medida: "kg", stock_actual: 30.0, stock_minimo: 6.0, costo_unitario: 18000.0, fecha_vencimiento: "2026-11-10", estado: "ACTIVO" },
  { id_insumo: 3, nombre: "Arroz Blanco Supremo", unidad_medida: "kg", stock_actual: 50.0, stock_minimo: 10.0, costo_unitario: 4200.0, fecha_vencimiento: "2027-02-28", estado: "ACTIVO" },
  { id_insumo: 4, nombre: "Aceite Vegetal de Girasol", unidad_medida: "l", stock_actual: 15.0, stock_minimo: 4.0, costo_unitario: 11500.0, fecha_vencimiento: "2027-04-30", estado: "ACTIVO" },
  { id_insumo: 5, nombre: "Pulpa de Lulo Congelada", unidad_medida: "kg", stock_actual: 12.0, stock_minimo: 3.0, costo_unitario: 9000.0, fecha_vencimiento: "2026-12-01", estado: "ACTIVO" },
  { id_insumo: 6, nombre: "Leche Entera Pasteurizada", unidad_medida: "l", stock_actual: 20.0, stock_minimo: 8.0, costo_unitario: 4200.0, fecha_vencimiento: "2026-10-25", estado: "ACTIVO" },
  { id_insumo: 7, nombre: "Café Tostado y Molido Especial", unidad_medida: "kg", stock_actual: 8.0, stock_minimo: 2.0, costo_unitario: 32000.0, fecha_vencimiento: "2027-06-30", estado: "ACTIVO" },
  { id_insumo: 8, nombre: "Harina de Trigo Fortificada", unidad_medida: "kg", stock_actual: 40.0, stock_minimo: 10.0, costo_unitario: 3800.0, fecha_vencimiento: "2027-01-15", estado: "ACTIVO" },
  { id_insumo: 9, nombre: "Mantequilla Pura sin Sal", unidad_medida: "kg", stock_actual: 10.0, stock_minimo: 2.5, costo_unitario: 26000.0, fecha_vencimiento: "2026-12-15", estado: "ACTIVO" },
  { id_insumo: 10, nombre: "Huevos Rojos Tipo AA", unidad_medida: "unidad", stock_actual: 180.0, stock_minimo: 30.0, costo_unitario: 600.0, fecha_vencimiento: "2026-11-05", estado: "ACTIVO" }
]);

dbTarget.recetas.insertMany([
  { id_receta: 1, id_producto: 1, id_insumo: 2, cantidad: 0.200 },
  { id_receta: 2, id_producto: 1, id_insumo: 3, cantidad: 0.100 },
  { id_receta: 3, id_producto: 1, id_insumo: 4, cantidad: 0.020 },
  { id_receta: 4, id_producto: 3, id_insumo: 5, cantidad: 0.100 },
  { id_receta: 5, id_producto: 5, id_insumo: 7, cantidad: 0.015 },
  { id_receta: 6, id_producto: 6, id_insumo: 8, cantidad: 0.080 },
  { id_receta: 7, id_producto: 6, id_insumo: 9, cantidad: 0.035 },
  { id_receta: 8, id_producto: 8, id_insumo: 10, cantidad: 2.0 },
  { id_receta: 9, id_producto: 8, id_insumo: 9, cantidad: 0.015 },
  { id_receta: 10, id_producto: 9, id_insumo: 1, cantidad: 0.180 },
  { id_receta: 11, id_producto: 9, id_insumo: 8, cantidad: 0.060 },
  { id_receta: 12, id_producto: 10, id_insumo: 1, cantidad: 0.040 },
  { id_receta: 13, id_producto: 10, id_insumo: 8, cantidad: 0.050 }
]);

dbTarget.proveedores.insertMany([
  { id_proveedor: 1, nit: "900123456-1", razon_social: "Distribuidora Avícola y Carnes del Huila S.A.S", telefono: "3101234567", correo: "ventas@avicolahuila.com", direccion: "Calle 10 # 5-20, Garzón", estado: "ACTIVO" },
  { id_proveedor: 2, nit: "900234567-2", razon_social: "Molinos y Granos del Surcolombiano Ltda", telefono: "3202345678", correo: "pedidos@granosdelsur.com", direccion: "Carrera 8 # 12-40, Neiva", estado: "ACTIVO" },
  { id_proveedor: 3, nit: "900345678-3", razon_social: "Lácteos La Pradera S.A.", telefono: "3153456789", correo: "contacto@lacteospradera.com", direccion: "Vereda El Recreo Km 3, Gigante", estado: "ACTIVO" },
  { id_proveedor: 4, nit: "900456789-4", razon_social: "Frutas y Pulpas del Valle del Huila", telefono: "3114567890", correo: "distribucion@frutasvalle.com", direccion: "Plaza Mayorista Bodega 4, Neiva", estado: "ACTIVO" },
  { id_proveedor: 5, nit: "900567890-5", razon_social: "Café y Derivados Macizo Colombiano", telefono: "3145678901", correo: "comercial@cafemacizo.com", direccion: "Carrera 5 # 3-12, Pitalito", estado: "ACTIVO" },
  { id_proveedor: 6, nit: "900678901-6", razon_social: "Panadería y Molinería Industrial S.A.S", telefono: "3126789012", correo: "ventas@panaderiaindustrial.com", direccion: "Calle 15 # 9-80, Garzón", estado: "ACTIVO" },
  { id_proveedor: 7, nit: "900789012-7", razon_social: "Grasas y Aceites Naturales del Huila", telefono: "3187890123", correo: "pedidos@aceiteshuila.com", direccion: "Zona Industrial Manzana B, Neiva", estado: "ACTIVO" },
  { id_proveedor: 8, nit: "900890123-8", razon_social: "Huevos y Aves San Jerónimo", telefono: "3178901234", correo: "info@avessanjeronimo.com", direccion: "Finca San Jerónimo, Garzón", estado: "ACTIVO" },
  { id_proveedor: 9, nit: "900901234-9", razon_social: "Empaques y Desechables Ecológicos Sur", telefono: "3219012345", correo: "ventas@empaquessur.com", direccion: "Calle 7 # 11-30, Garzón", estado: "ACTIVO" },
  { id_proveedor: 10, nit: "900012345-0", razon_social: "Comercializadora Agropecuaria El Samán", telefono: "3160123456", correo: "elsaman@comercializadora.com", direccion: "Carrera 12 # 4-50, Garzón", estado: "INACTIVO" }
]);

dbTarget.clientes.insertMany([
  { id_cliente: 1, identificacion: "1085234111", nombres: "Brayan Steven", apellidos: "Pinto Lozano", telefono: "3112223344", correo: "brayan.pinto@soy.sena.edu.co", tipo_cliente: "APRENDIZ", estado: "ACTIVO" },
  { id_cliente: 2, identificacion: "1087345222", nombres: "Daniela", apellidos: "Castro Vargas", telefono: "3123334455", correo: "daniela.castro@soy.sena.edu.co", tipo_cliente: "APRENDIZ", estado: "ACTIVO" },
  { id_cliente: 3, identificacion: "1075678333", nombres: "Ing. Gabriel", apellidos: "Morales Medina", telefono: "3154445566", correo: "gabriel.morales@sena.edu.co", tipo_cliente: "INSTRUCTOR", estado: "ACTIVO" },
  { id_cliente: 4, identificacion: "1074890444", nombres: "Dra. Patricia", apellidos: "Ospina Ramos", telefono: "3165556677", correo: "patricia.ospina@sena.edu.co", tipo_cliente: "INSTRUCTOR", estado: "ACTIVO" },
  { id_cliente: 5, identificacion: "1081123555", nombres: "Nelson Enrique", apellidos: "Vargas Murcia", telefono: "3176667788", correo: "nelson.vargas@sena.edu.co", tipo_cliente: "FUNCIONARIO", estado: "ACTIVO" },
  { id_cliente: 6, identificacion: "1083456666", nombres: "Luz Marina", apellidos: "Salazar Cruz", telefono: "3187778899", correo: "luz.salazar@sena.edu.co", tipo_cliente: "FUNCIONARIO", estado: "ACTIVO" },
  { id_cliente: 7, identificacion: "1079234777", nombres: "Fabio Alberto", apellidos: "Gutiérrez Peña", telefono: "3198889900", correo: "fabio.gutierrez@gmail.com", tipo_cliente: "EXTERNO", estado: "ACTIVO" },
  { id_cliente: 8, identificacion: "1082567888", nombres: "Claudia Marcela", apellidos: "Chávarro Polo", telefono: "3109990011", correo: "claudia.chavarro@hotmail.com", tipo_cliente: "EXTERNO", estado: "ACTIVO" },
  { id_cliente: 9, identificacion: "1077890999", nombres: "Kevin Alexander", apellidos: "Ibarra Perdomo", telefono: "3131112233", correo: "kevin.ibarra@soy.sena.edu.co", tipo_cliente: "APRENDIZ", estado: "ACTIVO" },
  { id_cliente: 10, identificacion: "1076012000", nombres: "Martha Cecilia", apellidos: "Trujillo Ortiz", telefono: "3142223355", correo: "martha.trujillo@gmail.com", tipo_cliente: "EXTERNO", estado: "INACTIVO" }
]);

dbTarget.compras.insertMany([
  { id_compra: 1, numero_factura: "FAC-00101", fecha_compra: new Date("2026-10-01T08:30:00Z"), id_proveedor: 1, id_usuario: 1, total: 480000.0, detalles: [{ id_detalle_compra: 1, id_insumo: 1, cantidad: 20.0, costo_unitario: 24000.0, subtotal: 480000.0 }] },
  { id_compra: 2, numero_factura: "FAC-00102", fecha_compra: new Date("2026-10-02T09:15:00Z"), id_proveedor: 2, id_usuario: 1, total: 210000.0, detalles: [{ id_detalle_compra: 1, id_insumo: 3, cantidad: 50.0, costo_unitario: 4200.0, subtotal: 210000.0 }] },
  { id_compra: 3, numero_factura: "FAC-00103", fecha_compra: new Date("2026-10-03T10:00:00Z"), id_proveedor: 3, id_usuario: 1, total: 126000.0, detalles: [{ id_detalle_compra: 1, id_insumo: 6, cantidad: 30.0, costo_unitario: 4200.0, subtotal: 126000.0 }] },
  { id_compra: 4, numero_factura: "FAC-00104", fecha_compra: new Date("2026-10-05T11:20:00Z"), id_proveedor: 4, id_usuario: 1, total: 90000.0, detalles: [{ id_detalle_compra: 1, id_insumo: 5, cantidad: 10.0, costo_unitario: 9000.0, subtotal: 90000.0 }] },
  { id_compra: 5, numero_factura: "FAC-00105", fecha_compra: new Date("2026-10-06T08:45:00Z"), id_proveedor: 5, id_usuario: 1, total: 160000.0, detalles: [{ id_detalle_compra: 1, id_insumo: 7, cantidad: 5.0, costo_unitario: 32000.0, subtotal: 160000.0 }] },
  { id_compra: 6, numero_factura: "FAC-00106", fecha_compra: new Date("2026-10-08T14:10:00Z"), id_proveedor: 6, id_usuario: 1, total: 152000.0, detalles: [{ id_detalle_compra: 1, id_insumo: 8, cantidad: 40.0, costo_unitario: 3800.0, subtotal: 152000.0 }] },
  { id_compra: 7, numero_factura: "FAC-00107", fecha_compra: new Date("2026-10-09T15:30:00Z"), id_proveedor: 7, id_usuario: 1, total: 115000.0, detalles: [{ id_detalle_compra: 1, id_insumo: 4, cantidad: 10.0, costo_unitario: 11500.0, subtotal: 115000.0 }] },
  { id_compra: 8, numero_factura: "FAC-00108", fecha_compra: new Date("2026-10-10T16:00:00Z"), id_proveedor: 8, id_usuario: 1, total: 108000.0, detalles: [{ id_detalle_compra: 1, id_insumo: 10, cantidad: 180.0, costo_unitario: 600.0, subtotal: 108000.0 }] },
  { id_compra: 9, numero_factura: "FAC-00109", fecha_compra: new Date("2026-10-12T09:30:00Z"), id_proveedor: 1, id_usuario: 1, total: 360000.0, detalles: [{ id_detalle_compra: 1, id_insumo: 2, cantidad: 20.0, costo_unitario: 18000.0, subtotal: 360000.0 }] },
  { id_compra: 10, numero_factura: "FAC-00110", fecha_compra: new Date("2026-10-14T10:15:00Z"), id_proveedor: 3, id_usuario: 1, total: 84000.0, detalles: [{ id_detalle_compra: 1, id_insumo: 9, cantidad: 3.23, costo_unitario: 26000.0, subtotal: 84000.0 }] }
]);

dbTarget.pedidos.insertMany([
  { id_pedido: 1, fecha_pedido: new Date("2026-10-10T12:15:00Z"), id_cliente: 1, id_usuario: 2, tipo_pedido: "MESA", estado: "ENTREGADO", total: 18500.0, observaciones: "Mesa 3 - Sin cebolla", items: [{ id_detalle: 1, id_producto: 1, cantidad: 1.0, precio_unitario: 14000.0, subtotal: 14000.0 }, { id_detalle: 2, id_producto: 3, cantidad: 1.0, precio_unitario: 4500.0, subtotal: 4500.0 }] },
  { id_pedido: 2, fecha_pedido: new Date("2026-10-11T12:30:00Z"), id_cliente: 2, id_usuario: 2, tipo_pedido: "PARA_LLEVAR", estado: "ENTREGADO", total: 20500.0, observaciones: "Empacado individual", items: [{ id_detalle: 1, id_producto: 9, cantidad: 1.0, precio_unitario: 16000.0, subtotal: 16000.0 }, { id_detalle: 2, id_producto: 3, cantidad: 1.0, precio_unitario: 4500.0, subtotal: 4500.0 }] },
  { id_pedido: 3, fecha_pedido: new Date("2026-10-12T12:45:00Z"), id_cliente: 3, id_usuario: 2, tipo_pedido: "MESA", estado: "ENTREGADO", total: 28000.0, observaciones: "Mesa 1", items: [{ id_detalle: 1, id_producto: 1, cantidad: 2.0, precio_unitario: 14000.0, subtotal: 28000.0 }] },
  { id_pedido: 4, fecha_pedido: new Date("2026-10-13T13:00:00Z"), id_cliente: 4, id_usuario: 2, tipo_pedido: "MESA", estado: "ENTREGADO", total: 14000.0, observaciones: "Mesa 5", items: [{ id_detalle: 1, id_producto: 1, cantidad: 1.0, precio_unitario: 14000.0, subtotal: 14000.0 }] },
  { id_pedido: 5, fecha_pedido: new Date("2026-10-14T07:45:00Z"), id_cliente: 5, id_usuario: 2, tipo_pedido: "MESA", estado: "ENTREGADO", total: 12500.0, observaciones: "Desayuno mesa 2", items: [{ id_detalle: 1, id_producto: 8, cantidad: 1.0, precio_unitario: 9000.0, subtotal: 9000.0 }, { id_detalle: 2, id_producto: 5, cantidad: 1.0, precio_unitario: 3500.0, subtotal: 3500.0 }] },
  { id_pedido: 6, fecha_pedido: new Date("2026-10-14T12:10:00Z"), id_cliente: 6, id_usuario: 2, tipo_pedido: "PARA_LLEVAR", estado: "ENTREGADO", total: 18500.0, observaciones: "Almuerzo con jugo", items: [{ id_detalle: 1, id_producto: 1, cantidad: 1.0, precio_unitario: 14000.0, subtotal: 14000.0 }, { id_detalle: 2, id_producto: 3, cantidad: 1.0, precio_unitario: 4500.0, subtotal: 4500.0 }] },
  { id_pedido: 7, fecha_pedido: new Date("2026-10-15T12:20:00Z"), id_cliente: 7, id_usuario: 2, tipo_pedido: "MESA", estado: "EN_PREPARACION", total: 32000.0, observaciones: "Mesa 6", items: [{ id_detalle: 1, id_producto: 9, cantidad: 2.0, precio_unitario: 16000.0, subtotal: 32000.0 }] },
  { id_pedido: 8, fecha_pedido: new Date("2026-10-15T13:10:00Z"), id_cliente: 8, id_usuario: 2, tipo_pedido: "MESA", estado: "PENDIENTE", total: 16000.0, observaciones: "Mesa 4", items: [{ id_detalle: 1, id_producto: 9, cantidad: 1.0, precio_unitario: 16000.0, subtotal: 16000.0 }] },
  { id_pedido: 9, fecha_pedido: new Date("2026-10-15T14:00:00Z"), id_cliente: 9, id_usuario: 2, tipo_pedido: "PARA_LLEVAR", estado: "ANULADO", total: 14000.0, observaciones: "Cliente canceló", items: [{ id_detalle: 1, id_producto: 1, cantidad: 1.0, precio_unitario: 14000.0, subtotal: 14000.0 }] },
  { id_pedido: 10, fecha_pedido: new Date("2026-10-16T08:30:00Z"), id_cliente: 1, id_usuario: 2, tipo_pedido: "MESA", estado: "PENDIENTE", total: 9000.0, observaciones: "Desayuno", items: [{ id_detalle: 1, id_producto: 8, cantidad: 1.0, precio_unitario: 9000.0, subtotal: 9000.0 }] }
]);

dbTarget.calificaciones.insertMany([
  {
    id_pedido: 1,
    id_cliente: 1,
    fecha: "2026-10-10T12:45:00",
    calificacion_servicio: 5,
    comentario: "Excelente sazón y atención muy rápida en la mesa.",
    productos: [
      { id_producto: 1, nombre: "Almuerzo Ejecutivo Especial", calificacion: 5 },
      { id_producto: 3, nombre: "Jugo Natural de Lulo", calificacion: 5 }
    ]
  },
  {
    id_pedido: 2,
    id_cliente: 2,
    fecha: "2026-10-11T13:00:00",
    calificacion_servicio: 4,
    comentario: "Muy buen empaque para llevar, la hamburguesa llegó caliente.",
    productos: [
      { id_producto: 9, nombre: "Hamburguesa Artesanal de Res", calificacion: 4 },
      { id_producto: 3, nombre: "Jugo Natural de Lulo", calificacion: 5 }
    ]
  },
  {
    id_pedido: 3,
    id_cliente: 3,
    fecha: "2026-10-12T13:20:00",
    calificacion_servicio: 5,
    comentario: "El almuerzo campesino estuvo insuperable, porciones generosas.",
    productos: [
      { id_producto: 1, nombre: "Almuerzo Ejecutivo Especial", calificacion: 5 }
    ]
  },
  {
    id_pedido: 4,
    id_cliente: 4,
    fecha: "2026-10-13T13:30:00",
    calificacion_servicio: 4,
    comentario: "Buena presentación y sabor balanceado.",
    productos: [
      { id_producto: 1, nombre: "Almuerzo Ejecutivo Especial", calificacion: 4 }
    ]
  },
  {
    id_pedido: 5,
    id_cliente: 5,
    fecha: "2026-10-14T08:15:00",
    calificacion_servicio: 5,
    comentario: "El café huilense tiene un aroma delicioso y los huevos estaban en su punto.",
    productos: [
      { id_producto: 8, nombre: "Desayuno Tradicional con Huevos", calificacion: 5 },
      { id_producto: 5, nombre: "Café Especial Americano", calificacion: 5 }
    ]
  },
  {
    id_pedido: 6,
    id_cliente: 6,
    fecha: "2026-10-14T12:40:00",
    calificacion_servicio: 5,
    comentario: "Excelente relación calidad precio. Muy recomendado.",
    productos: [
      { id_producto: 1, nombre: "Almuerzo Ejecutivo Especial", calificacion: 5 },
      { id_producto: 3, nombre: "Jugo Natural de Lulo", calificacion: 4 }
    ]
  }
]);

print("¡Base de datos MongoDB 'bd_gastronomia_nosql' inicializada con 10 colecciones completas!");
