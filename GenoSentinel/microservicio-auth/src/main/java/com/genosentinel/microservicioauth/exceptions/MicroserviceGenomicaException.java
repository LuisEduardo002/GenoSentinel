package com.genosentinel.microservicioauth.exceptions;

import lombok.Getter;
import org.springframework.http.HttpStatus;

/**
 * Excepción personalizada para errores del microservicio de Genómica (Django).
 * Preserva el código HTTP original y el mensaje de error del microservicio.
 */
@Getter
public class MicroserviceGenomicaException extends RuntimeException {
    private final HttpStatus status;
    private final String message;

    public MicroserviceGenomicaException(HttpStatus status, String message) {
        super(message);
        this.status = status;
        this.message = message;
    }
}
