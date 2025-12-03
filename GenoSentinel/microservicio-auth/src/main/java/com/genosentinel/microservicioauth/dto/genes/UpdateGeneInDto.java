package com.genosentinel.microservicioauth.dto.genes;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

import javax.validation.constraints.Size;

/**
 * DTO para actualizar un gen existente en el microservicio de Genómica.
 * Mapea campos del serializer GeneUpdateSerializer de Django.
 */
@Data
public class UpdateGeneInDto {

    @JsonProperty("full_name")
    @Size(max = 255, message = "El nombre completo no puede exceder 255 caracteres")
    private String fullName;

    @JsonProperty("function_summary")
    private String functionSummary;
}
