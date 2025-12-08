package com.genosentinel.microservicioauth;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.http.client.HttpComponentsClientHttpRequestFactory;
import org.springframework.web.client.RestTemplate;

@SpringBootApplication
public class MicroservicioAuthApplication {

    public static void main(String[] args) {
        SpringApplication.run(MicroservicioAuthApplication.class, args);
    }

    @Bean
    public RestTemplate restTemplate() {
        // Usamos HttpComponentsClientHttpRequestFactory para soportar correctamente
        // métodos HTTP como PATCH en el RestTemplate.
        HttpComponentsClientHttpRequestFactory requestFactory = new HttpComponentsClientHttpRequestFactory();
        return new RestTemplate(requestFactory);
    }
}
