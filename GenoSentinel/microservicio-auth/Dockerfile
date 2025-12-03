# Imagen de runtime con Java 17
FROM eclipse-temurin:17-jre
WORKDIR /app

# Copiar el JAR ya construido localmente (ejecuta antes: mvn clean package)
COPY target/microservicio-auth-0.0.1-SNAPSHOT.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java","-jar","/app/app.jar"]