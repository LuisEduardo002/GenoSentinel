package com.genosentinel.microservicioauth.controller;

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import com.genosentinel.microservicioauth.service.JwtService;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/gateway")
public class GatewayController 
{
    private final RestTemplate restTemplate;
    private final JwtService jwtService;

    private final String clinicaBaseUrl;
    private final String genomicaBaseUrl;

    public GatewayController(RestTemplate restTemplate, JwtService jwtService)
    {
        this.restTemplate = restTemplate;
        this.jwtService = jwtService;

        this.clinicaBaseUrl = System.getenv().getOrDefault("CLINICA_BASE_URL", "http://localhost:3001");
        this.genomicaBaseUrl = System.getenv().getOrDefault("GENOMICA_BASE_URL", "http://localhost:8000");
    }

    @GetMapping("/health")
    public ResponseEntity<?> health() 
    {
        Map<String, String> body = new HashMap<>();
        body.put("status", "OK");
        body.put("service", "gateway-auth");
        return ResponseEntity.ok(body);
    }

    @GetMapping("/patients/{patientId}/summary")
    public ResponseEntity<?> patientSummary(
            @PathVariable("patientId") String patientId,
            @RequestHeader(value = "Authorization", required = false) String authorization
    ) {
        if (!isAuthorized(authorization)) 
        {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body("Token no proporcionado o inválido");

        }
        // Ahora el resumen clínico + genómico lo construye Genómica.
        // El gateway solo reenvía la petición autenticada.
        String summaryUrl = genomicaBaseUrl + "/api/patient-reports/summary/" + patientId + "/";
        ResponseEntity<Object> summaryResponse = restTemplate.getForEntity(summaryUrl, Object.class);
        return ResponseEntity.status(summaryResponse.getStatusCode()).body(summaryResponse.getBody());
    }

    private boolean isAuthorized(String authorizationHeader) {
        if (authorizationHeader == null || !authorizationHeader.startsWith("Bearer ")) {
            return false;
        }
        String token = authorizationHeader.substring(7);
        return jwtService.isTokenValid(token);
    }
}