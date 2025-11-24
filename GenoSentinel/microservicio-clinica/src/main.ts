import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Enable validation pipes globally
  app.useGlobalPipes(new ValidationPipe({
    whitelist: true,
    forbidNonWhitelisted: true,
    transform: true,
  }));

  // Enable CORS
  app.enableCors();

  // Swagger configuration
  const config = new DocumentBuilder()
    .setTitle('GenoSentinel - Microservicio Clínica')
    .setDescription('API para gestión de información clínica de pacientes oncológicos')
    .setVersion('1.0')
    .addTag('patients', 'Gestión de pacientes')
    .addTag('tumor-types', 'Gestión de tipos de tumor')
    .addTag('clinical-records', 'Gestión de historias clínicas')
    .build();

  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs', app, document);

  const port = process.env.PORT || 3001;
  await app.listen(port);
  console.log(`Microservicio Clínica ejecutándose en puerto ${port}`);
  console.log(`Documentación Swagger disponible en: http://localhost:${port}/api/docs`);
}
bootstrap();
