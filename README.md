# Sistema Kardex Pro - Gestión de Inventarios

Aplicación de escritorio moderna y robusta para la administración y control de inventarios (**Kardex**), desarrollada bajo el patrón arquitectónico **MVC (Modelo-Vista-Controlador)** en **Python**, con interfaz gráfica moderna en **CustomTkinter**, base de datos relacional en **Microsoft SQL Server** y generación de reportes oficiales en **PDF** con **ReportLab**.

---

## 📌 Características Principales

- **Dashboard Ejecutivo Interactivo:**
  - Tarjetas de indicadores clave (KPIs) en tiempo real: *Total de Productos*, *Bodegas Activas*, *Productos en Alerta* y *Movimientos de Hoy*.
  - Las flechas y tarjetas abren ventanas interactivas de detalle con tablas filtrables.
  - Gráfica dinámica de barras que muestra las entradas y salidas de los **últimos 7 días**.
  - Indicadores tipo Donut y Semáforo de estado de inventario (*Óptimo*, *Stock Bajo*, *Agotado*).

- **Generador de Reportes en PDF (Exclusivo Administrador):**
  - Motor de reportes formales construido con **ReportLab**.
  - Exportación de 5 tipos de reportes institucionales:
    1. *Catálogo General de Productos* (con costos, categorías y stock mínimo).
    2. *Directorio e Inventario por Bodegas* (con existencias acumuladas por sucursal).
    3. *Reporte de Alertas Críticas de Stock* (productos agotados o bajo stock mínimo).
    4. *Bitácora de Movimientos del Día* (entradas, salidas y ajustes de hoy).
    5. *Reporte Consolidado de Movimientos de los Últimos 7 Días* (análisis de entradas vs. salidas).
  - Diálogo para elegir la ubicación del archivo y apertura automática al finalizar.
  - Los botones de exportación a PDF están **restringidos exclusivamente al rol de Administrador**.

- **Flujo de Autorización de Ajustes de Inventario:**
  - Los encargados de bodega pueden solicitar **Ajustes Positivos (+)** o **Ajustes Negativos (-)** justificando con un motivo de excepción.
  - El movimiento se registra con estado **`EN REVISION`** y **no afecta el stock físico** en bodega de manera preliminar.
  - El Administrador cuenta con un panel exclusivo en *Administración* $\rightarrow$ *Aprobar Ajustes* para revisar las solicitudes y **Aprobar** (aplica el cambio al inventario en una transacción segura) o **Rechazar**.

- **Control de Inventario y Kardex (Semáforos):**
  - Tabla de consulta de inventario con paginación, filtros por bodega y estado, y búsqueda en tiempo real.
  - Bloqueo matemático de stock negativo para prevenir descuadres de existencias.

- **Diseño Moderno y Accesible:**
  - Soporte nativo para modo **Oscuro (Dark)** y modo **Claro (Light)** con cambio en caliente.
  - Iconografía vectorial limpia y diseño visual coherente.

---

## 🏗️ Estructura del Proyecto (MVC)

```text
Sistema Kardex/
├── controllers/                  # Lógica de Negocio y Controladores
│   ├── admin_ctrl.py             # CRUD de usuarios, catálogo y autorización de ajustes
│   ├── auth_ctrl.py              # Autenticación y roles de usuario
│   ├── kardex_ctrl.py            # Matemáticas de inventario, stock y movimientos
│   └── reportes_ctrl.py          # Motor de generación de reportes en PDF (ReportLab)
├── models/                       # Capa de Datos (ORM SQLAlchemy)
│   ├── database.py               # Configuración de conexión a SQL Server (pyodbc)
│   └── entities.py               # Modelos: Usuarios, Roles, Productos, Bodegas, Movimientos
├── views/                        # Capa de Presentación (CustomTkinter)
│   ├── components/
│   │   ├── dashboard_home.py     # Vista principal del Dashboard (KPIs, gráfica, modales)
│   │   └── kardex_table.py       # Tabla paginada de inventario y semáforos
│   ├── forms/
│   │   ├── admin_view.py         # Panel de gestión de usuarios, productos y aprobación de ajustes
│   │   └── movimiento_view.py    # Formulario de registro de movimientos y solicitudes de ajuste
│   ├── main_dashboard.py         # Contenedor principal con barra lateral y navegación por roles
│   └── ui_theme.py               # Tokens de diseño, paleta claro/oscuro y componentes visuales
├── main.py                       # Punto de entrada de la aplicación (Ventana de Login)
├── seed_data.sql                 # Script de inicialización de datos para SQL Server
├── requirements.txt              # Dependencias de Python
├── run.bat                       # Script ejecutable directo para Windows
└── .gitignore                    # Archivos y carpetas excluidos del control de versiones
```

---

## ⚙️ Requisitos Previos

1. **Python 3.10 o superior** instalado en el sistema.
2. **Microsoft SQL Server** (Express, Developer o Standard) ejecutándose localmente.
3. **ODBC Driver 17 for SQL Server** (o versión 18) instalado en Windows.

---

## 🚀 Guía de Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd "Sistema Kardex"
```

### 2. Crear y Activar el Entorno Virtual
En la consola de Windows (PowerShell o CMD):
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3. Instalar las Dependencias
Con el entorno virtual activado, ejecuta:
```bash
pip install -r requirements.txt
```

Las dependencias principales son:
- `customtkinter`: Interfaz gráfica moderna de escritorio.
- `SQLAlchemy`: ORM para mapeo objeto-relacional y transacciones seguras.
- `pyodbc`: Conector ODBC para SQL Server.
- `reportlab`: Generador de documentos PDF profesionales.
- `pandas`: Procesamiento y análisis de datos.

### 4. Configurar la Base de Datos en SQL Server

1. Abre **SQL Server Management Studio (SSMS)** o Azure Data Studio.
2. Crea una base de datos llamada `SISTEMA_KARDEX` (o ejecuta el script inicial).
3. Abre y ejecuta el archivo [`seed_data.sql`](file:///c:/Desarrollo%20Fernando/Sistema%20Kardex/seed_data.sql) para crear las tablas de catálogo, bodegas, tipos de movimientos y usuarios iniciales.
4. Si tu instancia de SQL Server tiene un nombre especial (por ejemplo `localhost\SQLEXPRESS`), configúralo en [`models/database.py`](file:///c:/Desarrollo%20Fernando/Sistema%20Kardex/models/database.py):

```python
SERVER = 'localhost' # o 'localhost\\SQLEXPRESS'
DATABASE = 'SISTEMA_KARDEX'
```

---

## 💻 Ejecución del Sistema

### Opción 1: Archivo Ejecutable (Recomendado en Windows)
Simplemente haz doble clic en el archivo [`run.bat`](file:///c:/Desarrollo%20Fernando/Sistema%20Kardex/run.bat) en la raíz del proyecto.

### Opción 2: Desde Terminal
```powershell
.\venv\Scripts\activate
python main.py
```

---

## 👥 Roles y Credenciales de Prueba

El sistema incluye usuarios preconfigurados en `seed_data.sql` para validar los diferentes niveles de acceso:

| Rol | Correo Electrónico | Contraseña | Permisos y Alcance |
| :--- | :--- | :--- | :--- |
| **Administrador** | `fernando@gmail.com` | `admin123` | Control total: Dashboard, inventario, registro de movimientos, gestión de usuarios, catálogo, **aprobación/rechazo de ajustes** y **exportación de todos los reportes PDF**. |
| **Encargado de Bodega** | `fernando2@gmail.com` | `bodega123` | Consulta de inventario, registro de entradas/salidas y **envío de solicitudes de ajuste** (quedan en revisión). Sin exportación PDF de reportes ejecutivos. |
| **Consulta / Supervisión** | `consultas@gmail.com` | `consulta123` | Solo lectura: Consulta de inventario y semáforos. Sin acciones de guardar ni exportaciones administrativas. |

---

## 📄 Licencia y Confidencialidad
Proyecto desarrollado para gestión y control integral de inventarios bajo el esquema Kardex. Uso académico y empresarial autorizado.
