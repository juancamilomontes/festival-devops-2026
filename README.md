# 🎵 Pacific DevOps Music Fest — Actividad #5

**Programa:** DevOps y Contenedores (Docker) — SENA CTMA  
**Semana:** 05 — Docker Compose  
**Instructor:** Efrén Moreno Valoyes  

---

## 📋 Descripción

Landing page profesional para el festival **Pacific DevOps Music Fest 2026**, desplegada con un entorno multi-contenedor usando Docker Compose. El proyecto integra frontend, backend API y base de datos en una arquitectura completamente dockerizada.

---

## 🏗️ Arquitectura del proyecto

```
festival-devops/
├── frontend/
│   ├── index.html       → Landing page del festival
│   ├── style.css        → Estilos personalizados
│   └── Dockerfile       → Imagen basada en Nginx:alpine
│
├── backend/
│   ├── app.py           → API REST con Flask
│   ├── requirements.txt → Dependencias Python
│   └── Dockerfile       → Imagen basada en Python:3.11-slim
│
├── database/            → Carpeta reservada para scripts SQL
├── .env                 → Variables de entorno (no se sube a GitHub)
├── .gitignore
└── docker-compose.yml   → Orquestación de los 3 servicios
```

---

## 🐳 Servicios Docker

| Servicio   | Imagen base       | Puerto | Descripción                        |
|------------|-------------------|--------|------------------------------------|
| `frontend` | nginx:alpine      | 8080   | Sirve la landing page del festival |
| `backend`  | python:3.11-slim  | 5000   | API REST Flask con endpoints JSON  |
| `db`       | mysql:8.0         | 3306   | Base de datos persistente MySQL    |

---

## 🔗 Comunicación entre servicios

Los tres servicios se comunican dentro de la red personalizada `festival-network` de tipo `bridge`:

- El **frontend** hace una petición al **backend** en `http://localhost:5000/api/concierto` para mostrar la info del concierto en tiempo real.
- El **backend** se conecta a la **base de datos** usando el hostname `db` (nombre del servicio en Docker Compose), por el puerto 3306.
- La **base de datos** persiste sus datos en el volumen `festival-db-data`, así aunque el contenedor se reinicie los datos no se pierden.

---

## 🌐 Endpoints de la API

| Método | Endpoint          | Descripción                        |
|--------|-------------------|------------------------------------|
| GET    | `/api/concierto`  | Info general del festival desde DB |
| GET    | `/api/artistas`   | Lista de artistas del festival     |
| GET    | `/health`         | Estado del servicio backend        |

---

## ✅ Variables de entorno

Definidas en el archivo `.env` (no incluido en el repositorio):

```
DB_NAME=festival_db
DB_USER=festival_user
DB_PASSWORD=festival_pass
MYSQL_ROOT_PASSWORD=root_secret_2026
```

---

## 🚀 Cómo levantar el proyecto

### 1. Construir y levantar todos los servicios

```bash
docker-compose up --build
```

### 2. Verificar que los contenedores estén corriendo

```bash
docker ps
```

### 3. Acceder a los servicios

- **Frontend:** http://localhost:8080  
- **Backend API:** http://localhost:5000/api/concierto  
- **Health check:** http://localhost:5000/health  

### 4. Bajar el entorno

```bash
docker-compose down
```

### 5. Bajar y eliminar volúmenes

```bash
docker-compose down -v
```

---

## 🔍 Comandos de validación

```bash
# Ver contenedores activos
docker ps

# Ver redes
docker network ls
docker network inspect festival-network

# Ver volúmenes
docker volume ls
docker volume inspect festival-db-data

# Logs de un servicio
docker logs festival-backend
docker logs festival-frontend
docker logs festival-db
```

---

## 💡 Ventajas de Docker Compose

- **Un solo comando** levanta todo el entorno completo (`docker-compose up`).
- **Aislamiento por servicio**: cada contenedor corre su propio proceso sin interferir con los demás.
- **Red interna automática**: los servicios se comunican por nombre sin necesidad de IPs fijas.
- **Variables de entorno centralizadas** en `.env`, fáciles de cambiar entre ambientes (desarrollo, producción).
- **Persistencia garantizada** con volúmenes Docker: los datos de MySQL sobreviven reinicios.
- **Reproducible**: cualquier persona puede clonar el repo y levantar el mismo entorno exacto.

---

*Desarrollado por Juan Camilo Montes Velásquez — SENA CTMA ADSO 2026*
