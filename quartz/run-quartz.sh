#!/bin/bash

# En el caso de que se ejecute el cronjob levantamos las variables
# del contenedor
xargs -0 -L1 -a /proc/1/environ | grep QUARTZ > /etc/environment

# Usamos las variables de entorno que nos pasan cuando se levanta el contenedor
# y sino dejamos las default para que rompa el .py
echo "[quartz]
api_key = ${QUARTZ_API_KEY:-XXXXXX}
url = ${QUARTZ_URL:-https://xxxxxxxx}
isp = ${QUARTZ_ISP:-Nombre del ISP (Fibertel, Telecentro, etc.)} \
" > /root/.config/quartz.conf

# Corremos el script y lo logueamos just in case
/usr/local/bin/python /app/quartz.py >> /app/quartz.log 2>&1