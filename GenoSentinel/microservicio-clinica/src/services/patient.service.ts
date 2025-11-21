import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Patient } from '../entities/patient.entity';
import { CreatePatientDto } from '../dto/create-patient.dto';
import { UpdatePatientDto } from '../dto/update-patient.dto';

@Injectable()
export class PatientService {
  constructor(
    @InjectRepository(Patient)
    private patientRepository: Repository<Patient>,
  ) {}

  async create(createPatientDto: CreatePatientDto): Promise<Patient> {
    const patient = this.patientRepository.create({
      ...createPatientDto,
      birthDate: new Date(createPatientDto.birthDate),
    });
    return await this.patientRepository.save(patient);
  }

  async findAll(): Promise<Patient[]> {
    return await this.patientRepository.find({
      relations: ['clinicalRecords'],
      order: { createdAt: 'DESC' },
    });
  }

  async findOne(id: string): Promise<Patient> {
    const patient = await this.patientRepository.findOne({
      where: { id },
      relations: ['clinicalRecords', 'clinicalRecords.tumorType'],
    });

    if (!patient) {
      throw new NotFoundException(`Paciente con ID ${id} no encontrado`);
    }

    return patient;
  }

  async update(id: string, updatePatientDto: UpdatePatientDto): Promise<Patient> {
    const patient = await this.findOne(id);
    
    const updateData = {
      ...updatePatientDto,
      ...(updatePatientDto.birthDate && { birthDate: new Date(updatePatientDto.birthDate) }),
    };

    Object.assign(patient, updateData);
    return await this.patientRepository.save(patient);
  }

  async remove(id: string): Promise<void> {
    const patient = await this.findOne(id);
    await this.patientRepository.remove(patient);
  }

  async deactivate(id: string): Promise<Patient> {
    const patient = await this.findOne(id);
    patient.status = 'Inactivo';
    return await this.patientRepository.save(patient);
  }

  async findByStatus(status: string): Promise<Patient[]> {
    return await this.patientRepository.find({
      where: { status },
      relations: ['clinicalRecords'],
      order: { createdAt: 'DESC' },
    });
  }
}
