package com.genosentinel.microservicioauth.dto.tumortypes;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.Size;
import lombok.Data;

/**
 * DTO para actualizar un tipo de tumor en el microservicio de Clínica (NestJS).
 * Mapea campos del DTO UpdateTumorTypeDto de NestJS.
 */
@Data
public class UpdateTumorTypeInDto {

    @JsonProperty("name")
    @Size(max = 100, message = "El nombre no puede exceder 100 caracteres")
    private String name;

    @JsonProperty("systemAffected")
    @Size(max = 100, message = "El sistema afectado no puede exceder 100 caracteres")
    private String systemAffected;

    @JsonProperty("description")
    private String description;
}
