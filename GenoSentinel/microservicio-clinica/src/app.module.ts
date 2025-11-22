import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';
import { PatientModule } from './modules/patient.module';
import { TumorTypeModule } from './modules/tumor-type.module';
import { ClinicalRecordModule } from './modules/clinical-record.module';
import { HealthController } from './controllers/health.controller';
import { DatabaseService } from './database/database.service';
import { Patient } from './entities/patient.entity';
import { TumorType } from './entities/tumor-type.entity';
import { ClinicalRecord } from './entities/clinical-record.entity';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
    }),
    TypeOrmModule.forRoot({
      type: 'mysql',
      host: process.env.DB_HOST || 'localhost',
      port: parseInt(process.env.DB_PORT) || 3306,
      username: process.env.DB_USERNAME || 'root',
      password: process.env.DB_PASSWORD || 'password',
      database: process.env.DB_DATABASE || 'genosentinel_clinica',
      entities: [Patient, TumorType, ClinicalRecord],
      synchronize: process.env.NODE_ENV === 'development',
      logging: process.env.NODE_ENV === 'development',
    }),
    TypeOrmModule.forFeature([Patient, TumorType, ClinicalRecord]),
    PatientModule,
    TumorTypeModule,
    ClinicalRecordModule,
  ],
  controllers: [HealthController],
  providers: [DatabaseService],
})
export class AppModule {}
