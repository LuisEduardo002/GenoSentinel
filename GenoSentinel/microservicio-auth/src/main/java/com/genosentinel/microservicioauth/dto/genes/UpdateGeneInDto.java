package com.genosentinel.microservicioauth.dto.genes;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.Size;
import lombok.Data;

/**
 * DTO para actualizar un gen existente en el microservicio de Genómica.
 * Mapea campos del serializer GeneUpdateSerializer de Django.
 */
@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
public class UpdateGeneInDto {

    @JsonProperty("symbol")
    @Size(max = 50, message = "El símbolo no puede exceder 50 caracteres")
    private String symbol;

    @JsonProperty("full_name")
    @Size(max = 255, message = "El nombre completo no puede exceder 255 caracteres")
    private String fullName;

    @JsonProperty("function_summary")
    private String functionSummary;
}
