package com.genosentinel.microservicioauth.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.genosentinel.microservicioauth.dto.reports.CreatePatientReportInDto;
import com.genosentinel.microservicioauth.dto.reports.UpdatePatientReportInDto;
import com.genosentinel.microservicioauth.exceptions.MicroserviceGenomicaException;
import lombok.RequiredArgsConstructor;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.HttpServerErrorException;
import org.springframework.web.client.RestTemplate;

/**
 * Servicio Gateway para gestionar reportes de variantes de pacientes en el
 * microservicio de Genómica.
 */
@Service
@RequiredArgsConstructor
public class PatientReportGatewayService {

    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper = new ObjectMapper();

    private String getGenomicaUrl() {
        return System.getenv().getOrDefault("GENOMICA_BASE_URL", "http://localhost:8000");
    }

    /**
     * Obtiene todos los reportes.
     */
    public Object getAllReports() {
        String url = getGenomicaUrl() + "/api/patient-reports/";

        try {
            ResponseEntity<Object> response = restTemplate.exchange(
                    url, HttpMethod.GET, null, Object.class);
            return response.getBody();

        } catch (HttpClientErrorException | HttpServerErrorException e) {
            throw new MicroserviceGenomicaException(
                    HttpStatus.valueOf(e.getStatusCode().value()),
                    e.getResponseBodyAsString());
        } catch (Exception e) {
            throw new MicroserviceGenomicaException(
                    HttpStatus.SERVICE_UNAVAILABLE,
                    "No se pudo conectar con el microservicio de Genómica");
        }
    }

    /**
     * Obtiene un reporte por su ID.
     */
    public Object getReportById(String id) {
        String url = getGenomicaUrl() + "/api/patient-reports/" + id + "/";

        try {
            ResponseEntity<Object> response = restTemplate.exchange(
                    url, HttpMethod.GET, null, Object.class);
            return response.getBody();

        } catch (HttpClientErrorException | HttpServerErrorException e) {
            throw new MicroserviceGenomicaException(
                    HttpStatus.valueOf(e.getStatusCode().value()),
                    e.getResponseBodyAsString());
        } catch (Exception e) {
            throw new MicroserviceGenomicaException(
                    HttpStatus.SERVICE_UNAVAILABLE,
                    "No se pudo conectar con el microservicio de Genómica");
        }
    }

    /**
     * Obtiene todos los reportes de un paciente.
     */
    public Object getReportsByPatient(String patientId) {
        String url = getGenomicaUrl() + "/api/patient-reports/patient/" + patientId + "/";

        try {
            ResponseEntity<Object> response = restTemplate.exchange(
                    url, HttpMethod.GET, null, Object.class);
            return response.getBody();

        } catch (HttpClientErrorException | HttpServerErrorException e) {
            throw new MicroserviceGenomicaException(
                    HttpStatus.valueOf(e.getStatusCode().value()),
                    e.getResponseBodyAsString());
        } catch (Exception e) {
            throw new MicroserviceGenomicaException(
                    HttpStatus.SERVICE_UNAVAILABLE,
                    "No se pudo conectar con el microservicio de Genómica");
        }
    }

    /**
     * Obtiene el resumen de un paciente (integración clínica + genómica).
     */
    public Object getPatientSummary(String patientId) {
        String url = getGenomicaUrl() + "/api/patient-reports/summary/" + patientId + "/";

        try {
            ResponseEntity<Object> response = restTemplate.exchange(
                    url, HttpMethod.GET, null, Object.class);
            return response.getBody();

        } catch (HttpClientErrorException | HttpServerErrorException e) {
            throw new MicroserviceGenomicaException(
                    HttpStatus.valueOf(e.getStatusCode().value()),
                    e.getResponseBodyAsString());
        } catch (Exception e) {
            throw new MicroserviceGenomicaException(
                    HttpStatus.SERVICE_UNAVAILABLE,
                    "No se pudo conectar con el microservicio de Genómica");
        }
    }

    /**
     * Obtiene estadísticas de un paciente.
     */
    public Object getPatientStatistics(String patientId) {
        String url = getGenomicaUrl() + "/api/patient-reports/patient/" + patientId + "/statistics/";

        try {
            ResponseEntity<Object> response = restTemplate.exchange(
                    url, HttpMethod.GET, null, Object.class);
            return response.getBody();

        } catch (HttpClientErrorException | HttpServerErrorException e) {
            throw new MicroserviceGenomicaException(
                    HttpStatus.valueOf(e.getStatusCode().value()),
                    e.getResponseBodyAsString());
        } catch (Exception e) {
            throw new MicroserviceGenomicaException(
                    HttpStatus.SERVICE_UNAVAILABLE,
                    "No se pudo conectar con el microservicio de Genómica");
        }
    }

    /**
     * Crea un nuevo reporte.
     */
    public Object createReport(CreatePatientReportInDto createDto) {
        String url = getGenomicaUrl() + "/api/patient-reports/";

        try {
            String jsonBody = objectMapper.writeValueAsString(createDto);

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<String> request = new HttpEntity<>(jsonBody, headers);

            ResponseEntity<Object> response = restTemplate.exchange(
                    url, HttpMethod.POST, request, Object.class);
            return response.getBody();

        } catch (HttpClientErrorException | HttpServerErrorException e) {
            throw new MicroserviceGenomicaException(
                    HttpStatus.valueOf(e.getStatusCode().value()),
                    e.getResponseBodyAsString());
        } catch (Exception e) {
            throw new MicroserviceGenomicaException(
                    HttpStatus.SERVICE_UNAVAILABLE,
                    "No se pudo conectar con el microservicio de Genómica: " + e.getMessage());
        }
    }

    /**
     * Actualiza un reporte (PUT completo).
     */
    public Object updateReport(String id, UpdatePatientReportInDto updateDto) {
        String url = getGenomicaUrl() + "/api/patient-reports/" + id + "/";

        try {
            String jsonBody = objectMapper.writeValueAsString(updateDto);

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<String> request = new HttpEntity<>(jsonBody, headers);

            ResponseEntity<Object> response = restTemplate.exchange(
                    url, HttpMethod.PUT, request, Object.class);
            return response.getBody();

        } catch (HttpClientErrorException | HttpServerErrorException e) {
            throw new MicroserviceGenomicaException(
                    HttpStatus.valueOf(e.getStatusCode().value()),
                    e.getResponseBodyAsString());
        } catch (Exception e) {
            throw new MicroserviceGenomicaException(
                    HttpStatus.SERVICE_UNAVAILABLE,
                    "No se pudo conectar con el microservicio de Genómica: " + e.getMessage());
        }
    }

    /**
     * Actualiza parcialmente un reporte (PATCH).
     */
    public Object patchReport(String id, UpdatePatientReportInDto patchDto) {
        String url = getGenomicaUrl() + "/api/patient-reports/" + id + "/";

        try {
            String jsonBody = objectMapper.writeValueAsString(patchDto);

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<String> request = new HttpEntity<>(jsonBody, headers);

            ResponseEntity<Object> response = restTemplate.exchange(
                    url, HttpMethod.PATCH, request, Object.class);
            return response.getBody();

        } catch (HttpClientErrorException | HttpServerErrorException e) {
            throw new MicroserviceGenomicaException(
                    HttpStatus.valueOf(e.getStatusCode().value()),
                    e.getResponseBodyAsString());
        } catch (Exception e) {
            throw new MicroserviceGenomicaException(
                    HttpStatus.SERVICE_UNAVAILABLE,
                    "No se pudo conectar con el microservicio de Genómica: " + e.getMessage());
        }
    }

    /**
     * Elimina un reporte.
     */
    public void deleteReport(String id) {
        String url = getGenomicaUrl() + "/api/patient-reports/" + id + "/";

        try {
            restTemplate.exchange(url, HttpMethod.DELETE, null, Void.class);

        } catch (HttpClientErrorException | HttpServerErrorException e) {
            throw new MicroserviceGenomicaException(
                    HttpStatus.valueOf(e.getStatusCode().value()),
                    e.getResponseBodyAsString());
        } catch (Exception e) {
            throw new MicroserviceGenomicaException(
                    HttpStatus.SERVICE_UNAVAILABLE,
                    "No se pudo conectar con el microservicio de Genómica");
        }
    }

    /**
     * Obtiene estadísticas generales de reportes.
     */
    public Object getGeneralStatistics() {
        String url = getGenomicaUrl() + "/api/patient-reports/statistics/";

        try {
            ResponseEntity<Object> response = restTemplate.exchange(
                    url, HttpMethod.GET, null, Object.class);
            return response.getBody();

        } catch (HttpClientErrorException | HttpServerErrorException e) {
            throw new MicroserviceGenomicaException(
                    HttpStatus.valueOf(e.getStatusCode().value()),
                    e.getResponseBodyAsString());
        } catch (Exception e) {
            throw new MicroserviceGenomicaException(
                    HttpStatus.SERVICE_UNAVAILABLE,
                    "No se pudo conectar con el microservicio de Genómica");
        }
    }
}
