import { IsString, IsDateString, IsNotEmpty, IsUUID, IsNumber, MaxLength, IsOptional } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class CreateClinicalRecordDto {
  @ApiProperty({ description: 'ID del paciente', example: '123e4567-e89b-12d3-a456-426614174000' })
  @IsUUID()
  @IsNotEmpty()
  patientId: string;

  @ApiProperty({ description: 'ID del tipo de tumor', example: 1 })
  @IsNumber()
  @IsNotEmpty()
  tumorTypeId: number;

  @ApiProperty({ description: 'Fecha de diagnóstico', example: '2024-01-15' })
  @IsDateString()
  diagnosisDate: string;

  @ApiProperty({ description: 'Estadio del tumor', example: 'IIA' })
  @IsString()
  @IsNotEmpty()
  @MaxLength(10)
  stage: string;

  @ApiProperty({ description: 'Protocolo de tratamiento', example: 'Quimioterapia con doxorubicina y ciclofosfamida' })
  @IsString()
  @IsNotEmpty()
  treatmentProtocol: string;

  @ApiProperty({ description: 'Notas adicionales', example: 'Paciente responde bien al tratamiento', required: false })
  @IsString()
  @IsOptional()
  notes?: string;
}
