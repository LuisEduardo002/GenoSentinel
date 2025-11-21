import { Controller, Get, Post, Body, Patch, Param, Delete, Query } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiParam, ApiQuery } from '@nestjs/swagger';
import { PatientService } from '../services/patient.service';
import { CreatePatientDto } from '../dto/create-patient.dto';
import { UpdatePatientDto } from '../dto/update-patient.dto';

@ApiTags('patients')
@Controller('patients')
export class PatientController {
  constructor(private readonly patientService: PatientService) {}

  @Post()
  @ApiOperation({ summary: 'Crear un nuevo paciente' })
  @ApiResponse({ status: 201, description: 'Paciente creado exitosamente.' })
  @ApiResponse({ status: 400, description: 'Datos inválidos.' })
  create(@Body() createPatientDto: CreatePatientDto) {
    return this.patientService.create(createPatientDto);
  }

  @Get()
  @ApiOperation({ summary: 'Obtener todos los pacientes' })
  @ApiQuery({ name: 'status', required: false, description: 'Filtrar por estado del paciente' })
  @ApiResponse({ status: 200, description: 'Lista de pacientes obtenida exitosamente.' })
  findAll(@Query('status') status?: string) {
    if (status) {
      return this.patientService.findByStatus(status);
    }
    return this.patientService.findAll();
  }

  @Get(':id')
  @ApiOperation({ summary: 'Obtener un paciente por ID' })
  @ApiParam({ name: 'id', description: 'ID del paciente' })
  @ApiResponse({ status: 200, description: 'Paciente encontrado.' })
  @ApiResponse({ status: 404, description: 'Paciente no encontrado.' })
  findOne(@Param('id') id: string) {
    return this.patientService.findOne(id);
  }

  @Patch(':id')
  @ApiOperation({ summary: 'Actualizar un paciente' })
  @ApiParam({ name: 'id', description: 'ID del paciente' })
  @ApiResponse({ status: 200, description: 'Paciente actualizado exitosamente.' })
  @ApiResponse({ status: 404, description: 'Paciente no encontrado.' })
  update(@Param('id') id: string, @Body() updatePatientDto: UpdatePatientDto) {
    return this.patientService.update(id, updatePatientDto);
  }

  @Patch(':id/deactivate')
  @ApiOperation({ summary: 'Desactivar un paciente' })
  @ApiParam({ name: 'id', description: 'ID del paciente' })
  @ApiResponse({ status: 200, description: 'Paciente desactivado exitosamente.' })
  @ApiResponse({ status: 404, description: 'Paciente no encontrado.' })
  deactivate(@Param('id') id: string) {
    return this.patientService.deactivate(id);
  }

  @Delete(':id')
  @ApiOperation({ summary: 'Eliminar un paciente' })
  @ApiParam({ name: 'id', description: 'ID del paciente' })
  @ApiResponse({ status: 200, description: 'Paciente eliminado exitosamente.' })
  @ApiResponse({ status: 404, description: 'Paciente no encontrado.' })
  remove(@Param('id') id: string) {
    return this.patientService.remove(id);
  }
}
