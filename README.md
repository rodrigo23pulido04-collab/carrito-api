# API Robot (Django + DRF + PostgreSQL)

API de **solo consulta** con 3 tablas independientes (sin relaciones).
Seguridad: **JWT** (credenciales de usuario) **+ clave API** (header `X-API-Key`).

## 1. Instalación
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # y edita los datos de PostgreSQL y SECRET_KEY
```

## 2. Base de datos (PostgreSQL)
```sql
CREATE DATABASE robot_db;
```
```bash
python manage.py migrate
python manage.py createsuperuser   # = tus "claves de acceso" (usuario/contraseña)
```

## 3. Crear la clave API
```bash
python manage.py runserver
```
Entra a http://localhost:8000/admin/ → **Rest_Framework_Api_Key → API keys → Add**.
La clave completa **solo se muestra una vez** al crearla; guárdala.

Desde el mismo admin puedes capturar datos en Componentes, Historial de decisiones y Tiempos de reacción
(la API es solo lectura, así que los datos se cargan por admin o por SQL).

## 4. Uso
**Login (JWT)** — solo usuario y contraseña:
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"TU_USUARIO","password":"TU_PASSWORD"}'
# -> {"refresh": "...", "access": "..."}
```
**Renovar token:** `POST /api/auth/token/refresh/` con `{"refresh": "..."}`

**Consultas** — requieren ambos headers:
```bash
curl http://localhost:8000/api/componentes/ \
  -H "Authorization: Bearer <access>" \
  -H "X-API-Key: <tu_clave_api>"
```

| Endpoint | Descripción |
|---|---|
| `GET /api/componentes/` y `/api/componentes/<nombre>/` | Componentes |
| `GET /api/historial-decisiones/` y `/<id>/` | Historial de decisiones |
| `GET /api/tiempos-reaccion/` y `/<id>/` | Tiempos de reacción |

Sin token → 401, sin clave API → 403, POST/PUT/PATCH/DELETE → 405.

## Tablas
- **componentes**: `nombre` (PK, not null), `tipo` (not null), `voltaje` (null), `cantidad` (not null), `descripcion`
- **historial_decisiones**: `id`, `tipo` (derecha/izquierda/alto/avanzar), `senaleticas` (imágenes detectadas), `indice_confianza`
- **tiempos_reaccion**: `id`, `t_avance_maximo`, `t_avance_minimo`, `t_detenerse_maximo`, `t_detenerse_minimo`, `latencia_ms`
  (`velocidad` quedó pendiente en el pizarrón; se agrega después con una migración)
