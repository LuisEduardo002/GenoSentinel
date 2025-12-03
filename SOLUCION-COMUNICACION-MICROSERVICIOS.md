# 🔧 Solución: Error de Comunicación entre Microservicios

## ❌ Problema Identificado

El microservicio de **genómica** no podía comunicarse correctamente con el microservicio de **clínica**, generando estos errores:

```
Error de conexión con microservicio clínica
Not Found: /api/patient-reports/reports/
Bad Request: /api/patient-reports/reports/
```

## 🔍 Causas del Error

### 1. **URL Base Hardcodeada** ❌
En `apps/patient_reports/services.py` línea 33:
```python
self.base_url = "http://localhost:3007"  # ❌ Hardcodeado
```

**Problema**: No se adaptaba al entorno (Docker/K8s) donde el servicio está en `clinica-service:3001`

### 2. **Ruta de Endpoint Incorrecta** ❌
En `apps/patient_reports/services.py` línea 45:
```python
url = f"{self.base_url}/patients/{patient_id}"  # ❌ Ruta incorrecta
```

**Problema**: El controlador de NestJS usa `/patients/get/{id}`, no `/patients/{id}`

### 3. **Variable de Entorno Faltante** ❌
No se estaba configurando `CLINICAL_SERVICE_URL` en Docker ni en K8s

---

## ✅ Soluciones Aplicadas

### 1. **Fix en `services.py`** ✅

**Archivo**: `GenoSentinel/microservicio-genomica/apps/patient_reports/services.py`

**Cambios**:
```python
def __init__(self):
    # ✅ Ahora usa la configuración de settings
    self.base_url = settings.CLINICAL_SERVICE_URL
    self.timeout = getattr(settings, 'MICROSERVICE_REQUEST_TIMEOUT', 5)

def get_patient(self, patient_id: str, token: Optional[str] = None) -> Optional[Dict]:
    # ✅ Ruta correcta que coincide con el controlador de NestJS
    url = f"{self.base_url}/patients/get/{patient_id}"
```

### 2. **Actualización de Kubernetes Config** ✅

**Archivo**: `GenoSentinel/k8s/config-genomica.yaml`

**Cambio**:
```yaml
data:
  CLINICAL_SERVICE_URL: "http://microservicio-clinica:3001"  # ✅ Agregado
  CLINICA_BASE_URL: "http://microservicio-clinica:3001"
```

### 3. **Actualización de Comandos Docker** ✅

**Archivo**: `DOCKER-COMMANDS.md`

**Cambio**:
```bash
docker run -d \
  --name genomica-service \
  --network genosentinel-network \
  -e CLINICAL_SERVICE_URL=http://clinica-service:3001 \  # ✅ Agregado
  -e CLINICA_SERVICE_URL=http://clinica-service:3001 \
  -p 8000:8000 \
  genosentinel-genomica
```

---

## 🚀 Cómo Aplicar la Corrección

### **Opción A: Docker** 🐳

Si ya tienes el contenedor corriendo, debes recrearlo:

```bash
# 1. Detener y eliminar el contenedor actual
docker stop genomica-service
docker rm genomica-service

# 2. Reconstruir la imagen con el código corregido
docker build -t genosentinel-genomica ./GenoSentinel/microservicio-genomica

# 3. Ejecutar con las variables de entorno correctas
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

# 4. Verificar logs
docker logs -f genomica-service
```

### **Opción B: Kubernetes** ☸️

```bash
# 1. Actualizar el ConfigMap
kubectl apply -f GenoSentinel/k8s/config-genomica.yaml

# 2. Reconstruir la imagen Docker (si usas Minikube)
eval $(minikube docker-env)
docker build -t genosentinel/microservicio-genomica:latest ./GenoSentinel/microservicio-genomica

# 3. Reiniciar el deployment para que tome los cambios
kubectl rollout restart deployment/microservicio-genomica -n genosentinel

# 4. Verificar que el pod esté corriendo
kubectl get pods -n genosentinel -l app=microservicio-genomica

# 5. Ver logs
kubectl logs -f deployment/microservicio-genomica -n genosentinel
```

---

## ✅ Verificación de la Solución

### 1. **Verificar que el servicio genómica se conecta correctamente**

```bash
# Docker
docker logs genomica-service | grep -i "error\|connection"

# Kubernetes
kubectl logs deployment/microservicio-genomica -n genosentinel | grep -i "error\|connection"
```

**No deberías ver**: "Error de conexión con microservicio clínica"

### 2. **Probar el endpoint manualmente**

```bash
# Port-forward al servicio de genómica
kubectl port-forward svc/microservicio-genomica 8000:8000 -n genosentinel
# O en Docker: ya está expuesto en localhost:8000

# Hacer una petición de prueba (necesitas un patient_id válido)
curl http://localhost:8000/api/patient-reports/reports/
```

### 3. **Verificar conectividad interna**

```bash
# Entrar al pod/contenedor de genómica
docker exec -it genomica-service /bin/bash
# O en K8s:
kubectl exec -it deployment/microservicio-genomica -n genosentinel -- /bin/bash

# Dentro del contenedor, probar la conectividad
curl http://clinica-service:3001/health
# O en K8s:
curl http://microservicio-clinica:3001/health
```

---

## 📝 Resumen de Cambios

| Archivo | Línea/Sección | Cambio |
|---------|---------------|--------|
| `apps/patient_reports/services.py` | 31-34 | Usar `settings.CLINICAL_SERVICE_URL` en lugar de hardcode |
| `apps/patient_reports/services.py` | 45 | Cambiar ruta a `/patients/get/{id}` |
| `k8s/config-genomica.yaml` | 12 | Agregar variable `CLINICAL_SERVICE_URL` |
| `DOCKER-COMMANDS.md` | 70, 194 | Agregar `-e CLINICAL_SERVICE_URL=...` |

---

## 🎯 Resultado Esperado

Después de aplicar estos cambios:

✅ El microservicio genómica se conecta correctamente al microservicio clínica
✅ Las rutas `/api/patient-reports/reports/` funcionan correctamente
✅ No hay errores de "Error de conexión con microservicio clínica"
✅ Los reportes de pacientes se obtienen con los datos clínicos completos

---

## 📞 Siguiente Paso

1. **Aplica los cambios** según tu entorno (Docker o K8s)
2. **Verifica los logs** para confirmar que no hay errores
3. **Prueba los endpoints** de patient reports
4. Si persisten errores, verifica:
   - Que el servicio de clínica esté corriendo
   - Que la red/namespace de K8s esté correcta
   - Que los puertos sean los correctos
