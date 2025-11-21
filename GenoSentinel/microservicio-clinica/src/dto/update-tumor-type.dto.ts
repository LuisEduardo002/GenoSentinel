import { PartialType } from '@nestjs/swagger';
import { CreateTumorTypeDto } from './create-tumor-type.dto';

export class UpdateTumorTypeDto extends PartialType(CreateTumorTypeDto) {}
