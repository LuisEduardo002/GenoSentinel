package com.genosentinel.microservicioauth.exceptions;

import lombok.Getter;
import org.springframework.http.HttpStatus;

/**
 * Excepción personalizada para errores del microservicio de Clínica (NestJS).
 * Preserva el código HTTP original y el mensaje de error del microservicio.
 */
@Getter
public class MicroserviceException extends RuntimeException {
    private final HttpStatus status;
    private final String message;

    public MicroserviceException(HttpStatus status, String message) {
        super(message);
        this.status = status;
        this.message = message;
    }
}
