import { Injectable, NotFoundException, BadRequestException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { TumorType } from '../entities/tumor-type.entity';
import { CreateTumorTypeDto } from '../dto/create-tumor-type.dto';
import { UpdateTumorTypeDto } from '../dto/update-tumor-type.dto';

@Injectable()
export class TumorTypeService {
  constructor(
    @InjectRepository(TumorType)
    private tumorTypeRepository: Repository<TumorType>,
  ) {}

  async create(createTumorTypeDto: CreateTumorTypeDto): Promise<TumorType> {
    // Validar unicidad por nombre de tipo de tumor
    const existing = await this.tumorTypeRepository.findOne({
      where: { name: createTumorTypeDto.name },
    });

    if (existing) {
      throw new BadRequestException(
        `Ya existe un tipo de tumor con el nombre ${createTumorTypeDto.name}`,
      );
    }

    const tumorType = this.tumorTypeRepository.create(createTumorTypeDto);
    return await this.tumorTypeRepository.save(tumorType);
  }

  async findAll(): Promise<TumorType[]> {
    return await this.tumorTypeRepository.find({
      relations: ['clinicalRecords'],
      order: { name: 'ASC' },
    });
  }

  async findOne(id: number): Promise<TumorType> {
    const tumorType = await this.tumorTypeRepository.findOne({
      where: { id },
      relations: ['clinicalRecords', 'clinicalRecords.patient'],
    });

    if (!tumorType) {
      throw new NotFoundException(`Tipo de tumor con ID ${id} no encontrado`);
    }

    return tumorType;
  }

  async update(id: number, updateTumorTypeDto: UpdateTumorTypeDto): Promise<TumorType> {
    const tumorType = await this.findOne(id);
    Object.assign(tumorType, updateTumorTypeDto);
    return await this.tumorTypeRepository.save(tumorType);
  }

  async remove(id: number): Promise<void> {
    const tumorType = await this.findOne(id);
    await this.tumorTypeRepository.remove(tumorType);
  }

  async findBySystem(systemAffected: string): Promise<TumorType[]> {
    return await this.tumorTypeRepository.find({
      where: { systemAffected },
      relations: ['clinicalRecords'],
      order: { name: 'ASC' },
    });
  }
}
