package com.genosentinel.microservicioauth.controller;

import com.genosentinel.microservicioauth.dto.genes.CreateGeneInDto;
import com.genosentinel.microservicioauth.dto.genes.UpdateGeneInDto;
import com.genosentinel.microservicioauth.dto.variants.CreateGeneticVariantInDto;
import com.genosentinel.microservicioauth.dto.variants.UpdateGeneticVariantInDto;
import com.genosentinel.microservicioauth.dto.reports.CreatePatientReportInDto;
import com.genosentinel.microservicioauth.dto.reports.UpdatePatientReportInDto;
import com.genosentinel.microservicioauth.dto.clinicalrecords.CreateClinicalRecordInDto;
import com.genosentinel.microservicioauth.dto.clinicalrecords.UpdateClinicalRecordInDto;
import com.genosentinel.microservicioauth.dto.tumortypes.CreateTumorTypeInDto;
import com.genosentinel.microservicioauth.dto.tumortypes.UpdateTumorTypeInDto;
import com.genosentinel.microservicioauth.dto.PatientCreateRequestDto;
import com.genosentinel.microservicioauth.dto.PatientUpdateRequestDto;
import com.genosentinel.microservicioauth.service.*;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;

/**
 * Controlador Gateway que actúa como punto de entrada único para todos los
 * microservicios.
 * Delega las operaciones a servicios especializados y documenta la API con
 * Swagger.
 */
@RestController
@RequestMapping("/gateway")
@Tag(name = "Gateway", description = "API Gateway para microservicios de GenoSentinel")
public class GatewayController {

    private final GeneGatewayService geneGatewayService;
    private final GeneticVariantGatewayService variantGatewayService;
    private final PatientReportGatewayService reportGatewayService;
    private final ClinicalRecordGatewayService clinicalRecordGatewayService;
    private final PatientGatewayService patientGatewayService;
    private final TumorTypeGatewayService tumorTypeGatewayService;

    public GatewayController(
            GeneGatewayService geneGatewayService,
            GeneticVariantGatewayService variantGatewayService,
            PatientReportGatewayService reportGatewayService,
            ClinicalRecordGatewayService clinicalRecordGatewayService,
            PatientGatewayService patientGatewayService,
            TumorTypeGatewayService tumorTypeGatewayService) {

        this.geneGatewayService = geneGatewayService;
        this.variantGatewayService = variantGatewayService;
        this.reportGatewayService = reportGatewayService;
        this.clinicalRecordGatewayService = clinicalRecordGatewayService;
        this.patientGatewayService = patientGatewayService;
        this.tumorTypeGatewayService = tumorTypeGatewayService;
    }


    
    // ==================== GENES ENDPOINTS ====================

    @GetMapping("/genes")
    @Operation(summary = "Listar todos los genes", description = "Obtiene la lista completa de genes del microservicio de Genómica")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "Lista de genes obtenida exitosamente"),
            @ApiResponse(responseCode = "503", description = "Servicio de Genómica no disponible")
    })
    public ResponseEntity<?> getAllGenes() {
        return ResponseEntity.ok(geneGatewayService.getAllGenes());
    }

    @GetMapping("/genes/{id}")
    @Operation(summary = "Obtener gen por ID", description = "Obtiene los detalles de un gen específico")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "Gen encontrado"),
            @ApiResponse(responseCode = "404", description = "Gen no encontrado"),
            @ApiResponse(responseCode = "503", description = "Servicio de Genómica no disponible")
    })
    public ResponseEntity<?> getGeneById(@PathVariable String id) {
        return ResponseEntity.ok(geneGatewayService.getGeneById(id));
    }

    @GetMapping("/genes/search")
    @Operation(summary = "Buscar genes por símbolo", description = "Busca genes que coincidan con el símbolo proporcionado")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "Búsqueda completada"),
            @ApiResponse(responseCode = "503", description = "Servicio de Genómica no disponible")
    })
    public ResponseEntity<?> searchGenes(@RequestParam String symbol) {
        return ResponseEntity.ok(geneGatewayService.searchGeneBySymbol(symbol));
    }

    @PostMapping("/genes")
    @Operation(summary = "Crear nuevo gen", description = "Crea un nuevo gen en el sistema")
    @ApiResponses({
            @ApiResponse(responseCode = "201", description = "Gen creado exitosamente"),
            @ApiResponse(responseCode = "400", description = "Datos inválidos"),
            @ApiResponse(responseCode = "409", description = "El gen ya existe"),
            @ApiResponse(responseCode = "503", description = "Servicio de Genómica no disponible")
    })
    public ResponseEntity<?> createGene(@Valid @RequestBody CreateGeneInDto createDto) {
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(geneGatewayService.createGene(createDto));
    }

    @PutMapping("/genes/{id}")
    @Operation(summary = "Actualizar gen (PUT)", description = "Actualiza completamente un gen existente")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "Gen actualizado exitosamente"),
            @ApiResponse(responseCode = "400", description = "Datos inválidos"),
            @ApiResponse(responseCode = "404", description = "Gen no encontrado"),
            @ApiResponse(responseCode = "503", description = "Servicio de Genómica no disponible")
    })
    public ResponseEntity<?> updateGene(
            @PathVariable String id,
            @Valid @RequestBody UpdateGeneInDto updateDto) {
        return ResponseEntity.ok(geneGatewayService.updateGene(id, updateDto));
    }

    @PatchMapping("/genes/{id}")
    @Operation(summary = "Actualizar gen parcialmente (PATCH)", description = "Actualiza parcialmente un gen existente")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "Gen actualizado exitosamente"),
            @ApiResponse(responseCode = "400", description = "Datos inválidos"),
            @ApiResponse(responseCode = "404", description = "Gen no encontrado"),
            @ApiResponse(responseCode = "503", description = "Servicio de Genómica no disponible")
    })
    public ResponseEntity<?> patchGene(
            @PathVariable String id,
            @Valid @RequestBody UpdateGeneInDto patchDto) {
        return ResponseEntity.ok(geneGatewayService.patchGene(id, patchDto));
    }

    @DeleteMapping("/genes/{id}")
    @Operation(summary = "Eliminar gen", description = "Elimina un gen del sistema")
    @ApiResponses({
            @ApiResponse(responseCode = "204", description = "Gen eliminado exitosamente"),
            @ApiResponse(responseCode = "404", description = "Gen no encontrado"),
            @ApiResponse(responseCode = "503", description = "Servicio de Genómica no disponible")
    })
    public ResponseEntity<Void> deleteGene(@PathVariable String id) {
        geneGatewayService.deleteGene(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/genes/statistics")
    @Operation(summary = "Estadísticas de genes", description = "Obtiene estadísticas generales de genes")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "Estadísticas obtenidas"),
            @ApiResponse(responseCode = "503", description = "Servicio de Genómica no disponible")
    })
    public ResponseEntity<?> getGeneStatistics() {
        return ResponseEntity.ok(geneGatewayService.getGeneStatistics());
    }

    // ==================== VARIANTS ENDPOINTS ====================

    @GetMapping("/variants")
    @Operation(summary = "Listar todas las variantes", description = "Obtiene la lista completa de variantes genéticas")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "Lista de variantes obtenida"),
            @ApiResponse(responseCode = "503", description = "Servicio de Genómica no disponible")
    })
    public ResponseEntity<?> getAllVariants() {
        return ResponseEntity.ok(variantGatewayService.getAllVariants());
    }

    @GetMapping("/variants/{id}")
    @Operation(summary = "Obtener variante por ID", description = "Obtiene los detalles de una variante específica")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "Variante encontrada"),
            @ApiResponse(responseCode = "404", description = "Variante no encontrada"),
            @ApiResponse(responseCode = "503", description = "Servicio de Genómica no disponible")
    })
    public ResponseEntity<?> getVariantById(@PathVariable String id) {
        return ResponseEntity.ok(variantGatewayService.getVariantById(id));
    }

    @GetMapping("/variants/by-gene/{geneSymbol}")
    @Operation(summary = "Variantes por gen", description = "Obtiene todas las variantes de un gen específico")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "Variantes obtenidas"),
            @ApiResponse(responseCode = "503", description = "Servicio de Genómica no disponible")
    })
    public ResponseEntity<?> getVariantsByGene(@PathVariable String geneSymbol) {
        return ResponseEntity.ok(variantGatewayService.getVariantsByGene(geneSymbol));
    }

    @GetMapping("/variants/by-chromosome/{chromosome}")
    @Operation(summary = "Variantes por cromosoma", description = "Obtiene todas las variantes de un cromosoma específico")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "Variantes obtenidas"),
            @ApiResponse(responseCode = "503", description = "Servicio de Genómica no disponible")
    })
    public ResponseEntity<?> getVariantsByChromosome(@PathVariable String chromosome) {
        return ResponseEntity.ok(variantGatewayService.getVariantsByChromosome(chromosome));
    }

    @PostMapping("/variants")
    @Operation(summary = "Crear variante", description = "Crea una nueva variante genética")
    @ApiResponses({
            @ApiResponse(responseCode = "201", description = "Variante creada"),
            @ApiResponse(responseCode = "400", description = "Datos inválidos"),
            @ApiResponse(responseCode = "404", description = "Gen no encontrado"),
            @ApiResponse(responseCode = "503", description = "Servicio de Genómica no disponible")
    })
    public ResponseEntity<?> createVariant(@Valid @RequestBody CreateGeneticVariantInDto createDto) {
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(variantGatewayService.createVariant(createDto));
    }

    @PutMapping("/variants/{id}")
    @Operation(summary = "Actualizar variante (PUT)", description = "Actualiza completamente una variante")
    public ResponseEntity<?> updateVariant(
            @PathVariable String id,
            @Valid @RequestBody UpdateGeneticVariantInDto updateDto) {
        return ResponseEntity.ok(variantGatewayService.updateVariant(id, updateDto));
    }

    @PatchMapping("/variants/{id}")
    @Operation(summary = "Actualizar variante (PATCH)", description = "Actualiza parcialmente una variante")
    public ResponseEntity<?> patchVariant(
            @PathVariable String id,
            @Valid @RequestBody UpdateGeneticVariantInDto patchDto) {
        return ResponseEntity.ok(variantGatewayService.patchVariant(id, patchDto));
    }

    @DeleteMapping("/variants/{id}")
    @Operation(summary = "Eliminar variante", description = "Elimina una variante del sistema")
    public ResponseEntity<Void> deleteVariant(@PathVariable String id) {
        variantGatewayService.deleteVariant(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/variants/statistics")
    @Operation(summary = "Estadísticas de variantes", description = "Obtiene estadísticas generales de variantes")
    public ResponseEntity<?> getVariantStatistics() {
        return ResponseEntity.ok(variantGatewayService.getVariantStatistics());
    }

    // ==================== PATIENT REPORTS ENDPOINTS ====================

    @GetMapping("/patient-reports")
    @Operation(summary = "Listar reportes", description = "Obtiene todos los reportes de variantes de pacientes")
    public ResponseEntity<?> getAllReports() {
        return ResponseEntity.ok(reportGatewayService.getAllReports());
    }

    @GetMapping("/patient-reports/{id}")
    @Operation(summary = "Obtener reporte por ID", description = "Obtiene un reporte específico")
    public ResponseEntity<?> getReportById(@PathVariable String id) {
        return ResponseEntity.ok(reportGatewayService.getReportById(id));
    }

    @GetMapping("/patient-reports/patient/{patientId}")
    @Operation(summary = "Reportes por paciente", description = "Obtiene todos los reportes de un paciente")
    public ResponseEntity<?> getReportsByPatient(@PathVariable String patientId) {
        return ResponseEntity.ok(reportGatewayService.getReportsByPatient(patientId));
    }

    @GetMapping("/patient-reports/patient/{patientId}/summary")
    @Operation(summary = "Resumen del paciente", description = "Obtiene el resumen clínico y genómico de un paciente")
    public ResponseEntity<?> getPatientSummary(@PathVariable String patientId) {
        return ResponseEntity.ok(reportGatewayService.getPatientSummary(patientId));
    }

    @GetMapping("/patient-reports/patient/{patientId}/statistics")
    @Operation(summary = "Estadísticas del paciente", description = "Obtiene estadísticas de variantes del paciente")
    public ResponseEntity<?> getPatientStatistics(@PathVariable String patientId) {
        return ResponseEntity.ok(reportGatewayService.getPatientStatistics(patientId));
    }

    @PostMapping("/patient-reports")
    @Operation(summary = "Crear reporte", description = "Crea un nuevo reporte de variante para un paciente")
    public ResponseEntity<?> createReport(@Valid @RequestBody CreatePatientReportInDto createDto) {
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(reportGatewayService.createReport(createDto));
    }

    @PutMapping("/patient-reports/{id}")
    @Operation(summary = "Actualizar reporte (PUT)", description = "Actualiza completamente un reporte")
    public ResponseEntity<?> updateReport(
            @PathVariable String id,
            @Valid @RequestBody UpdatePatientReportInDto updateDto) {
        return ResponseEntity.ok(reportGatewayService.updateReport(id, updateDto));
    }

    @PatchMapping("/patient-reports/{id}")
    @Operation(summary = "Actualizar reporte (PATCH)", description = "Actualiza parcialmente un reporte")
    public ResponseEntity<?> patchReport(
            @PathVariable String id,
            @Valid @RequestBody UpdatePatientReportInDto patchDto) {
        return ResponseEntity.ok(reportGatewayService.patchReport(id, patchDto));
    }

    @DeleteMapping("/patient-reports/{id}")
    @Operation(summary = "Eliminar reporte", description = "Elimina un reporte")
    public ResponseEntity<Void> deleteReport(@PathVariable String id) {
        reportGatewayService.deleteReport(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/patient-reports/statistics")
    @Operation(summary = "Estadísticas generales de reportes", description = "Obtiene estadísticas generales")
    public ResponseEntity<?> getReportStatistics() {
        return ResponseEntity.ok(reportGatewayService.getGeneralStatistics());
    }

    // ==================== CLINICAL RECORDS ENDPOINTS ====================

    @GetMapping("/clinical-records")
    @Operation(summary = "Listar registros clínicos", description = "Obtiene todos los registros clínicos")
    public ResponseEntity<?> getAllClinicalRecords() {
        return ResponseEntity.ok(clinicalRecordGatewayService.getAllClinicalRecords());
    }

    @GetMapping("/clinical-records/{id}")
    @Operation(summary = "Obtener registro clínico por ID", description = "Obtiene un registro clínico específico")
    public ResponseEntity<?> getClinicalRecordById(@PathVariable Long id) {
        return ResponseEntity.ok(clinicalRecordGatewayService.getClinicalRecordById(id));
    }

    @GetMapping("/clinical-records/patient/{patientId}")
    @Operation(summary = "Registros por paciente", description = "Obtiene todos los registros clínicos de un paciente")
    public ResponseEntity<?> getClinicalRecordsByPatient(@PathVariable String patientId) {
        return ResponseEntity.ok(clinicalRecordGatewayService.getClinicalRecordsByPatient(patientId));
    }

    @PostMapping("/clinical-records")
    @Operation(summary = "Crear registro clínico", description = "Crea un nuevo registro clínico")
    public ResponseEntity<?> createClinicalRecord(@Valid @RequestBody CreateClinicalRecordInDto createDto) {
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(clinicalRecordGatewayService.createClinicalRecord(createDto));
    }

    @PatchMapping("/clinical-records/{id}")
    @Operation(summary = "Actualizar registro clínico", description = "Actualiza un registro clínico")
    public ResponseEntity<?> updateClinicalRecord(
            @PathVariable Long id,
            @Valid @RequestBody UpdateClinicalRecordInDto updateDto) {
        return ResponseEntity.ok(clinicalRecordGatewayService.updateClinicalRecord(id, updateDto));
    }

    @DeleteMapping("/clinical-records/{id}")
    @Operation(summary = "Eliminar registro clínico", description = "Elimina un registro clínico")
    public ResponseEntity<Void> deleteClinicalRecord(@PathVariable Long id) {
        clinicalRecordGatewayService.deleteClinicalRecord(id);
        return ResponseEntity.noContent().build();
    }

    // ==================== PATIENTS ENDPOINTS ====================

    @GetMapping("/patients")
    @Operation(summary = "Listar pacientes", description = "Obtiene todos los pacientes, opcionalmente filtrados por status")
    public ResponseEntity<?> getPatients(@RequestParam(required = false) String status) {
        return ResponseEntity.ok(patientGatewayService.getPatients(status));
    }

    @GetMapping("/patients/{id}")
    @Operation(summary = "Obtener paciente por ID", description = "Obtiene un paciente específico")
    public ResponseEntity<?> getPatientById(@PathVariable String id) {
        return ResponseEntity.ok(patientGatewayService.getPatientById(id));
    }

    @PostMapping("/patients")
    @Operation(summary = "Crear paciente", description = "Crea un nuevo paciente")
    public ResponseEntity<?> createPatient(@Valid @RequestBody PatientCreateRequestDto createDto) {
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(patientGatewayService.createPatient(createDto));
    }

    @PatchMapping("/patients/{id}")
    @Operation(summary = "Actualizar paciente", description = "Actualiza los datos de un paciente")
    public ResponseEntity<?> updatePatient(
            @PathVariable String id,
            @Valid @RequestBody PatientUpdateRequestDto updateDto) {
        return ResponseEntity.ok(patientGatewayService.updatePatient(id, updateDto));
    }

    @PatchMapping("/patients/{id}/deactivate")
    @Operation(summary = "Desactivar paciente", description = "Desactiva un paciente cambiando su status")
    public ResponseEntity<?> deactivatePatient(@PathVariable String id) {
        return ResponseEntity.ok(patientGatewayService.deactivatePatient(id));
    }

    @DeleteMapping("/patients/{id}")
    @Operation(summary = "Eliminar paciente", description = "Elimina un paciente del sistema")
    public ResponseEntity<Void> deletePatient(@PathVariable String id) {
        patientGatewayService.deletePatient(id);
        return ResponseEntity.noContent().build();
    }

    // ==================== TUMOR TYPES ENDPOINTS ====================

    @GetMapping("/tumor-types")
    @Operation(summary = "Listar tipos de tumor", description = "Obtiene todos los tipos de tumor")
    public ResponseEntity<?> getAllTumorTypes() {
        return ResponseEntity.ok(tumorTypeGatewayService.getAllTumorTypes());
    }

    @GetMapping("/tumor-types/{id}")
    @Operation(summary = "Obtener tipo de tumor por ID", description = "Obtiene un tipo de tumor específico")
    public ResponseEntity<?> getTumorTypeById(@PathVariable Long id) {
        return ResponseEntity.ok(tumorTypeGatewayService.getTumorTypeById(id));
    }

    @PostMapping("/tumor-types")
    @Operation(summary = "Crear tipo de tumor", description = "Crea un nuevo tipo de tumor")
    public ResponseEntity<?> createTumorType(@Valid @RequestBody CreateTumorTypeInDto createDto) {
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(tumorTypeGatewayService.createTumorType(createDto));
    }

    @PatchMapping("/tumor-types/{id}")
    @Operation(summary = "Actualizar tipo de tumor", description = "Actualiza un tipo de tumor")
    public ResponseEntity<?> updateTumorType(
            @PathVariable Long id,
            @Valid @RequestBody UpdateTumorTypeInDto updateDto) {
        return ResponseEntity.ok(tumorTypeGatewayService.updateTumorType(id, updateDto));
    }

    @DeleteMapping("/tumor-types/{id}")
    @Operation(summary = "Eliminar tipo de tumor", description = "Elimina un tipo de tumor")
    public ResponseEntity<Void> deleteTumorType(@PathVariable Long id) {
        tumorTypeGatewayService.deleteTumorType(id);
        return ResponseEntity.noContent().build();
    }

    // ==================== HEALTH ENDPOINT ====================

    @GetMapping("/health")
    @Operation(summary = "Health check", description = "Verifica el estado del Gateway")
    public ResponseEntity<?> health() {
        return ResponseEntity.ok(java.util.Map.of(
                "status", "OK",
                "service", "gateway-auth",
                "timestamp", java.time.LocalDateTime.now()));
    }
}