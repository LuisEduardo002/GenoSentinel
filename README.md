# GenoSentinel

Sistema distribuido para la gestión integrada de información clínica y genómica de pacientes oncológicos, desarrollado bajo una arquitectura de microservicios y desplegable en Kubernetes.

## Descripción

GenoSentinel centraliza la información clínica y genómica de pacientes oncológicos mediante una arquitectura modular, segura y escalable.

El sistema permite:

- Gestión de pacientes y registros clínicos.
- Administración de tipos de tumores oncológicos.
- Catalogación de genes de interés clínico.
- Registro de variantes genéticas.
- Asociación de variantes genómicas con pacientes.
- Autenticación y autorización mediante JWT.
- Comunicación entre microservicios a través de un API Gateway.
- Despliegue en contenedores Docker y orquestación con Kubernetes.

---

## Arquitectura

La solución está compuesta por tres microservicios desacoplados:

### Servicio de Autenticación y Gateway

Tecnología: Spring Boot

Responsabilidades:

- Autenticación de usuarios.
- Emisión y validación de tokens JWT.
- Simulación de API Gateway.
- Enrutamiento de peticiones.
- Monitoreo básico de servicios.

### Servicio Clínico

Tecnología: Spring Boot

Responsabilidades:

- Gestión de pacientes.
- Gestión de tipos de tumor.
- Gestión de historias clínicas.
- Exposición de endpoints REST documentados con Swagger.

### Servicio Genómico

Tecnología: NestJS

Responsabilidades:

- Gestión de genes de interés.
- Gestión de variantes genéticas.
- Generación de reportes genómicos asociados a pacientes.
- Integración con el servicio clínico.
- Documentación Swagger.

---

## Arquitectura General

Cliente

↓

API Gateway / Authentication Service

↓

Clinical Service ←→ Genomic Service

↓

MySQL

---

## Tecnologías Utilizadas

### Backend

- Spring Boot
- NestJS
- Java
- TypeScript

### Bases de Datos

- MySQL
- JPA / Hibernate
- TypeORM

### Seguridad

- JWT Authentication
- Spring Security

### DevOps

- Docker
- Kubernetes
- ConfigMaps
- Secrets
- Persistent Volumes

### Documentación

- Swagger / OpenAPI

---

## Funcionalidades Implementadas

### Gestión Clínica

- Crear pacientes
- Actualizar pacientes
- Consultar pacientes
- Desactivar pacientes
- Registrar historias clínicas
- Gestionar tipos de tumor

### Gestión Genómica

- Registrar genes
- Registrar variantes genéticas
- Asociar variantes a pacientes
- Generar reportes genómicos

### Seguridad

- Login de usuarios
- Emisión de JWT
- Validación de tokens
- Control de acceso centralizado

---

## Diseño de Software

El proyecto implementa:

- Arquitectura de microservicios
- DTOs para transferencia de datos
- Validación de entradas
- Separación de responsabilidades
- Persistencia mediante ORM
- Principios REST
- Despliegue cloud-native

---

## Documentación API

Cada microservicio expone documentación Swagger.

### Clinical Service

```bash
http://localhost:XXXX/swagger-ui.html
```

### Genomic Service

```bash
http://localhost:XXXX/api
```

---

## Kubernetes

La solución fue diseñada para ejecutarse en un entorno Kubernetes mediante:

- Deployments
- Services
- ConfigMaps
- Secrets
- Persistent Volumes
- Health Checks
- Readiness Probes

Cada microservicio puede escalar de forma independiente.

---

## Estructura del Proyecto

```text
GenoSentinel/
│
├── microservicio-auth/
│
├── microservicio-clinica/
│
├── microservicio-genomica/
│
├── k8s/
│
└── docs/
```

---

## Competencias Técnicas Demostradas

- Desarrollo Backend
- Arquitectura de Microservicios
- Spring Boot
- NestJS
- JWT Authentication
- Docker
- Kubernetes
- API Gateway Pattern
- Swagger/OpenAPI
- MySQL
- ORM
- REST APIs
- Software Architecture

---

## Autor

Luis Eduardo

Estudiante de Ingeniería de Sistemas

Backend Developer

GitHub:
https://github.com/LuisEduardo002
