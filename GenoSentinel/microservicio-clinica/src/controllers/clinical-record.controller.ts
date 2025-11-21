import { Controller, Get, Post, Body, Patch, Param, Delete, Query } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiParam, ApiQuery } from '@nestjs/swagger';
import { ClinicalRecordService } from '../services/clinical-record.service';
import { CreateClinicalRecordDto } from '../dto/create-clinical-record.dto';
import { UpdateClinicalRecordDto } from '../dto/update-clinical-record.dto';

@ApiTags('clinical-records')
@Controller('clinical-records')
export class ClinicalRecordController {
  constructor(private readonly clinicalRecordService: ClinicalRecordService) {}

  @Post()
  @ApiOperation({ summary: 'Crear una nueva historia clínica' })
  @ApiResponse({ status: 201, description: 'Historia clínica creada exitosamente.' })
  @ApiResponse({ status: 400, description: 'Datos inválidos.' })
  create(@Body() createClinicalRecordDto: CreateClinicalRecordDto) {
    return this.clinicalRecordService.create(createClinicalRecordDto);
  }

  @Get()
  @ApiOperation({ summary: 'Obtener todas las historias clínicas' })
  @ApiQuery({ name: 'patientId', required: false, description: 'Filtrar por ID del paciente' })
  @ApiQuery({ name: 'tumorTypeId', required: false, description: 'Filtrar por ID del tipo de tumor' })
  @ApiResponse({ status: 200, description: 'Lista de historias clínicas obtenida exitosamente.' })
  findAll(@Query('patientId') patientId?: string, @Query('tumorTypeId') tumorTypeId?: string) {
    if (patientId) {
      return this.clinicalRecordService.findByPatient(patientId);
    }
    if (tumorTypeId) {
      return this.clinicalRecordService.findByTumorType(+tumorTypeId);
    }
    return this.clinicalRecordService.findAll();
  }

  @Get(':id')
  @ApiOperation({ summary: 'Obtener una historia clínica por ID' })
  @ApiParam({ name: 'id', description: 'ID de la historia clínica' })
  @ApiResponse({ status: 200, description: 'Historia clínica encontrada.' })
  @ApiResponse({ status: 404, description: 'Historia clínica no encontrada.' })
  findOne(@Param('id') id: string) {
    return this.clinicalRecordService.findOne(id);
  }

  @Patch(':id')
  @ApiOperation({ summary: 'Actualizar una historia clínica' })
  @ApiParam({ name: 'id', description: 'ID de la historia clínica' })
  @ApiResponse({ status: 200, description: 'Historia clínica actualizada exitosamente.' })
  @ApiResponse({ status: 404, description: 'Historia clínica no encontrada.' })
  update(@Param('id') id: string, @Body() updateClinicalRecordDto: UpdateClinicalRecordDto) {
    return this.clinicalRecordService.update(id, updateClinicalRecordDto);
  }

  @Delete(':id')
  @ApiOperation({ summary: 'Eliminar una historia clínica' })
  @ApiParam({ name: 'id', description: 'ID de la historia clínica' })
  @ApiResponse({ status: 200, description: 'Historia clínica eliminada exitosamente.' })
  @ApiResponse({ status: 404, description: 'Historia clínica no encontrada.' })
  remove(@Param('id') id: string) {
    return this.clinicalRecordService.remove(id);
  }
}
