package com.genosentinel.microservicioauth.dto.variants;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;
import javax.validation.constraints.Size;
import java.util.UUID;

/**
 * DTO para crear una variante genética en el microservicio de Genómica.
 * Mapea campos del serializer GeneticVariantCreateSerializer de Django.
 */
@Data
public class CreateGeneticVariantInDto {

    @JsonProperty("gene_id")
    @NotNull(message = "El ID del gen es obligatorio")
    private UUID geneId;

    @JsonProperty("chromosome")
    @NotBlank(message = "El cromosoma es obligatorio")
    @Size(max = 10, message = "El cromosoma no puede exceder 10 caracteres")
    private String chromosome;

    @JsonProperty("position")
    @NotNull(message = "La posición es obligatoria")
    private Long position;

    @JsonProperty("reference_base")
    @NotBlank(message = "La base de referencia es obligatoria")
    @Size(max = 100, message = "La base de referencia no puede exceder 100 caracteres")
    private String referenceBase;

    @JsonProperty("alternate_base")
    @NotBlank(message = "La base alternativa es obligatoria")
    @Size(max = 100, message = "La base alternativa no puede exceder 100 caracteres")
    private String alternateBase;

    @JsonProperty("impact")
    @NotBlank(message = "El impacto es obligatorio")
    @Pattern(regexp = "HIGH|MODERATE|LOW|MODIFIER", message = "El impacto debe ser HIGH, MODERATE, LOW o MODIFIER")
    private String impact;
}
