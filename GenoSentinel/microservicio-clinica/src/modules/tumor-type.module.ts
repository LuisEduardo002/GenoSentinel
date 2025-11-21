import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { TumorType } from '../entities/tumor-type.entity';
import { TumorTypeService } from '../services/tumor-type.service';
import { TumorTypeController } from '../controllers/tumor-type.controller';

@Module({
  imports: [TypeOrmModule.forFeature([TumorType])],
  controllers: [TumorTypeController],
  providers: [TumorTypeService],
  exports: [TumorTypeService],
})
export class TumorTypeModule {}
