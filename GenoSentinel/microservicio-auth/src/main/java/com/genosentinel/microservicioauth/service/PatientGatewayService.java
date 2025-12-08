package com.genosentinel.microservicioauth.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.genosentinel.microservicioauth.dto.PatientCreateRequestDto;
import com.genosentinel.microservicioauth.dto.PatientUpdateRequestDto;
import com.genosentinel.microservicioauth.exceptions.MicroserviceException;
import lombok.RequiredArgsConstructor;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.HttpServerErrorException;
import org.springframework.web.client.RestTemplate;

import java.util.List;

/**
 * Servicio Gateway para gestionar pacientes en el microservicio de Clínica
 * (NestJS).
 */
@Service
@RequiredArgsConstructor
public class PatientGatewayService {

    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper = new ObjectMapper();

    private String getClinicaUrl() {
        return System.getenv().getOrDefault("CLINICA_BASE_URL", "http://localhost:3001");
    }

    /**
     * Obtiene todos los pacientes, opcionalmente filtrados por status.
     */
    public Object getPatients(String status) {
        // En NestJS el controlador está definido como @Controller("patients")
        // y este método corresponde a GET /patients
        String url = getClinicaUrl() + "/patients";
        if (status != null && !status.isEmpty()) {
            url = url + "?status=" + status;
        }

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
     * Obtiene un paciente por su ID.
     */
    public Object getPatientById(String id) {
        // Método findOne -> GET /patients/get/:id
        String url = getClinicaUrl() + "/patients/get/" + id;

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
     * Crea un nuevo paciente.
     */
    public Object createPatient(PatientCreateRequestDto createDto) {
        // Método create -> POST /patients/create
        String url = getClinicaUrl() + "/patients/create";

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
     * Actualiza un paciente.
     */
    public Object updatePatient(String id, PatientUpdateRequestDto updateDto) {
        // Método update -> PATCH /patients/update/:id
        String url = getClinicaUrl() + "/patients/update/" + id;

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
     * Desactiva un paciente.
     */
    public Object deactivatePatient(String id) {
        // Método deactivate -> PATCH /patients/deactivate/:id
        String url = getClinicaUrl() + "/patients/deactivate/" + id;

        try {
            ResponseEntity<Object> response = restTemplate.exchange(
                    url, HttpMethod.PATCH, null, Object.class);
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
     * Elimina un paciente.
     */
    public void deletePatient(String id) {
        // Método remove -> DELETE /patients/delete/:id
        String url = getClinicaUrl() + "/patients/delete/" + id;

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
