# 🚀 Guía Completa de Despliegue en Kubernetes (K8s)

## 📋 Requisitos Previos
- Kubernetes cluster (Minikube, Kind, K3s, AKS, EKS, GKE, etc.)
- kubectl instalado y configurado
- Docker instalado
- Maven instalado (para compilar microservicio-auth)

---

## 🎯 PASO 1: Compilar el Microservicio de Autenticación (Java)

```bash
cd GenoSentinel/microservicio-auth
mvn clean package
cd ../..
```

---

## 🐳 PASO 2: Construir las Imágenes Docker

### Opción A: Usando Minikube (Recomendado para desarrollo local)

```bash
# Configurar Docker para usar el daemon de Minikube
minikube start
eval $(minikube docker-env)

# Construir las imágenes dentro de Minikube
docker build -t genosentinel/microservicio-auth:latest ./GenoSentinel/microservicio-auth
docker build -t genosentinel/microservicio-clinica:latest ./GenoSentinel/microservicio-clinica
docker build -t genosentinel/microservicio-genomica:latest ./GenoSentinel/microservicio-genomica

# Verificar que las imágenes se crearon
docker images | grep genosentinel
```

### Opción B: Usando Docker Registry (Para producción)

```bash
# Construir y etiquetar las imágenes
docker build -t tu-registry/genosentinel/microservicio-auth:latest ./GenoSentinel/microservicio-auth
docker build -t tu-registry/genosentinel/microservicio-clinica:latest ./GenoSentinel/microservicio-clinica
docker build -t tu-registry/genosentinel/microservicio-genomica:latest ./GenoSentinel/microservicio-genomica

# Subir las imágenes al registry
docker push tu-registry/genosentinel/microservicio-auth:latest
docker push tu-registry/genosentinel/microservicio-clinica:latest
docker push tu-registry/genosentinel/microservicio-genomica:latest
```

---

## ☸️ PASO 3: Desplegar en Kubernetes

### 3.1 Crear el Namespace

```bash
kubectl apply -f GenoSentinel/k8s/namespace.yaml
```

### 3.2 Verificar que el namespace se creó

```bash
kubectl get namespaces | grep genosentinel
```

### 3.3 Desplegar MySQL

```bash
# Crear el PersistentVolumeClaim para almacenamiento persistente
kubectl apply -f GenoSentinel/k8s/mysql-pvc.yaml

# Desplegar MySQL
kubectl apply -f GenoSentinel/k8s/mysql-deployment.yaml

# Crear el servicio de MySQL
kubectl apply -f GenoSentinel/k8s/mysql-service.yaml

# Verificar que MySQL esté corriendo
kubectl get pods -n genosentinel -l app=mysql
kubectl get svc -n genosentinel -l app=mysql
```

### 3.4 Esperar a que MySQL esté listo

```bash
# Observar el estado del pod de MySQL
kubectl get pods -n genosentinel -w

# Cuando el pod esté READY (1/1), presiona Ctrl+C y continúa
# O usa este comando para esperar automáticamente:
kubectl wait --for=condition=ready pod -l app=mysql -n genosentinel --timeout=300s
```

### 3.5 Crear ConfigMaps y Secrets

```bash
# ConfigMap y Secret para microservicio clínica
kubectl apply -f GenoSentinel/k8s/config-clinica.yaml

# ConfigMap y Secret para microservicio genómica
kubectl apply -f GenoSentinel/k8s/config-genomica.yaml

# Verificar
kubectl get configmaps -n genosentinel
kubectl get secrets -n genosentinel
```

### 3.6 Desplegar Microservicio de Autenticación

```bash
# Desplegar el deployment
kubectl apply -f GenoSentinel/k8s/deployment-auth.yaml

# Crear el servicio
kubectl apply -f GenoSentinel/k8s/service-auth.yaml

# Verificar
kubectl get pods -n genosentinel -l app=microservicio-auth
kubectl get svc -n genosentinel -l app=microservicio-auth
```

### 3.7 Desplegar Microservicio Clínica

```bash
# Desplegar el deployment
kubectl apply -f GenoSentinel/k8s/deployment-clinica.yaml

# Crear el servicio
kubectl apply -f GenoSentinel/k8s/service-clinica.yaml

# Verificar
kubectl get pods -n genosentinel -l app=microservicio-clinica
kubectl get svc -n genosentinel -l app=microservicio-clinica
```

### 3.8 Desplegar Microservicio Genómica

```bash
# Desplegar el deployment
kubectl apply -f GenoSentinel/k8s/deployment-genomica.yaml

# Crear el servicio
kubectl apply -f GenoSentinel/k8s/service-genomica.yaml

# Verificar
kubectl get pods -n genosentinel -l app=microservicio-genomica
kubectl get svc -n genosentinel -l app=microservicio-genomica
```

---

## ⚡ DESPLIEGUE RÁPIDO (Todos los comandos en uno)

```bash
# Compilar microservicio Java
cd GenoSentinel/microservicio-auth && mvn clean package && cd ../..

# Si usas Minikube
minikube start
eval $(minikube docker-env)

# Construir imágenes
docker build -t genosentinel/microservicio-auth:latest ./GenoSentinel/microservicio-auth
docker build -t genosentinel/microservicio-clinica:latest ./GenoSentinel/microservicio-clinica
docker build -t genosentinel/microservicio-genomica:latest ./GenoSentinel/microservicio-genomica

# Desplegar TODO en orden
kubectl apply -f GenoSentinel/k8s/namespace.yaml
kubectl apply -f GenoSentinel/k8s/mysql-pvc.yaml
kubectl apply -f GenoSentinel/k8s/mysql-deployment.yaml
kubectl apply -f GenoSentinel/k8s/mysql-service.yaml

# Esperar a que MySQL esté listo
kubectl wait --for=condition=ready pod -l app=mysql -n genosentinel --timeout=300s

# Desplegar ConfigMaps y Secrets
kubectl apply -f GenoSentinel/k8s/config-clinica.yaml
kubectl apply -f GenoSentinel/k8s/config-genomica.yaml

# Desplegar microservicios
kubectl apply -f GenoSentinel/k8s/deployment-auth.yaml
kubectl apply -f GenoSentinel/k8s/service-auth.yaml
kubectl apply -f GenoSentinel/k8s/deployment-clinica.yaml
kubectl apply -f GenoSentinel/k8s/service-clinica.yaml
kubectl apply -f GenoSentinel/k8s/deployment-genomica.yaml
kubectl apply -f GenoSentinel/k8s/service-genomica.yaml

# Ver todo
kubectl get all -n genosentinel
```

---

## 🔍 PASO 4: Verificar el Despliegue

### Ver todos los recursos

```bash
kubectl get all -n genosentinel
```

### Ver pods en detalle

```bash
kubectl get pods -n genosentinel -o wide
```

### Ver servicios

```bash
kubectl get svc -n genosentinel
```

### Ver deployments

```bash
kubectl get deployments -n genosentinel
```

### Ver ConfigMaps y Secrets

```bash
kubectl get configmaps -n genosentinel
kubectl get secrets -n genosentinel
```

### Describir un pod (para debugging)

```bash
kubectl describe pod <nombre-del-pod> -n genosentinel
```

### Ver logs de los pods

```bash
# MySQL
kubectl logs -f deployment/mysql -n genosentinel

# Microservicio Auth
kubectl logs -f deployment/microservicio-auth -n genosentinel

# Microservicio Clínica
kubectl logs -f deployment/microservicio-clinica -n genosentinel

# Microservicio Genómica
kubectl logs -f deployment/microservicio-genomica -n genosentinel
```

---

## 🌐 PASO 5: Acceder a los Servicios

### Opción A: Port-Forward (Para desarrollo local)

```bash
# MySQL
kubectl port-forward svc/mysql 3306:3306 -n genosentinel

# Microservicio Auth
kubectl port-forward svc/microservicio-auth 8080:8080 -n genosentinel

# Microservicio Clínica
kubectl port-forward svc/microservicio-clinica 3001:3001 -n genosentinel

# Microservicio Genómica
kubectl port-forward svc/microservicio-genomica 8000:8000 -n genosentinel
```

### Opción B: Usar Minikube Service (Solo Minikube)

```bash
# Exponer el servicio de auth
minikube service microservicio-auth -n genosentinel

# Exponer el servicio de clínica
minikube service microservicio-clinica -n genosentinel

# Exponer el servicio de genómica
minikube service microservicio-genomica -n genosentinel
```

### Opción C: LoadBalancer (En cloud providers)

Si cambias los servicios a tipo `LoadBalancer`:

```bash
kubectl get svc -n genosentinel
# Verás las IPs externas asignadas
```

---

## 🔗 Comunicación entre Servicios (DNS interno de K8s)

Dentro del cluster, los servicios pueden comunicarse usando DNS de Kubernetes:

- **MySQL**: `mysql.genosentinel.svc.cluster.local` (o simplemente `mysql` dentro del namespace)
- **Auth**: `microservicio-auth.genosentinel.svc.cluster.local`
- **Clínica**: `microservicio-clinica.genosentinel.svc.cluster.local`
- **Genómica**: `microservicio-genomica.genosentinel.svc.cluster.local`

**Ejemplo**: Desde el pod de `microservicio-clinica`, puedes hacer una petición HTTP a:
- `http://microservicio-auth:8080/api/...`
- `http://mysql:3306` (para conexión a BD)

---

## 🛠️ Comandos de Troubleshooting

### Ver eventos del namespace

```bash
kubectl get events -n genosentinel --sort-by='.lastTimestamp'
```

### Ejecutar comandos dentro de un pod

```bash
# Conectarse a MySQL desde el pod de MySQL
kubectl exec -it deployment/mysql -n genosentinel -- mysql -u root -p1234

# Entrar en un pod
kubectl exec -it deployment/microservicio-auth -n genosentinel -- /bin/sh
kubectl exec -it deployment/microservicio-clinica -n genosentinel -- /bin/sh
kubectl exec -it deployment/microservicio-genomica -n genosentinel -- /bin/bash
```

### Probar conectividad entre pods

```bash
# Entrar al pod de clínica
kubectl exec -it deployment/microservicio-clinica -n genosentinel -- /bin/sh

# Dentro del pod, probar conexión a MySQL
nc -zv mysql 3306

# Probar conexión a otros microservicios
curl http://microservicio-auth:8080/gateway/health
curl http://microservicio-genomica:8000/
```

### Ver uso de recursos

```bash
kubectl top pods -n genosentinel
kubectl top nodes
```

### Reiniciar un deployment

```bash
kubectl rollout restart deployment/microservicio-auth -n genosentinel
kubectl rollout restart deployment/microservicio-clinica -n genosentinel
kubectl rollout restart deployment/microservicio-genomica -n genosentinel
```

---

## 📊 Escalar los Microservicios

```bash
# Escalar a 3 réplicas
kubectl scale deployment microservicio-auth --replicas=3 -n genosentinel
kubectl scale deployment microservicio-clinica --replicas=3 -n genosentinel
kubectl scale deployment microservicio-genomica --replicas=3 -n genosentinel

# Verificar
kubectl get deployments -n genosentinel
```

---

## 🔄 Actualizar una Imagen

```bash
# Reconstruir la imagen
docker build -t genosentinel/microservicio-auth:latest ./GenoSentinel/microservicio-auth

# Forzar la recreación de los pods
kubectl rollout restart deployment/microservicio-auth -n genosentinel

# O cambiar la imagen directamente
kubectl set image deployment/microservicio-auth microservicio-auth=genosentinel/microservicio-auth:v2 -n genosentinel
```

---

## 🗑️ Eliminar Todo

```bash
# Opción 1: Eliminar el namespace completo (elimina TODO)
kubectl delete namespace genosentinel

# Opción 2: Eliminar recursos individuales
kubectl delete -f GenoSentinel/k8s/deployment-genomica.yaml
kubectl delete -f GenoSentinel/k8s/service-genomica.yaml
kubectl delete -f GenoSentinel/k8s/deployment-clinica.yaml
kubectl delete -f GenoSentinel/k8s/service-clinica.yaml
kubectl delete -f GenoSentinel/k8s/deployment-auth.yaml
kubectl delete -f GenoSentinel/k8s/service-auth.yaml
kubectl delete -f GenoSentinel/k8s/config-genomica.yaml
kubectl delete -f GenoSentinel/k8s/config-clinica.yaml
kubectl delete -f GenoSentinel/k8s/mysql-service.yaml
kubectl delete -f GenoSentinel/k8s/mysql-deployment.yaml
kubectl delete -f GenoSentinel/k8s/mysql-pvc.yaml
kubectl delete -f GenoSentinel/k8s/namespace.yaml

# Opción 3: Eliminar todo el directorio
kubectl delete -f GenoSentinel/k8s/
```

---

## 📝 Notas Importantes

### 🔹 Redes en Kubernetes

Kubernetes crea automáticamente una red virtual para todos los pods dentro del cluster. No necesitas configurar redes manualmente. Todos los servicios pueden comunicarse entre sí usando:
- **Nombre del servicio** (si están en el mismo namespace): `mysql`, `microservicio-auth`, etc.
- **FQDN** (Fully Qualified Domain Name): `mysql.genosentinel.svc.cluster.local`

### 🔹 Orden de Despliegue

Es importante seguir este orden:
1. **Namespace** primero
2. **MySQL** (PVC + Deployment + Service) y esperar a que esté listo
3. **ConfigMaps y Secrets**
4. **Microservicios** (Deployments + Services)

### 🔹 Persistencia de Datos

- Los datos de MySQL se guardan en un **PersistentVolumeClaim (PVC)**
- Aunque elimines el pod de MySQL, los datos permanecerán
- Para eliminar los datos completamente, debes eliminar el PVC:
  ```bash
  kubectl delete pvc mysql-pvc -n genosentinel
  ```

### 🔹 Health Checks

Todos los deployments tienen configurados **liveness** y **readiness probes**:
- **Liveness**: Verifica si el contenedor está vivo (si falla, K8s lo reinicia)
- **Readiness**: Verifica si el contenedor está listo para recibir tráfico

### 🔹 Variables de Entorno

Las variables de entorno se configuran a través de:
- **ConfigMaps**: Datos no sensibles (URLs, puertos, nombres de BD)
- **Secrets**: Datos sensibles (contraseñas, tokens)

---

## 🎯 Comandos Más Usados (Referencia Rápida)

```bash
# Ver todo
kubectl get all -n genosentinel

# Ver pods
kubectl get pods -n genosentinel

# Ver logs
kubectl logs -f deployment/microservicio-auth -n genosentinel

# Port-forward
kubectl port-forward svc/microservicio-auth 8080:8080 -n genosentinel

# Describir un recurso
kubectl describe pod <pod-name> -n genosentinel

# Ejecutar comando en un pod
kubectl exec -it deployment/microservicio-clinica -n genosentinel -- sh

# Reiniciar deployment
kubectl rollout restart deployment/microservicio-auth -n genosentinel

# Escalar
kubectl scale deployment microservicio-auth --replicas=3 -n genosentinel

# Eliminar todo
kubectl delete namespace genosentinel
```

---

## ✅ Verificación Final

Después del despliegue, ejecuta estos comandos para verificar que todo esté funcionando:

```bash
# 1. Todos los pods deben estar READY
kubectl get pods -n genosentinel

# 2. Todos los servicios deben tener ClusterIP asignado
kubectl get svc -n genosentinel

# 3. Ver logs de cada microservicio (no debe haber errores graves)
kubectl logs deployment/microservicio-auth -n genosentinel --tail=50
kubectl logs deployment/microservicio-clinica -n genosentinel --tail=50
kubectl logs deployment/microservicio-genomica -n genosentinel --tail=50

# 4. Probar endpoints con port-forward
kubectl port-forward svc/microservicio-auth 8080:8080 -n genosentinel
# En otra terminal: curl http://localhost:8080/gateway/health
```

---

¡Listo! 🚀 Tu aplicación GenoSentinel está desplegada en Kubernetes con todos los microservicios comunicándose entre sí a través de la red interna de K8s.
