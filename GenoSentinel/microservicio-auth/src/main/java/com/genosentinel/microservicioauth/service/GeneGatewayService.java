package com.genosentinel.microservicioauth.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.genosentinel.microservicioauth.dto.genes.CreateGeneInDto;
import com.genosentinel.microservicioauth.dto.genes.UpdateGeneInDto;
import com.genosentinel.microservicioauth.exceptions.MicroserviceGenomicaException;
import lombok.RequiredArgsConstructor;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.HttpServerErrorException;
import org.springframework.web.client.RestTemplate;

/**
 * Servicio Gateway para gestionar genes en el microservicio de Genómica.
 * Maneja la comunicación HTTP y el manejo robusto de errores.
 */
@Service
@RequiredArgsConstructor
public class GeneGatewayService {

    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper = new ObjectMapper();

    private String getGenomicaUrl() {
        return System.getenv().getOrDefault("GENOMICA_BASE_URL", "http://localhost:8000");
    }

    /**
     * Obtiene todos los genes del microservicio de Genómica.
     */
    public Object getAllGenes() {
        String url = getGenomicaUrl() + "/api/genes/";

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
     * Obtiene un gen por su ID.
     */
    public Object getGeneById(String id) {
        String url = getGenomicaUrl() + "/api/genes/" + id + "/";

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
     * Busca genes por símbolo.
     */
    public Object searchGeneBySymbol(String symbol) {
        // En el microservicio de Genómica la búsqueda se hace sobre el endpoint de lista
        // usando el parámetro de query "search" (no existe /api/genes/search/).
        String url = getGenomicaUrl() + "/api/genes/?search=" + symbol;

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
     * Crea un nuevo gen.
     */
    public Object createGene(CreateGeneInDto createDto) {
        String url = getGenomicaUrl() + "/api/genes/";

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
     * Actualiza un gen existente (PUT completo).
     */
    public Object updateGene(String id, UpdateGeneInDto updateDto) {
        String url = getGenomicaUrl() + "/api/genes/" + id + "/";

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
     * Actualiza parcialmente un gen (PATCH).
     */
    public Object patchGene(String id, UpdateGeneInDto patchDto) {
        String url = getGenomicaUrl() + "/api/genes/" + id + "/";

        try {
            String jsonBody = objectMapper.writeValueAsString(patchDto);

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<String> request = new HttpEntity<>(jsonBody, headers);

            // El backend de Genómica usa el mismo serializer de actualización
            // para PUT y PATCH, aceptando actualizaciones parciales. Además,
            // el cliente HTTP actual puede no soportar correctamente PATCH,
            // por lo que aquí enviamos un PUT interno.
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
     * Elimina un gen.
     */
    public void deleteGene(String id) {
        String url = getGenomicaUrl() + "/api/genes/" + id + "/";

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
     * Obtiene estadísticas de genes.
     */
    public Object getGeneStatistics() {
        String url = getGenomicaUrl() + "/api/genes/statistics/";

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
