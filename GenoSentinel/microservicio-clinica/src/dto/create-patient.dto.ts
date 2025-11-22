import { IsString, IsDateString, IsEnum, IsNotEmpty, MaxLength } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class CreatePatientDto {
  @ApiProperty({ description: 'Nombre del paciente', example: 'Juan' })
  @IsString()
  @IsNotEmpty()
  @MaxLength(100)
  firstName: string;

  @ApiProperty({ description: 'Apellido del paciente', example: 'Pérez' })
  @IsString()
  @IsNotEmpty()
  @MaxLength(100)
  lastName: string;

  @ApiProperty({ description: 'Fecha de nacimiento', example: '1980-05-15' })
  @IsDateString()
  birthDate: string;

  @ApiProperty({ description: 'Género del paciente', example: 'Masculino', enum: ['Masculino', 'Femenino', 'Otro'] })
  @IsString()
  @IsEnum(['Masculino', 'Femenino', 'Otro'])
  gender: string;

  @ApiProperty({ description: 'Estado del paciente', example: 'Activo', enum: ['Activo', 'Seguimiento', 'Inactivo'], required: false })
  @IsString()
  @IsEnum(['Activo', 'Seguimiento', 'Inactivo'])
  status?: string = 'Activo';
}
