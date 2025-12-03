package com.genosentinel.microservicioauth.controller;

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import com.genosentinel.microservicioauth.service.JwtService;
import com.genosentinel.microservicioauth.dto.PatientCreateRequestDto;
import com.genosentinel.microservicioauth.dto.PatientUpdateRequestDto;
import com.genosentinel.microservicioauth.dto.PatientResponseDto;
import com.genosentinel.microservicioauth.dto.TumorTypeCreateRequestDto;
import com.genosentinel.microservicioauth.dto.TumorTypeUpdateRequestDto;
import com.genosentinel.microservicioauth.dto.TumorTypeResponseDto;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.springframework.core.ParameterizedTypeReference;

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

    @PostMapping("/patients")
    public ResponseEntity<PatientResponseDto> createPatient(@RequestBody PatientCreateRequestDto request) {
        String url = clinicaBaseUrl + "/patients/create";
        ResponseEntity<PatientResponseDto> response = restTemplate.postForEntity(url, request, PatientResponseDto.class);
        return ResponseEntity.status(response.getStatusCode()).body(response.getBody());
    }

    @GetMapping("/patients")
    public ResponseEntity<List<PatientResponseDto>> getPatients(@RequestParam(value = "status", required = false) String status) {
        String url = clinicaBaseUrl + "/patients";
        if (status != null && !status.isEmpty()) {
            url = url + "?status=" + status;
        }

        ResponseEntity<List<PatientResponseDto>> response = restTemplate.exchange(
                url,
                HttpMethod.GET,
                null,
                new ParameterizedTypeReference<List<PatientResponseDto>>() {}
        );

        return ResponseEntity.status(response.getStatusCode()).body(response.getBody());
    }

    @GetMapping("/patients/{id}")
    public ResponseEntity<PatientResponseDto> getPatientById(@PathVariable("id") String id) {
        String url = clinicaBaseUrl + "/patients/get/" + id;
        ResponseEntity<PatientResponseDto> response = restTemplate.getForEntity(url, PatientResponseDto.class);
        return ResponseEntity.status(response.getStatusCode()).body(response.getBody());
    }

    @PatchMapping("/patients/{id}")
    public ResponseEntity<PatientResponseDto> updatePatient(
            @PathVariable("id") String id,
            @RequestBody PatientUpdateRequestDto request
    ) {
        String url = clinicaBaseUrl + "/patients/update/" + id;
        HttpEntity<PatientUpdateRequestDto> entity = new HttpEntity<>(request);

        ResponseEntity<PatientResponseDto> response = restTemplate.exchange(
                url,
                HttpMethod.PATCH,
                entity,
                PatientResponseDto.class
        );

        return ResponseEntity.status(response.getStatusCode()).body(response.getBody());
    }

    @PatchMapping("/patients/{id}/deactivate")
    public ResponseEntity<PatientResponseDto> deactivatePatient(@PathVariable("id") String id) {
        String url = clinicaBaseUrl + "/patients/deactivate/" + id;
        ResponseEntity<PatientResponseDto> response = restTemplate.exchange(
                url,
                HttpMethod.PATCH,
                null,
                PatientResponseDto.class
        );
        return ResponseEntity.status(response.getStatusCode()).body(response.getBody());
    }

    @DeleteMapping("/patients/{id}")
    public ResponseEntity<Void> deletePatient(@PathVariable("id") String id) {
        String url = clinicaBaseUrl + "/patients/delete/" + id;
        ResponseEntity<Void> response = restTemplate.exchange(
                url,
                HttpMethod.DELETE,
                null,
                Void.class
        );
        return ResponseEntity.status(response.getStatusCode()).build();
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