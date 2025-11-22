import { Injectable, OnModuleInit } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { TumorType } from '../entities/tumor-type.entity';
import { Patient } from '../entities/patient.entity';
import { ClinicalRecord } from '../entities/clinical-record.entity';
import { tumorTypesSeed } from './seeds/tumor-types.seed';
import { patientsSeed } from './seeds/patients.seed';

@Injectable()
export class DatabaseService implements OnModuleInit {
  constructor(
    @InjectRepository(TumorType)
    private tumorTypeRepository: Repository<TumorType>,
    @InjectRepository(Patient)
    private patientRepository: Repository<Patient>,
    @InjectRepository(ClinicalRecord)
    private clinicalRecordRepository: Repository<ClinicalRecord>,
  ) {}

  async onModuleInit() {
    if (process.env.NODE_ENV === 'development') {
      await this.seedDatabase();
    }
  }

  private async seedDatabase() {
    // Seed tumor types
    const tumorTypeCount = await this.tumorTypeRepository.count();
    if (tumorTypeCount === 0) {
      console.log('🌱 Seeding tumor types...');
      for (const tumorTypeData of tumorTypesSeed) {
        const tumorType = this.tumorTypeRepository.create(tumorTypeData);
        await this.tumorTypeRepository.save(tumorType);
      }
      console.log('✅ Tumor types seeded successfully');
    }

    // Seed patients
    const patientCount = await this.patientRepository.count();
    if (patientCount === 0) {
      console.log('🌱 Seeding patients...');
      for (const patientData of patientsSeed) {
        const patient = this.patientRepository.create({
          ...patientData,
          birthDate: new Date(patientData.birthDate),
        });
        await this.patientRepository.save(patient);
      }
      console.log('✅ Patients seeded successfully');
    }

    // Seed clinical records
    const clinicalRecordCount = await this.clinicalRecordRepository.count();
    if (clinicalRecordCount === 0) {
      console.log('🌱 Seeding clinical records...');
      const patients = await this.patientRepository.find();
      const tumorTypes = await this.tumorTypeRepository.find();

      if (patients.length > 0 && tumorTypes.length > 0) {
        // Create sample clinical records
        const sampleRecords = [
          {
            patientId: patients[0].id,
            tumorTypeId: tumorTypes[0].id,
            diagnosisDate: new Date('2024-01-15'),
            stage: 'IIA',
            treatmentProtocol: 'Quimioterapia con doxorubicina y ciclofosfamida',
            notes: 'Paciente responde bien al tratamiento inicial'
          },
          {
            patientId: patients[1].id,
            tumorTypeId: tumorTypes[1].id,
            diagnosisDate: new Date('2023-11-20'),
            stage: 'IIIB',
            treatmentProtocol: 'Radioterapia combinada con quimioterapia',
            notes: 'Seguimiento cada 3 meses'
          },
          {
            patientId: patients[2].id,
            tumorTypeId: tumorTypes[2].id,
            diagnosisDate: new Date('2024-02-10'),
            stage: 'I',
            treatmentProtocol: 'Resección quirúrgica',
            notes: 'Cirugía exitosa, pronóstico favorable'
          }
        ];

        for (const recordData of sampleRecords) {
          const clinicalRecord = this.clinicalRecordRepository.create(recordData);
          await this.clinicalRecordRepository.save(clinicalRecord);
        }
        console.log('✅ Clinical records seeded successfully');
      }
    }

    console.log('🎉 Database seeding completed!');
  }
}
