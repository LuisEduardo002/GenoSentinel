package com.genosentinel.microservicioauth.dto.clinicalrecords;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import java.util.UUID;

/**
 * DTO para crear un registro clínico en el microservicio de Clínica (NestJS).
 * Mapea campos del DTO CreateClinicalRecordDto de NestJS.
 */
@Data
public class CreateClinicalRecordInDto {

    @JsonProperty("patientId")
    @NotNull(message = "El ID del paciente es obligatorio")
    private UUID patientId;

    @JsonProperty("tumorTypeId")
    @NotNull(message = "El ID del tipo de tumor es obligatorio")
    private Long tumorTypeId;

    @JsonProperty("diagnosisDate")
    @NotBlank(message = "La fecha de diagnóstico es obligatoria")
    private String diagnosisDate; // ISO date string

    @JsonProperty("stage")
    @NotBlank(message = "El estadio del tumor es obligatorio")
    @Size(max = 10, message = "El estadio no puede exceder 10 caracteres")
    private String stage;

    @JsonProperty("treatmentProtocol")
    @NotBlank(message = "El protocolo de tratamiento es obligatorio")
    private String treatmentProtocol;

    @JsonProperty("notes")
    private String notes;
}
