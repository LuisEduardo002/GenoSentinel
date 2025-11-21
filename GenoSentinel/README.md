# GenoSentinel - Sistema de Gestión Genómica y Clínica

Sistema modular, seguro y escalable para la gestión y consulta de información genómica y clínica de pacientes oncológicos.

## Arquitectura del Sistema

### Microservicios

1. **Microservicio Clínica (NestJS)** - Puerto 3001
   - Gestión de pacientes
   - Catálogo de tipos de tumor
   - Historias clínicas

2. **Microservicio Genómica (Django)** - Puerto 3002
   - Catálogo de genes de interés oncológico
   - Gestión de variantes genéticas
   - Reportes de variantes por paciente

3. **Microservicio Auth/Gateway (Spring Boot)** - Puerto 3000
   - Autenticación JWT
   - Enrutamiento de peticiones
   - Simulación de API Gateway

### Tecnologías

- **Base de Datos**: MySQL 8.x
- **Orquestación**: Kubernetes
- **Documentación**: Swagger/OpenAPI
- **Contenedores**: Docker

## Estructura del Proyecto

```
GenoSentinel/
├── microservicio-clinica/     # NestJS - Gestión clínica
├── microservicio-genomica/    # Django - Gestión genómica
├── microservicio-auth/        # Spring Boot - Autenticación
├── k8s/                       # Archivos Kubernetes
├── docs/                      # Documentación y diagramas
└── README.md
```

## Instalación y Configuración

### Prerrequisitos

- Node.js 18+
- Python 3.9+
- Java JDK 17+
- MySQL 8.x
- Docker Desktop (con Kubernetes habilitado)

### Configuración de Base de Datos

```sql
-- Crear bases de datos
CREATE DATABASE genosentinel_clinica;
CREATE DATABASE genosentinel_genomica;
CREATE DATABASE genosentinel_auth;

-- Crear usuario (opcional)
CREATE USER 'genosentinel'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON genosentinel_*.* TO 'genosentinel'@'localhost';
FLUSH PRIVILEGES;
```

### Ejecución en Desarrollo

#### 1. Microservicio Clínica (NestJS)
```bash
cd microservicio-clinica
npm install
npm run start:dev
# Swagger: http://localhost:3001/api/docs
```

#### 2. Microservicio Genómica (Django)
```bash
cd microservicio-genomica
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:3002
# Swagger: http://localhost:3002/api/docs/
```

#### 3. Microservicio Auth (Spring Boot)
```bash
cd microservicio-auth
./mvnw spring-boot:run
# Endpoints: http://localhost:3000
```

## Endpoints Principales

### Microservicio Clínica (3001)
- `GET /patients` - Listar pacientes
- `POST /patients` - Crear paciente
- `GET /tumor-types` - Listar tipos de tumor
- `GET /clinical-records` - Listar historias clínicas

### Microservicio Genómica (3002)
- `GET /genes` - Listar genes
- `POST /genes` - Crear gen
- `GET /genetic-variants` - Listar variantes genéticas
- `GET /patient-variant-reports` - Reportes de variantes

### Microservicio Auth (3000)
- `POST /auth/login` - Autenticación
- `POST /auth/refresh` - Renovar token
- `GET /health` - Health check

## Despliegue en Kubernetes

```bash
# Aplicar configuraciones
kubectl apply -f k8s/

# Verificar pods
kubectl get pods

# Acceder a servicios
kubectl port-forward service/clinica-service 3001:3001
kubectl port-forward service/genomica-service 3002:3002
kubectl port-forward service/auth-service 3000:3000
```

## Flujo de Datos

1. **Cliente** → **Auth Service** (Autenticación)
2. **Auth Service** → **Clínica/Genómica Services** (Enrutamiento)
3. **Services** → **MySQL** (Persistencia)

## Documentación API

- **Clínica**: http://localhost:3001/api/docs
- **Genómica**: http://localhost:3002/api/docs/
- **Auth**: http://localhost:3000/swagger-ui.html

## Estado del Proyecto

- ✅ Microservicio Clínica (NestJS)
- 🔄 Microservicio Genómica (Django)
- ⏳ Microservicio Auth (Spring Boot)
- ⏳ Configuración Kubernetes
- ⏳ Diagrama de Arquitectura

## Contribución

1. Clonar repositorio
2. Configurar variables de entorno
3. Ejecutar servicios en desarrollo
4. Probar endpoints con Swagger

## Licencia

Proyecto académico - Universidad Autónoma de Madrid
