package com.genosentinel.microservicioauth.dto;

public class TumorTypeUpdateRequestDto {
    private String name;
    private String systemAffected;
    private String description;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getSystemAffected() {
        return systemAffected;
    }

    public void setSystemAffected(String systemAffected) {
        this.systemAffected = systemAffected;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }
}
