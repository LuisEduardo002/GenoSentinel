import { Controller, Get, Post, Body, Patch, Param, Delete, Query } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiParam, ApiQuery } from '@nestjs/swagger';
import { TumorTypeService } from '../services/tumor-type.service';
import { CreateTumorTypeDto } from '../dto/create-tumor-type.dto';
import { UpdateTumorTypeDto } from '../dto/update-tumor-type.dto';

@ApiTags('tumor-types')
@Controller('tumor-types')
export class TumorTypeController {
  constructor(private readonly tumorTypeService: TumorTypeService) {}

  @Post()
  @ApiOperation({ summary: 'Crear un nuevo tipo de tumor' })
  @ApiResponse({ status: 201, description: 'Tipo de tumor creado exitosamente.' })
  @ApiResponse({ status: 400, description: 'Datos inválidos.' })
  create(@Body() createTumorTypeDto: CreateTumorTypeDto) {
    return this.tumorTypeService.create(createTumorTypeDto);
  }

  @Get()
  @ApiOperation({ summary: 'Obtener todos los tipos de tumor' })
  @ApiQuery({ name: 'system', required: false, description: 'Filtrar por sistema afectado' })
  @ApiResponse({ status: 200, description: 'Lista de tipos de tumor obtenida exitosamente.' })
  findAll(@Query('system') system?: string) {
    if (system) {
      return this.tumorTypeService.findBySystem(system);
    }
    return this.tumorTypeService.findAll();
  }

  @Get(':id')
  @ApiOperation({ summary: 'Obtener un tipo de tumor por ID' })
  @ApiParam({ name: 'id', description: 'ID del tipo de tumor' })
  @ApiResponse({ status: 200, description: 'Tipo de tumor encontrado.' })
  @ApiResponse({ status: 404, description: 'Tipo de tumor no encontrado.' })
  findOne(@Param('id') id: string) {
    return this.tumorTypeService.findOne(+id);
  }

  @Patch(':id')
  @ApiOperation({ summary: 'Actualizar un tipo de tumor' })
  @ApiParam({ name: 'id', description: 'ID del tipo de tumor' })
  @ApiResponse({ status: 200, description: 'Tipo de tumor actualizado exitosamente.' })
  @ApiResponse({ status: 404, description: 'Tipo de tumor no encontrado.' })
  update(@Param('id') id: string, @Body() updateTumorTypeDto: UpdateTumorTypeDto) {
    return this.tumorTypeService.update(+id, updateTumorTypeDto);
  }

  @Delete(':id')
  @ApiOperation({ summary: 'Eliminar un tipo de tumor' })
  @ApiParam({ name: 'id', description: 'ID del tipo de tumor' })
  @ApiResponse({ status: 200, description: 'Tipo de tumor eliminado exitosamente.' })
  @ApiResponse({ status: 404, description: 'Tipo de tumor no encontrado.' })
  remove(@Param('id') id: string) {
    return this.tumorTypeService.remove(+id);
  }
}
