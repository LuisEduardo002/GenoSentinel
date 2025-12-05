package com.genosentinel.microservicioauth.dto.genes;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

/**
 * DTO para crear un nuevo gen en el microservicio de Genómica.
 * Mapea campos del serializer GeneCreateSerializer de Django.
 */
@Data
public class CreateGeneInDto {

    @JsonProperty("symbol")
    @NotBlank(message = "El símbolo del gen es obligatorio")
    @Size(max = 50, message = "El símbolo no puede exceder 50 caracteres")
    private String symbol;

    @JsonProperty("full_name")
    @NotBlank(message = "El nombre completo del gen es obligatorio")
    @Size(max = 255, message = "El nombre completo no puede exceder 255 caracteres")
    private String fullName;

    @JsonProperty("function_summary")
    @NotBlank(message = "El resumen de función es obligatorio")
    private String functionSummary;
}
