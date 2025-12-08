package com.genosentinel.microservicioauth.dto.variants;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.Data;

/**
 * DTO para actualizar una variante genética en el microservicio de Genómica.
 * Mapea campos del serializer GeneticVariantUpdateSerializer de Django.
 */
@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
public class UpdateGeneticVariantInDto {

    @JsonProperty("reference_base")
    @Size(max = 100, message = "La base de referencia no puede exceder 100 caracteres")
    private String referenceBase;

    @JsonProperty("alternate_base")
    @Size(max = 100, message = "La base alternativa no puede exceder 100 caracteres")
    private String alternateBase;

    @JsonProperty("impact")
    @Pattern(
        regexp = "MISSENSE|FRAMESHIFT|NONSENSE|SILENT|SPLICE_SITE",
        message = "El impacto debe ser MISSENSE, FRAMESHIFT, NONSENSE, SILENT o SPLICE_SITE"
    )
    private String impact;
}
