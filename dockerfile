# Usa una imagen base de Python
FROM python:3.8-slim



# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requerimientos y lo instala
COPY blacklist/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install newrelic
# Copia el resto de la aplicación
COPY . .

# Establece las variables de entorno
ENV FLASK_APP=application.py
ENV FLASK_RUN_HOST=0.0.0.0



WORKDIR /app/blacklist

# Expone el puerto en el que correrá la aplicación
EXPOSE 3000

# Comando para correr la aplicación
CMD ["flask", "--app", "application.py", "run", "--host=0.0.0.0", "--port=3000"]
ENV NEW_RELIC_APP_NAME="Blacklist"
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
ENV NEW_RELIC_LICENSE_KEY=886a9d67c390e80a12e217e362a81313FFFFNRAL
ENV NEW_RELIC_LOG_LEVEL=debug

ENTRYPOINT [ "newrelic-admin", "run-program" ]