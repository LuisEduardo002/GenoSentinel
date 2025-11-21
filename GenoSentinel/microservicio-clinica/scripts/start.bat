@echo off
echo 🏥 Iniciando Microservicio Clínica - GenoSentinel
echo.

echo Verificando dependencias...
if not exist "node_modules" (
    echo Instalando dependencias...
    npm install
)

echo.
echo Iniciando servidor en modo desarrollo...
npm run start:dev
