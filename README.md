# Proyecto TechGear

Sistema web compuesto por una API REST en FastAPI y un Frontend en Django.

## ✨ Funcionalidades

- **Catálogo público**: lista de productos con imagen, precio y stock, con botón de compra directa.
- **Checkout**: formulario donde el cliente ingresa su nombre y cantidad; el pedido se crea automáticamente en la API (valida que no se pida más cantidad de la disponible en stock).
- **Panel de Administración** (`/panel/`):
  - Gestión de productos: crear, editar y eliminar, incluyendo carga de imagen.
  - Historial de pedidos realizados, con detalle de cada pedido.
- **Manejo de errores**: si la API de FastAPI no está disponible, el frontend muestra un mensaje en vez de romperse.

## 📁 Arquitectura del Proyecto

- `/techgear_api`: Backend desarrollado en FastAPI y MongoDB Atlas.
- `/techgear_web`: Frontend desarrollado en Django (patrón MVT).

---

## 🚀 Configuración e Instalación del Backend (`/techgear_api`)

### 1. Entrar al directorio del backend
```bash
cd techgear_api
```

### 2. Crear y activar un entorno virtual
```bash
python -m venv venv
venv\Scripts\activate       # En Windows
source venv/bin/activate    # En macOS/Linux
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crea un archivo `.env` dentro de `techgear_api/` con el siguiente contenido, reemplazando `<usuario>`, `<password>` y `<cluster>` por tus propias credenciales de MongoDB Atlas:

```env
MONGODB_URL=mongodb+srv://<usuario>:<password>@<cluster>.mongodb.net/?appName=Cluster0
```

> ⚠️ Este archivo `.env` nunca debe subirse a GitHub (ya está incluido en `.gitignore`).

### 5. Levantar el servidor
```bash
uvicorn main:app --reload
```

La API quedará disponible en: **http://127.0.0.1:8000/**
Documentación interactiva (Swagger UI): **http://127.0.0.1:8000/docs**

---

## 🖥️ Configuración e Instalación del Frontend (`/techgear_web`)

### 1. Entrar al directorio del frontend
```bash
cd techgear_web
```

### 2. Crear y activar un entorno virtual (independiente del backend)
```bash
python -m venv venv
venv\Scripts\activate       # En Windows
source venv/bin/activate    # En macOS/Linux
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones de Django
```bash
python manage.py migrate
```

### 5. Levantar el servidor
Como el backend ya ocupa el puerto **8000**, el frontend debe correrse en un puerto distinto, por ejemplo el **8001**:
```bash
python manage.py runserver 8001
```

El catálogo quedará disponible en: **http://127.0.0.1:8001/**

---

## ▶️ Cómo correr el proyecto completo

Se necesitan **dos terminales abiertas al mismo tiempo**:

| Terminal | Carpeta | Comando | URL |
|---|---|---|---|
| 1 | `techgear_api` | `uvicorn main:app --reload` | http://127.0.0.1:8000/ |
| 2 | `techgear_web` | `python manage.py runserver 8001` | http://127.0.0.1:8080/ |

Con ambos servidores corriendo, el catálogo en `http://127.0.0.1:8001/` consumirá en tiempo real los productos almacenados en MongoDB Atlas a través de la API.

---

## 🗂️ Estructura del repositorio

```text
TechGear_Project/
├── techgear_api/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── requirements.txt
│   └── .env           
├── techgear_web/
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/
│   ├── media/          
│   └── tienda/
│       ├── templates/tienda/
│       └── static/tienda/css
├── .gitignore
└── README.md
```