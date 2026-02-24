# KalmyPT
Solución a la prueba técnica para Kalmy.

---

## Requisitos

- Python 3.10+
- pip

---

## Cómo correr la API

**1. Clona el repositorio**
```bash
git clone <url-del-repo>
cd KalmyPT
```

**2. Crea y activa el entorno virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Instala las dependencias**
```bash
pip install -r requirements.txt
```

**4. Crea el archivo `.env`**
```bash
DATABASE_URL=sqlite:///./items.db
```

**5. Corre la API**
```bash
uvicorn app.main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`

La documentación automática estará disponible en:
- Swagger UI: `http://127.0.0.1:8000/docs`
- Redoc: `http://127.0.0.1:8000/redoc`

---

## Cómo correr los tests
Con el venv activado y en la carpeta KalmyPT pon lo siguiente:

```bash
pytest tests/ -v
```

Los tests usan una base de datos separada `test.db` que se crea y se elimina automáticamente en cada ejecución, por lo que no afectan la base de datos real.

---

## Endpoints

| Método | Ruta | Descripción | Status Code |
|--------|------|-------------|-------------|
| GET | `/items/` | Lista todos los items con paginación | 200 |
| GET | `/items/{id}` | Obtiene un item por ID | 200 |
| POST | `/items/` | Crea un item | 201 |
| PUT | `/items/{id}` | Actualiza un item | 200 |
| DELETE | `/items/{id}` | Elimina un item | 204 |

### Paginación

El endpoint `GET /items/` soporta paginación mediante query params:

```
GET /items/?page=1&size=10
```

| Param | Tipo | Default | Validación |
|-------|------|---------|------------|
| page | int | 1 | >= 1 |
| size | int | 10 | >= 1, <= 100 |

Respuesta:
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "size": 10
}
```

### Modelo de datos

```json
{
  "id": 1,
  "name": "Laptop",
  "description": "Laptop gamer",
  "price": 1500.00,
  "available": true
}
```

| Campo | Tipo | Obligatorio | Validación |
|-------|------|-------------|------------|
| name | string | SI | min 1, max 100 caracteres |
| description | string | SI | max 500 caracteres |
| price | float | SI | mayor a 0 |
| available | bool | NO | default true |

---

## Decisiones tecnológicas

### Stack

- **FastAPI** → Lo que pidieron para esta prueba técnica, pero esta bien porque bien con documentación automática via OpenAPI/Swagger y tiene integración con Pydantic para validaciones.
- **SQLAlchemy** → ORM (Object Relational Mapper) que permite trabajar con la base de datos en Python sin escribir SQL. Si se cambia de SQLite a PostgreSQL, el código no cambia.
- **Pydantic** → Validación automática de datos de entrada y salida. Si un campo tiene el tipo incorrecto, rechaza el request automáticamente con un 422. Ahora tener que escribir a mano las validaciones.
- **SQLite** → Base de datos de archivo, ideal para desarrollo local sin necesidad de configurar un servidor. Para producción en AWS solo se cambia la variable `DATABASE_URL` en el `.env`.
- **pytest + httpx** → Testing de endpoints sin necesidad de levantar un servidor real.

### Patrón de arquitectura

**Descartados:**

- **MVC** → No aplica bien en APIs porque no hay una vista como en una app web.
- **Arquitectura Hexagonal** → Nunca lo he usado y demasiado compleja para este scope. Sé que se usa para integrar más servicios de forma sencilla pero para el scope de este proyecto no es necesario.
- **Clean Architecture** → Misma razón que la hexagonal. Pero esta la he usado en apps móviles con MVVM.
- **Monolito sin capas** → Poner todo en `main.py` haría el código difícil de testear y mantener.
- **Factory Pattern** → Útil cuando hay múltiples tipos de objetos con construcción diferente, pero todos los Items tienen la misma estructura.

**Patrón elegido: Arquitectura en Capas + Repository + Service**

Es fácil de implementar, permite separar responsabilidades y es ideal para el scope de este proyecto sin ser demasiado complejo. Cada capa tiene un único trabajo:

```
api/          →  recibe el request y delega
services/     →  lógica de negocio y validaciones de dominio
repositories/ →  queries a la base de datos
models/       →  estructura de las tablas
schemas/      →  validación de entrada y salida
```

Si el proyecto crece este patrón permite escalarlo y manterlo más facil.

---

## Estructura del proyecto

```
app/
├── main.py
├── core/
│   ├── config.py
│   └── database.py
├── models/
│   └── item.py
├── schemas/
│   └── item.py
├── repositories/
│   └── item_repository.py
├── services/
│   └── item_service.py
└── api/
    └── items.py
tests/
├── conftest.py
└── test_items.py
.env
.gitignore
requirements.txt
README.md
```