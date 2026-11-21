# Monitor de estabilidad de la aplicación APP-03

Programa de menú que analiza las descargas y las caídas semanales de la aplicación móvil **Horario de Bus** (APP-03) a lo largo de doce semanas.

- **Módulo:** IC44 — Fundamentos de programación en Python
- **Unidad:** 2 — Estructuras de control, depuración y excepciones
- **Pareja:** Pareja 2
- **Autor:** Arecmon605

## Aplicación analizada

| Dato | Valor |
|---|---|
| Código | APP-03 |
| Nombre | Horario de Bus |
| Semanas analizadas | 12 |

## Ejecución desde Docker Hub

No hace falta clonar el proyecto ni tener Python instalado. Al ser un programa interactivo por consola que pide entradas por teclado, se debe arrancar con el modificador `-it`:

```bash
docker run --rm -it --pull always Arecmon605/monitor-app-03:1.0.0
```

Repositorio público en Docker Hub:  
https://hub.docker.com/r/Arecmon605/monitor-app-03

## Ejecución en local

Requiere Python 3.10 o superior (solo utiliza la biblioteca estándar de Python):

```bash
# Crear entorno virtual
python -m venv .venv

# Activar en Windows:
.venv\Scripts\activate

# Activar en Linux/macOS:
source .venv/bin/activate

# Ejecutar el programa
python monitor_app.py
```

## Construcción de la imagen Docker

Construcción y ejecución local:

```bash
docker build -t monitor-app-03 .
docker run --rm -it monitor-app-03
```

Construcción y publicación multiarquitectura (`linux/amd64` y `linux/arm64`):

```bash
docker buildx build --platform linux/amd64,linux/arm64 \
  -t Arecmon605/monitor-app-03:1.0.0 \
  -t Arecmon605/monitor-app-03:latest \
  --push .
```

## Estructura del repositorio

```
monitor-app-03/
├── .dockerignore      # Archivos excluidos de la imagen Docker
├── .gitignore          # Archivos omitidos por Git
├── Dockerfile          # Receta del contenedor Docker
├── README.md           # Documentación del proyecto
├── requirements.txt    # Dependencias (vacío: solo biblioteca estándar)
└── monitor_app.py      # Código fuente del programa
```
