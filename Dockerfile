FROM python:3.14-slim

LABEL org.opencontainers.image.title="Monitor de estabilidad de Horario de Bus"
LABEL org.opencontainers.image.authors="Arecmon605"
LABEL org.opencontainers.image.source="https://github.com/ARMO575/monitor-app-03"

WORKDIR /app

COPY monitor_app.py .

CMD ["python", "monitor_app.py"]
