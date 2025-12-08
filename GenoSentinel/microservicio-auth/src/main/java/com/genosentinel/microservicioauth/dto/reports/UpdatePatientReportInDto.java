package com.genosentinel.microservicioauth.dto.reports;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

import jakarta.validation.constraints.DecimalMax;
import jakarta.validation.constraints.DecimalMin;
import java.math.BigDecimal;
import java.time.LocalDate;

/**
 * DTO para actualizar un reporte de variante de paciente en el microservicio de
 * Genómica.
 * Mapea campos del serializer PatientVariantReportUpdateSerializer de Django.
 */
@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
public class UpdatePatientReportInDto {

    @JsonProperty("detection_date")
    private LocalDate detectionDate;

    @JsonProperty("allele_frequency")
    @DecimalMin(value = "0.0", message = "La frecuencia alélica debe estar entre 0 y 1")
    @DecimalMax(value = "1.0", message = "La frecuencia alélica debe estar entre 0 y 1")
    private BigDecimal alleleFrequency;
}
