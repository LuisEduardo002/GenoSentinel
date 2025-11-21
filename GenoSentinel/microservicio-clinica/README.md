# Microservicio Clínica - GenoSentinel

Microservicio para la gestión de información clínica de pacientes oncológicos.

## Características

- **Gestión de Pacientes**: CRUD completo con estados (Activo, Seguimiento, Inactivo)
- **Tipos de Tumor**: Catálogo de patologías oncológicas
- **Historias Clínicas**: Registro de diagnósticos y tratamientos
- **Documentación Swagger**: API completamente documentada
- **Validación de DTOs**: Validación automática de datos de entrada
- **TypeORM**: ORM para interacción con MySQL

## Tecnologías

- NestJS 10.x
- TypeORM 0.3.x
- MySQL 8.x
- Swagger/OpenAPI
- Class Validator

## Instalación

```bash
# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones de base de datos

# Ejecutar en desarrollo
npm run start:dev

# Construir para producción
npm run build
npm run start:prod
```

## Endpoints Principales

### Pacientes
- `GET /patients` - Listar pacientes
- `POST /patients` - Crear paciente
- `GET /patients/:id` - Obtener paciente
- `PATCH /patients/:id` - Actualizar paciente
- `PATCH /patients/:id/deactivate` - Desactivar paciente
- `DELETE /patients/:id` - Eliminar paciente

### Tipos de Tumor
- `GET /tumor-types` - Listar tipos de tumor
- `POST /tumor-types` - Crear tipo de tumor
- `GET /tumor-types/:id` - Obtener tipo de tumor
- `PATCH /tumor-types/:id` - Actualizar tipo de tumor
- `DELETE /tumor-types/:id` - Eliminar tipo de tumor

### Historias Clínicas
- `GET /clinical-records` - Listar historias clínicas
- `POST /clinical-records` - Crear historia clínica
- `GET /clinical-records/:id` - Obtener historia clínica
- `PATCH /clinical-records/:id` - Actualizar historia clínica
- `DELETE /clinical-records/:id` - Eliminar historia clínica

## Documentación API

Una vez ejecutando el servidor, la documentación Swagger estará disponible en:
`http://localhost:3001/api/docs`

## Base de Datos

El microservicio creará automáticamente las tablas necesarias:
- `patients` - Información de pacientes
- `tumor_types` - Catálogo de tipos de tumor
- `clinical_records` - Historias clínicas

## Variables de Entorno

```env
DB_HOST=localhost
DB_PORT=3306
DB_USERNAME=root
DB_PASSWORD=password
DB_DATABASE=genosentinel_clinica
PORT=3001
NODE_ENV=development
```
