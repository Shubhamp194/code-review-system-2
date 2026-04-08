/*
 * Copyright IBM Corporation 2024
 * Licensed under the Apache License, Version 2.0
 * SPDX-License-Identifier: Apache-2.0
 */
package com.ibm.demo;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.List;
import java.util.ArrayList;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Example of good code following all rules
 */
public class GoodCode {
    
    private static final Logger log = LoggerFactory.getLogger(GoodCode.class);
    private static final String API_ENDPOINT = "api.endpoint";
    private static final int MAX_RETRIES = 3;
    
    private String username;
    private boolean isActive;
    private boolean hasPermission;
    
    public GoodCode() {
        this.username = "";
        this.isActive = false;
        this.hasPermission = false;
    }
    
    public String getUsername() {
        return username;
    }
    
    public void setUsername(String username) {
        this.username = username;
    }
    
    public boolean isActive() {
        return isActive;
    }
    
    public void setActive(boolean active) {
        isActive = active;
    }
    
    /**
     * Process user data safely
     */
    public void processUserData(String userId) {
        try {
            log.info("Processing user data for user: {}", userId);
            
            // Use PreparedStatement for SQL
            String query = "SELECT * FROM users WHERE id = ?";
            // PreparedStatement stmt = connection.prepareStatement(query);
            // stmt.setString(1, userId);
            
            log.info("User data processed successfully");
            
        } catch (IllegalArgumentException e) {
            log.error("Invalid user ID provided", e);
            throw new UserProcessingException("Failed to process user", e);
        }
    }
    
    /**
     * Build string efficiently
     */
    public String buildString(List<String> items) {
        StringBuilder result = new StringBuilder();
        for (String item : items) {
            result.append(item);
        }
        return result.toString();
    }
    
    /**
     * Compare strings correctly
     */
    public boolean checkName(String name) {
        return "admin".equals(name);
    }
    
    /**
     * Get configuration from environment
     */
    public String getApiUrl() {
        return System.getenv("API_URL");
    }
    
    /**
     * Custom exception class
     */
    public static class UserProcessingException extends RuntimeException {
        public UserProcessingException(String message, Throwable cause) {
            super(message, cause);
        }
    }
}

// Made with Bob
