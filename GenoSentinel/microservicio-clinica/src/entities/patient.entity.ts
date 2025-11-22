import { Entity, PrimaryGeneratedColumn, Column, OneToMany, CreateDateColumn, UpdateDateColumn } from 'typeorm';
import { ClinicalRecord } from './clinical-record.entity';

@Entity('patients')
export class Patient {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ name: 'first_name', length: 100 })
  firstName: string;

  @Column({ name: 'last_name', length: 100 })
  lastName: string;

  @Column({ name: 'birth_date', type: 'date' })
  birthDate: Date;

  @Column({ length: 10 })
  gender: string;

  @Column({ length: 20, default: 'Activo' })
  status: string;

  @OneToMany(() => ClinicalRecord, clinicalRecord => clinicalRecord.patient)
  clinicalRecords: ClinicalRecord[];

  @CreateDateColumn({ name: 'created_at' })
  createdAt: Date;

  @UpdateDateColumn({ name: 'updated_at' })
  updatedAt: Date;
}
