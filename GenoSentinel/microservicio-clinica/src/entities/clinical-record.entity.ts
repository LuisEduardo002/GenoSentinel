import { Entity, PrimaryGeneratedColumn, Column, ManyToOne, JoinColumn, CreateDateColumn, UpdateDateColumn } from 'typeorm';
import { Patient } from './patient.entity';
import { TumorType } from './tumor-type.entity';

@Entity('clinical_records')
export class ClinicalRecord {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ name: 'patient_id' })
  patientId: string;

  @Column({ name: 'tumor_type_id' })
  tumorTypeId: number;

  @Column({ name: 'diagnosis_date', type: 'date' })
  diagnosisDate: Date;

  @Column({ length: 10 })
  stage: string;

  @Column({ name: 'treatment_protocol', type: 'text' })
  treatmentProtocol: string;

  @Column({ type: 'text', nullable: true })
  notes: string;

  @ManyToOne(() => Patient, patient => patient.clinicalRecords)
  @JoinColumn({ name: 'patient_id' })
  patient: Patient;

  @ManyToOne(() => TumorType, tumorType => tumorType.clinicalRecords)
  @JoinColumn({ name: 'tumor_type_id' })
  tumorType: TumorType;

  @CreateDateColumn({ name: 'created_at' })
  createdAt: Date;

  @UpdateDateColumn({ name: 'updated_at' })
  updatedAt: Date;
}
