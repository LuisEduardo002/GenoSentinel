# 🐳 Comandos Docker - GenoSentinel

## ⚡ COMANDOS RÁPIDOS (copia y pega en orden)

### 1️⃣ Crear la red Docker
```bash
docker network create genosentinel-network
```

### 2️⃣ Ejecutar MySQL
```bash
docker run -d \
  --name mysql \
  --network genosentinel-network \
  -e MYSQL_ROOT_PASSWORD=1234 \
  -e MYSQL_DATABASE=genosentinel_db \
  -p 3306:3306 \
  mysql:8.0
```

### 3️⃣ Compilar microservicio Java
```bash
cd GenoSentinel/microservicio-auth
mvn clean package
cd ../..
```

### 4️⃣ Construir imágenes Docker
```bash
docker build -t genosentinel-auth ./GenoSentinel/microservicio-auth
docker build -t genosentinel-clinica ./GenoSentinel/microservicio-clinica
docker build -t genosentinel-genomica ./GenoSentinel/microservicio-genomica
```

### 5️⃣ Ejecutar microservicio de autenticación
```bash
docker run -d \
  --name auth-service \
  --network genosentinel-network \
  -e SPRING_DATASOURCE_URL=jdbc:mysql://mysql:3306/genosentinel_db \
  -e SPRING_DATASOURCE_USERNAME=root \
  -e SPRING_DATASOURCE_PASSWORD=1234 \
  -p 8080:8080 \
  genosentinel-auth
```

### 6️⃣ Ejecutar microservicio clínica
```bash
docker run -d \
  --name clinica-service \
  --network genosentinel-network \
  -e DB_HOST=mysql \
  -e DB_PORT=3306 \
  -e DB_USERNAME=root \
  -e DB_PASSWORD=1234 \
  -e DB_DATABASE=genosentinel_clinica \
  -e AUTH_SERVICE_URL=http://auth-service:8080 \
  -e GENOMICA_SERVICE_URL=http://genomica-service:8000 \
  -p 3001:3001 \
  genosentinel-clinica
```

### 7️⃣ Ejecutar microservicio genómica
```bash
docker run -d \
  --name genomica-service \
  --network genosentinel-network \
  -e DB_HOST=mysql \
  -e DB_PORT=3306 \
  -e DB_NAME=genosentinel_genomica \
  -e DB_USER=root \
  -e DB_PASSWORD=1234 \
  -e CLINICAL_SERVICE_URL=http://clinica-service:3001 \
  -e AUTH_SERVICE_URL=http://auth-service:8080 \
  -e CLINICA_SERVICE_URL=http://clinica-service:3001 \
  -p 8000:8000 \
  genosentinel-genomica
```

---

## 🔍 Verificar que todo está corriendo

```bash
# Ver contenedores
docker ps

# Ver la red
docker network inspect genosentinel-network

# Ver logs
docker logs mysql
docker logs auth-service
docker logs clinica-service
docker logs genomica-service
```

---

## 🛑 Detener todo

```bash
docker stop genomica-service clinica-service auth-service mysql
docker rm genomica-service clinica-service auth-service mysql
docker network rm genosentinel-network
```

---

## 🔄 Reiniciar un servicio

```bash
# Detener y eliminar
docker stop auth-service
docker rm auth-service

# Volver a ejecutar (usa el mismo comando del paso 5, 6 o 7)
docker run -d \
  --name auth-service \
  --network genosentinel-network \
  -e SPRING_DATASOURCE_URL=jdbc:mysql://mysql:3306/genosentinel_db \
  -e SPRING_DATASOURCE_USERNAME=root \
  -e SPRING_DATASOURCE_PASSWORD=1234 \
  -p 8080:8080 \
  genosentinel-auth
```

---

## 🌐 Comunicación entre contenedores

Todos los contenedores están en la red `genosentinel-network` y pueden comunicarse usando los nombres:

- `mysql` → Base de datos (puerto 3306)
- `auth-service` → Autenticación (puerto 8080)
- `clinica-service` → Clínica (puerto 3001)
- `genomica-service` → Genómica (puerto 8000)

**Ejemplo**: Desde `clinica-service` puedes hacer peticiones a:
- `http://auth-service:8080/api/...`
- `http://genomica-service:8000/api/...`
- `mysql:3306` (conexión a base de datos)

---

## 🧪 Probar conectividad

```bash
# Entrar a un contenedor
docker exec -it clinica-service sh

# Desde dentro del contenedor, probar conexión
ping mysql
ping auth-service
ping genomica-service
curl http://auth-service:8080/gateway/health
```

---

## 📦 Acceder desde tu máquina local

- MySQL: `localhost:3306`
- Auth: `http://localhost:8080`
- Clínica: `http://localhost:3001`
- Genómica: `http://localhost:8000`

---

## ⚡ SCRIPT COMPLETO (Todo en uno)

```bash
# Crear red
docker network create genosentinel-network

# MySQL
docker run -d --name mysql --network genosentinel-network -e MYSQL_ROOT_PASSWORD=1234 -e MYSQL_DATABASE=genosentinel_db -p 3306:3306 mysql:8.0

# Compilar Java
cd GenoSentinel/microservicio-auth && mvn clean package && cd ../..

# Construir imágenes
docker build -t genosentinel-auth ./GenoSentinel/microservicio-auth
docker build -t genosentinel-clinica ./GenoSentinel/microservicio-clinica
docker build -t genosentinel-genomica ./GenoSentinel/microservicio-genomica

# Esperar 20 segundos a que MySQL esté listo
sleep 20

# Ejecutar microservicios
docker run -d --name auth-service --network genosentinel-network -e SPRING_DATASOURCE_URL=jdbc:mysql://mysql:3306/genosentinel_db -e SPRING_DATASOURCE_USERNAME=root -e SPRING_DATASOURCE_PASSWORD=1234 -p 8080:8080 genosentinel-auth

docker run -d --name clinica-service --network genosentinel-network -e DB_HOST=mysql -e DB_PORT=3306 -e DB_USERNAME=root -e DB_PASSWORD=1234 -e DB_DATABASE=genosentinel_clinica -e AUTH_SERVICE_URL=http://auth-service:8080 -e GENOMICA_SERVICE_URL=http://genomica-service:8000 -p 3001:3001 genosentinel-clinica

docker run -d --name genomica-service --network genosentinel-network -e DB_HOST=mysql -e DB_PORT=3306 -e DB_NAME=genosentinel_genomica -e DB_USER=root -e DB_PASSWORD=1234 -e CLINICAL_SERVICE_URL=http://clinica-service:3001 -e AUTH_SERVICE_URL=http://auth-service:8080 -e CLINICA_SERVICE_URL=http://clinica-service:3001 -p 8000:8000 genosentinel-genomica

# Ver estado
docker ps
```
