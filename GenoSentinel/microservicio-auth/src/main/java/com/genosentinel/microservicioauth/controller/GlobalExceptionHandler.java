package com.genosentinel.microservicioauth.controller;

import com.genosentinel.microservicioauth.exceptions.MicroserviceException;
import com.genosentinel.microservicioauth.exceptions.MicroserviceGenomicaException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.time.LocalDateTime;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Manejador global de excepciones para el Gateway.
 * Captura excepciones de los microservicios y las transforma en respuestas HTTP
 * apropiadas.
 */
@RestControllerAdvice
public class GlobalExceptionHandler {

    /**
     * Maneja excepciones del microservicio de Clínica (NestJS).
     */
    @ExceptionHandler(MicroserviceException.class)
    public ResponseEntity<Object> handleMicroserviceException(MicroserviceException ex) {
        Map<String, Object> body = new LinkedHashMap<>();
        body.put("timestamp", LocalDateTime.now());
        body.put("status", ex.getStatus().value());
        body.put("error", ex.getStatus().getReasonPhrase());
        body.put("message", ex.getMessage());
        body.put("microservice", "clinica");

        return new ResponseEntity<>(body, ex.getStatus());
    }

    /**
     * Maneja excepciones del microservicio de Genómica (Django).
     */
    @ExceptionHandler(MicroserviceGenomicaException.class)
    public ResponseEntity<Object> handleMicroserviceGenomicaException(MicroserviceGenomicaException ex) {
        Map<String, Object> body = new LinkedHashMap<>();
        body.put("timestamp", LocalDateTime.now());
        body.put("status", ex.getStatus().value());
        body.put("error", ex.getStatus().getReasonPhrase());
        body.put("message", ex.getMessage());
        body.put("microservice", "genomica");

        return new ResponseEntity<>(body, ex.getStatus());
    }

    /**
     * Maneja excepciones genéricas no capturadas.
     */
    @ExceptionHandler(Exception.class)
    public ResponseEntity<Object> handleGenericException(Exception ex) {
        Map<String, Object> body = new LinkedHashMap<>();
        body.put("timestamp", LocalDateTime.now());
        body.put("status", HttpStatus.INTERNAL_SERVER_ERROR.value());
        body.put("error", "Internal Server Error");
        body.put("message", "Error interno del servidor: " + ex.getMessage());

        return new ResponseEntity<>(body, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
