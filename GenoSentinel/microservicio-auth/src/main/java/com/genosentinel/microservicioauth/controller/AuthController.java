package com.genosentinel.microservicioauth.controller;

import com.genosentinel.microservicioauth.dto.LoginRequest;
import com.genosentinel.microservicioauth.dto.LoginResponse;
import com.genosentinel.microservicioauth.service.JwtService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/auth")
public class AuthController {

    private static final String VALID_USERNAME = "admin";
    private static final String VALID_PASSWORD = "admin";

    private final JwtService jwtService;

    public AuthController(JwtService jwtService) {
        this.jwtService = jwtService;
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginRequest request) {
        if (VALID_USERNAME.equals(request.getUsername()) && VALID_PASSWORD.equals(request.getPassword())) {
            String token = jwtService.generateToken(request.getUsername());
            LoginResponse response = new LoginResponse(token, "Bearer", 3600L);
            return ResponseEntity.ok(response);
        }

        return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                .body("Credenciales inválidas");
    }
}
