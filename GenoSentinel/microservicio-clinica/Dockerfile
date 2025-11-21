FROM node:18-alpine

WORKDIR /app

# Instalar curl para el HEALTHCHECK
RUN apk add --no-cache curl

# Copiar package.json y package-lock.json
COPY package*.json ./

# Instalar dependencias (solo producción)
RUN npm ci --only=production

# Copiar el resto del código
COPY . .

# Construir la aplicación
RUN npm run build

# Puerto del microservicio
EXPOSE 3001

# Health check del contenedor
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3001/health || exit 1

# Comando de arranque
CMD ["npm", "run", "start:prod"]