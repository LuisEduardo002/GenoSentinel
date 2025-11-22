import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ClinicalRecord } from '../entities/clinical-record.entity';
import { ClinicalRecordService } from '../services/clinical-record.service';
import { ClinicalRecordController } from '../controllers/clinical-record.controller';

@Module({
  imports: [TypeOrmModule.forFeature([ClinicalRecord])],
  controllers: [ClinicalRecordController],
  providers: [ClinicalRecordService],
  exports: [ClinicalRecordService],
})
export class ClinicalRecordModule {}
