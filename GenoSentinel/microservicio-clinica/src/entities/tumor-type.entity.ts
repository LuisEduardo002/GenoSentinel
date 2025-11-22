import { Entity, PrimaryGeneratedColumn, Column, OneToMany, CreateDateColumn, UpdateDateColumn } from 'typeorm';
import { ClinicalRecord } from './clinical-record.entity';

@Entity('tumor_types')
export class TumorType {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ length: 100 })
  name: string;

  @Column({ name: 'system_affected', length: 100 })
  systemAffected: string;

  @Column({ type: 'text', nullable: true })
  description: string;

  @OneToMany(() => ClinicalRecord, clinicalRecord => clinicalRecord.tumorType)
  clinicalRecords: ClinicalRecord[];

  @CreateDateColumn({ name: 'created_at' })
  createdAt: Date;

  @UpdateDateColumn({ name: 'updated_at' })
  updatedAt: Date;
}
