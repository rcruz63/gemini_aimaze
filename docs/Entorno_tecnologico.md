# Entorno Tecnológico

## Principios

- Usamos uv como gestor de paquetes
- Usamos pyenv como gestor de versiones de python
- Usamos pytest como framework de pruebas
- El codigo tiene que seguir buenas prácticas y no generar errores de linting
- DEBE seguirse una bitacora de cambios. No se puede hacer ningún cambio sin que se registre en la bitacora.
- Maxima longitud de las lineas de codigo es de 88 caracteres.
- Maxima complejidad ciclomatica es de 10.
- Las funciones deben ser pequeñas y tener una sola responsabilidad.
- Se deben extraer helpers cuando sea necesario para reducir la complejidad.
- Se deben mantener los archivos focados. Se deben dividir en modulos cuando sean necesarios.
- Se debe documentar en el código, no en documentos externos. Los documentos externos son para los humanos. Debemos documentar el codigo para facilitar su mantenimiento por IA.
- Se utilizará ollama en entorno de desarrollo. Y openAI en entorno de producción.
- Se debe usar early returns para reducir la complejidad.
- El jugador principal se expresa en Español de España, debe ser el lenguaje del juego.

### Commits

Conventional Commits format: `tipo(scope): descripción`  
Types: `feat`, `fix`, `chore`, `refactor`, `docs`, `test`  
Commit frequently at atomic steps.

### Dependencies

Use `uv add <package>` (never `pip install`) to add dependencies. 
Se creara un entorno virtual con uv en la raiz del proyecto.
Se debe usar el entorno virtual para instalar las dependencias.
Se debe usar el entorno virtual para ejecutar el codigo (source .venv/bin/activate | uv run python main.py)
