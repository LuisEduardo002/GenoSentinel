import { Controller, Get } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse } from '@nestjs/swagger';

@ApiTags('health')
@Controller('health')
export class HealthController {
  @Get()
  @ApiOperation({ summary: 'Health check del microservicio' })
  @ApiResponse({ status: 200, description: 'Servicio funcionando correctamente.' })
  check() {
    return {
      status: 'ok',
      timestamp: new Date().toISOString(),
      service: 'microservicio-clinica',
      version: '1.0.0',
    };
  }
}
