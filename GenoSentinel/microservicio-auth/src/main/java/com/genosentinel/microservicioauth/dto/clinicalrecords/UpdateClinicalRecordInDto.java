package com.genosentinel.microservicioauth.dto.clinicalrecords;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

import javax.validation.constraints.Size;

/**
 * DTO para actualizar un registro clínico en el microservicio de Clínica
 * (NestJS).
 * Mapea campos del DTO UpdateClinicalRecordDto de NestJS.
 */
@Data
public class UpdateClinicalRecordInDto {

    @JsonProperty("diagnosisDate")
    private String diagnosisDate; // ISO date string

    @JsonProperty("stage")
    @Size(max = 10, message = "El estadio no puede exceder 10 caracteres")
    private String stage;

    @JsonProperty("treatmentProtocol")
    private String treatmentProtocol;

    @JsonProperty("notes")
    private String notes;
}
