package com.genosentinel.microservicioauth.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.genosentinel.microservicioauth.dto.clinicalrecords.CreateClinicalRecordInDto;
import com.genosentinel.microservicioauth.dto.clinicalrecords.UpdateClinicalRecordInDto;
import com.genosentinel.microservicioauth.exceptions.MicroserviceException;
import lombok.RequiredArgsConstructor;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.HttpServerErrorException;
import org.springframework.web.client.RestTemplate;

/**
 * Servicio Gateway para gestionar registros clínicos en el microservicio de
 * Clínica (NestJS).
 */
@Service
@RequiredArgsConstructor
public class ClinicalRecordGatewayService {

    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper = new ObjectMapper();

    private String getClinicaUrl() {
        return System.getenv().getOrDefault("CLINICA_BASE_URL", "http://localhost:3001");
    }

    /**
     * Obtiene todos los registros clínicos.
     */
    public Object getAllClinicalRecords() {
        String url = getClinicaUrl() + "/genosentinel/clinica/clinical-records";

        try {
            ResponseEntity<Object> response = restTemplate.exchange(
                    url, HttpMethod.GET, null, Object.class);
            return response.getBody();

        } catch (HttpClientErrorException e) {
            throw new MicroserviceException(
                    HttpStatus.valueOf(e.getStatusCode().value()),
                    e.getResponseBodyAsString());
        } catch (HttpServerErrorException e) {
            throw new MicroserviceException(
                    HttpStatus.valueOf(e.getStatusCode().value()),
                    e.getResponseBodyAsString());
        } catch (Exception e) {
            throw new MicroserviceException(
                    HttpStatus.SERVICE_UNAVAILABLE,
                    "No se pudo conectar con el microservicio de Clínica");
        }
    }

    /**
     * Obtiene un registro clínico por su ID.
     */
    public Object getClinicalRecordById(Long id) {
        String url = getClinicaUrl() + "/genosentinel/clinica/clinical-records/" + id;

        try {
            ResponseEntity<Object> response = restTemplate.exchange(
                    url, HttpMethod.GET, null, Object.class);
            return response.getBody();

        } catch (HttpClientErrorException e) {
            throw new MicroserviceException(
                    HttpStatus.valueOf(e.getStatusCode().value()),
                    e.getResponseBodyAsString());
        } catch (HttpServerErrorException e) {
            throw new MicroserviceException(
                    HttpStatus.valueOf(e.getStatusCode().value()),
                    e.getResponseBodyAsString());
        } catch (Exception e) {
            throw new MicroserviceException(
                    HttpStatus.SERVICE_UNAVAILABLE,
                    "No se pudo conectar con el microservicio de Clínica");
        }
    }

    /**
     * Obtiene registros clínicos por ID de paciente.
     */
    public Object getClinicalRecordsByPatient(String patientId) {
        String url = getClinicaUrl() + "/genosentinel/clinica/clinical-records/patient/" + patientId;

        try {
            ResponseEntity<Object> response = restTemplate.exchange(
                    url, HttpMethod.GET, null, Object.class);
            return response.getBody();

        } catch (HttpClientErrorException e) {
            throw new MicroserviceException(
                    HttpStatus.valueOf(e.getStatusCode().value()),
                    e.getResponseBodyAsString());
        } catch (HttpServerErrorException e) {
            throw new MicroserviceException(
                    HttpStatus.valueOf(e.getStatusCode().value()),
                    e.getResponseBodyAsString());
        } catch (Exception e) {
            throw new MicroserviceException(
                    HttpStatus.SERVICE_UNAVAILABLE,
                    "No se pudo conectar con el microservicio de Clínica");
        }
    }

    /**
     * Crea un nuevo registro clínico.
     */
    public Object createClinicalRecord(CreateClinicalRecordInDto createDto) {
        String url = getClinicaUrl() + "/genosentinel/clinica/clinical-records";

        try {
            String jsonBody = objectMapper.writeValueAsString(createDto);

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<String> request = new HttpEntity<>(jsonBody, headers);

            ResponseEntity<Object> response = restTemplate.exchange(
                    url, HttpMethod.POST, request, Object.class);
            return response.getBody();

        } catch (HttpClientErrorException e) {
            throw new MicroserviceException(
                    HttpStatus.valueOf(e.getStatusCode().value()),
                    e.getResponseBodyAsString());
        } catch (HttpServerErrorException e) {
            throw new MicroserviceException(
                    HttpStatus.valueOf(e.getStatusCode().value()),
                    e.getResponseBodyAsString());
        } catch (Exception e) {
            throw new MicroserviceException(
                    HttpStatus.SERVICE_UNAVAILABLE,
                    "No se pudo conectar con el microservicio de Clínica: " + e.getMessage());
        }
    }

    /**
     * Actualiza un registro clínico.
     */
    public Object updateClinicalRecord(Long id, UpdateClinicalRecordInDto updateDto) {
        String url = getClinicaUrl() + "/genosentinel/clinica/clinical-records/" + id;

        try {
            String jsonBody = objectMapper.writeValueAsString(updateDto);

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<String> request = new HttpEntity<>(jsonBody, headers);

            ResponseEntity<Object> response = restTemplate.exchange(
                    url, HttpMethod.PATCH, request, Object.class);
            return response.getBody();

        } catch (HttpClientErrorException e) {
            throw new MicroserviceException(
                    HttpStatus.valueOf(e.getStatusCode().value()),
                    e.getResponseBodyAsString());
        } catch (HttpServerErrorException e) {
            throw new MicroserviceException(
                    HttpStatus.valueOf(e.getStatusCode().value()),
                    e.getResponseBodyAsString());
        } catch (Exception e) {
            throw new MicroserviceException(
                    HttpStatus.SERVICE_UNAVAILABLE,
                    "No se pudo conectar con el microservicio de Clínica: " + e.getMessage());
        }
    }

    /**
     * Elimina un registro clínico.
     */
    public void deleteClinicalRecord(Long id) {
        String url = getClinicaUrl() + "/genosentinel/clinica/clinical-records/" + id;

        try {
            restTemplate.exchange(url, HttpMethod.DELETE, null, Void.class);

        } catch (HttpClientErrorException e) {
            throw new MicroserviceException(
                    HttpStatus.valueOf(e.getStatusCode().value()),
                    e.getResponseBodyAsString());
        } catch (HttpServerErrorException e) {
            throw new MicroserviceException(
                    HttpStatus.valueOf(e.getStatusCode().value()),
                    e.getResponseBodyAsString());
        } catch (Exception e) {
            throw new MicroserviceException(
                    HttpStatus.SERVICE_UNAVAILABLE,
                    "No se pudo conectar con el microservicio de Clínica");
        }
    }
}
