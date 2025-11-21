import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { ClinicalRecord } from '../entities/clinical-record.entity';
import { CreateClinicalRecordDto } from '../dto/create-clinical-record.dto';
import { UpdateClinicalRecordDto } from '../dto/update-clinical-record.dto';

@Injectable()
export class ClinicalRecordService {
  constructor(
    @InjectRepository(ClinicalRecord)
    private clinicalRecordRepository: Repository<ClinicalRecord>,
  ) {}

  async create(createClinicalRecordDto: CreateClinicalRecordDto): Promise<ClinicalRecord> {
    const clinicalRecord = this.clinicalRecordRepository.create({
      ...createClinicalRecordDto,
      diagnosisDate: new Date(createClinicalRecordDto.diagnosisDate),
    });
    return await this.clinicalRecordRepository.save(clinicalRecord);
  }

  async findAll(): Promise<ClinicalRecord[]> {
    return await this.clinicalRecordRepository.find({
      relations: ['patient', 'tumorType'],
      order: { diagnosisDate: 'DESC' },
    });
  }

  async findOne(id: string): Promise<ClinicalRecord> {
    const clinicalRecord = await this.clinicalRecordRepository.findOne({
      where: { id },
      relations: ['patient', 'tumorType'],
    });

    if (!clinicalRecord) {
      throw new NotFoundException(`Historia clínica con ID ${id} no encontrada`);
    }

    return clinicalRecord;
  }

  async update(id: string, updateClinicalRecordDto: UpdateClinicalRecordDto): Promise<ClinicalRecord> {
    const clinicalRecord = await this.findOne(id);
    
    const updateData = {
      ...updateClinicalRecordDto,
      ...(updateClinicalRecordDto.diagnosisDate && { diagnosisDate: new Date(updateClinicalRecordDto.diagnosisDate) }),
    };

    Object.assign(clinicalRecord, updateData);
    return await this.clinicalRecordRepository.save(clinicalRecord);
  }

  async remove(id: string): Promise<void> {
    const clinicalRecord = await this.findOne(id);
    await this.clinicalRecordRepository.remove(clinicalRecord);
  }

  async findByPatient(patientId: string): Promise<ClinicalRecord[]> {
    return await this.clinicalRecordRepository.find({
      where: { patientId },
      relations: ['tumorType'],
      order: { diagnosisDate: 'DESC' },
    });
  }

  async findByTumorType(tumorTypeId: number): Promise<ClinicalRecord[]> {
    return await this.clinicalRecordRepository.find({
      where: { tumorTypeId },
      relations: ['patient'],
      order: { diagnosisDate: 'DESC' },
    });
  }
}
