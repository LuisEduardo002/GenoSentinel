package com.genosentinel.microservicioauth.dto.tumortypes;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

/**
 * DTO para crear un tipo de tumor en el microservicio de Clínica (NestJS).
 * Mapea campos del DTO CreateTumorTypeDto de NestJS.
 */
@Data
public class CreateTumorTypeInDto {

    @JsonProperty("name")
    @NotBlank(message = "El nombre del tipo de tumor es obligatorio")
    @Size(max = 100, message = "El nombre no puede exceder 100 caracteres")
    private String name;

    @JsonProperty("systemAffected")
    @NotBlank(message = "El sistema afectado es obligatorio")
    @Size(max = 100, message = "El sistema afectado no puede exceder 100 caracteres")
    private String systemAffected;

    @JsonProperty("description")
    private String description;
}
