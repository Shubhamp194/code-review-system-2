// Missing IBM license header - CRITICAL VIOLATION

package com.ibm.demo;

import java.util.*;
import java.io.*;
import java.sql.*;

public class TestPRFile {
    
    // Hardcoded credentials - CRITICAL VIOLATION
    private static String password = "mySecretPassword123";
    private static String apiKey = "sk-1234567890abcdef";
    
    // Public field - MEDIUM VIOLATION
    public String publicData = "exposed";
    
    // Static mutable variable - MEDIUM VIOLATION
    private static List<String> cache = new ArrayList<>();
    
    public void processData(String input) {
        // System.out.println usage - HIGH VIOLATION
        System.out.println("Processing: " + input);
        
        // Empty catch block - HIGH VIOLATION
        try {
            int result = Integer.parseInt(input);
        } catch (Exception e) {
            // Empty catch - no logging
        }
        
        // String concatenation in loop - MEDIUM VIOLATION
        String output = "";
        for (int i = 0; i < 10; i++) {
            output += "Item " + i;
        }
        
        // Using == for string comparison - MEDIUM VIOLATION
        if (input == "test") {
            doSomething();
        }
        
        // TODO comment - HIGH VIOLATION
        // TODO: Fix this later
        
        // Hardcoded URL - HIGH VIOLATION
        String endpoint = "https://api.example.com/data";
        
        // SQL concatenation - CRITICAL VIOLATION
        String query = "SELECT * FROM users WHERE id = " + input;
        
        // Magic number - LOW VIOLATION
        if (input.length() > 12345) {
            return;
        }
    }
    
    // Method name not lowerCamelCase - NAMING VIOLATION
    public void Process_Data() {
        // Empty method - LOW VIOLATION
    }
    
    // Generic exception catch - HIGH VIOLATION
    public void riskyOperation() {
        try {
            // Some risky code
            Thread.sleep(1000);
        } catch (Exception e) {
            e.printStackTrace(); // printStackTrace usage - HIGH VIOLATION
        }
    }
    
    // Poor variable naming - NAMING VIOLATION
    public void calculate() {
        int x = 10;
        String temp = "data";
        Object obj = new Object();
    }
    
    private void doSomething() {
        // Commented out code - HIGH VIOLATION
        // String oldCode = "This was removed";
        // processOldWay(oldCode);
        
        // Debug flag - MEDIUM VIOLATION
        boolean debug = true;
        if (debug) {
            System.err.println("Debug mode"); // System.err usage - HIGH VIOLATION
        }
    }
}

// Made with Bob