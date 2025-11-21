import { IsString, IsNotEmpty, MaxLength, IsOptional } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class CreateTumorTypeDto {
  @ApiProperty({ description: 'Nombre del tipo de tumor', example: 'Cáncer de Mama' })
  @IsString()
  @IsNotEmpty()
  @MaxLength(100)
  name: string;

  @ApiProperty({ description: 'Sistema afectado', example: 'Glándulas' })
  @IsString()
  @IsNotEmpty()
  @MaxLength(100)
  systemAffected: string;

  @ApiProperty({ description: 'Descripción del tipo de tumor', example: 'Tumor maligno que se desarrolla en el tejido mamario', required: false })
  @IsString()
  @IsOptional()
  description?: string;
}
