#!/bin/bash

# Actualiza tus paquetes
sudo yum update -y

# Agrega el repositorio de MongoDB
echo "[mongodb-org-4.4]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/amazon/2/mongodb-org/4.4/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-4.4.asc" | sudo tee /etc/yum.repos.d/mongodb-org-4.4.repo

# Instala MongoDB
sudo yum install -y mongodb-org

# Inicia el servicio de MongoDB
sudo systemctl start mongod

# Asegúrate de que MongoDB se inicia automáticamente al reiniciar
sudo systemctl enable mongod