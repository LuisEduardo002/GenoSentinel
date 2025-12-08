package com.genosentinel.microservicioauth.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.genosentinel.microservicioauth.dto.variants.CreateGeneticVariantInDto;
import com.genosentinel.microservicioauth.dto.variants.UpdateGeneticVariantInDto;
import com.genosentinel.microservicioauth.exceptions.MicroserviceGenomicaException;
import lombok.RequiredArgsConstructor;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.HttpServerErrorException;
import org.springframework.web.client.RestTemplate;

/**
 * * Servicio Gateway para gestionar variantes genéticas en el microservicio de
 * Genómica.
 */
@Service
@RequiredArgsConstructor
public class GeneticVariantGatewayService {

    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper = new ObjectMapper();

    private String getGenomicaUrl() {
        return System.getenv().getOrDefault("GENOMICA_BASE_URL", "http://localhost:8000");
    }

    /**
     * Obtiene todas las variantes genéticas.
     */
    public Object getAllVariants() {
        String url = getGenomicaUrl() + "/api/variants/";

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
     * Obtiene una variante por su ID.
     */
    public Object getVariantById(String id) {
        String url = getGenomicaUrl() + "/api/variants/" + id + "/";

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
     * Obtiene variantes por gen.
     */
    public Object getVariantsByGene(String geneSymbol) {
        // En el microservicio de Genómica la acción se llama by_gene y recibe
        // el símbolo del gen como query param gene_symbol.
        String url = getGenomicaUrl() + "/api/variants/by_gene/?gene_symbol=" + geneSymbol;

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
     * Obtiene variantes por cromosoma.
     */
    public Object getVariantsByChromosome(String chromosome) {
        // En el microservicio de Genómica la acción se llama by_chromosome y
        // recibe el cromosoma como query param "chr" (ej: chr17).
        String url = getGenomicaUrl() + "/api/variants/by_chromosome/?chr=" + chromosome;

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
     * Crea una nueva variante genética.
     */
    public Object createVariant(CreateGeneticVariantInDto createDto) {
        String url = getGenomicaUrl() + "/api/variants/";

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
     * Actualiza una variante genética (PUT completo).
     */
    public Object updateVariant(String id, UpdateGeneticVariantInDto updateDto) {
        String url = getGenomicaUrl() + "/api/variants/" + id + "/";

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
     * Actualiza parcialmente una variante (PATCH).
     */
    public Object patchVariant(String id, UpdateGeneticVariantInDto patchDto) {
        String url = getGenomicaUrl() + "/api/variants/" + id + "/";

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
     * Elimina una variante.
     */
    public void deleteVariant(String id) {
        String url = getGenomicaUrl() + "/api/variants/" + id + "/";

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
     * Obtiene estadísticas de variantes.
     */
    public Object getVariantStatistics() {
        String url = getGenomicaUrl() + "/api/variants/statistics/";

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
