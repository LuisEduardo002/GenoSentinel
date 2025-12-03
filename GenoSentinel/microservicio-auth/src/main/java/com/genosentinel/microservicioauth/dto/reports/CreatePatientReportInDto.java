package com.genosentinel.microservicioauth.dto.reports;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

import javax.validation.constraints.DecimalMax;
import javax.validation.constraints.DecimalMin;
import javax.validation.constraints.NotNull;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.UUID;

/**
 * DTO para crear un reporte de variante de paciente en el microservicio de
 * Genómica.
 * Mapea campos del serializer PatientVariantReportCreateSerializer de Django.
 */
@Data
public class CreatePatientReportInDto {

    @JsonProperty("patient_id")
    @NotNull(message = "El ID del paciente es obligatorio")
    private UUID patientId;

    @JsonProperty("variant_id")
    @NotNull(message = "El ID de la variante es obligatorio")
    private UUID variantId;

    @JsonProperty("detection_date")
    @NotNull(message = "La fecha de detección es obligatoria")
    private LocalDate detectionDate;

    @JsonProperty("allele_frequency")
    @NotNull(message = "La frecuencia alélica es obligatoria")
    @DecimalMin(value = "0.0", message = "La frecuencia alélica debe estar entre 0 y 1")
    @DecimalMax(value = "1.0", message = "La frecuencia alélica debe estar entre 0 y 1")
    private BigDecimal alleleFrequency;
}
