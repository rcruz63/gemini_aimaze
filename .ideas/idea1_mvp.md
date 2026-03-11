# Idea 1: Configuración del Entorno y Esqueleto del Proyecto

**El Prompt (La Idea para la herramienta):**

> "Inicia el proyecto `ndd_aimaze`. Configura `pyproject.toml` usando Python 3.12+ y añade `pytest` y `pydantic` como dependencias de desarrollo usando `uv` (prohibido usar `pip`). Crea la estructura de directorios base según la arquitectura: `engine/`, `ai/`, `models/`, y `gameplay/`. Configura el linter/formateador para respetar un máximo de 88 caracteres por línea. Finalmente, crea el archivo `CHANGELOG.md` inicial y haz el primer commit. Todo el código debe pasar linting y tests vacíos."

* **Qué debe hacer su plan:** Crear carpetas, inicializar el entorno virtual con `uv`, instalar `pydantic` y `pytest`, configurar herramientas (ej. Ruff/Black en pyproject.toml) y crear el CHANGELOG.
* **Qué observar al finalizar:** * El directorio `.venv` existe.
* Hay un `CHANGELOG.md` con la primera entrada.
* La estructura de carpetas es idéntica a la del documento de arquitectura.
