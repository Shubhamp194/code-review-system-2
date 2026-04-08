// Missing IBM license header - SEC001 violation

package com.ibm.demo.todoreminder.service;

import com.ibm.demo.todoreminder.model.*;
import com.ibm.demo.todoreminder.repository.*;
import java.util.*;

public class NotificationService {
    
    // Hardcoded secrets - SEC002 CRITICAL violations
    private String apiKey = "sk-1234567890abcdef";
    private String password = "admin123";
    
    // Public field - BP006 violation
    public String endpoint = "https://api.notification.com";
    
    // Static mutable variable - BP007 violation
    private static String config = "production";
    
    // Generic variable names - NAM005 violations
    private String temp;
    private String data;
    
    // Method name not lowerCamelCase - NAM003 violation
    public void SendNotification(String message) {
        // TODO: Implement notification sending - CQ003 violation
        System.out.println("Sending: " + message);  // CQ001 violation
        
        try {
            // SQL injection - SEC003 CRITICAL violation
            String query = "SELECT * FROM notifications WHERE message = '" + message + "'";
            
            // Command injection - SEC004 CRITICAL violation
            Runtime.getRuntime().exec("curl " + endpoint + " -d " + message);
            
            // Empty catch block - CQ004 CRITICAL violation
        } catch (Exception e) {
            
        }
        
        // String concatenation in loop - BP004 violation
        String result = "";
        for (int i = 0; i < 10; i++) {
            result = result + i;
        }
        
        // String comparison with == - BP005 violation
        if (config == "production") {
            // Logging sensitive data - SEC005 violation
            System.out.println("API Key: " + apiKey);
        }
    }
    
    // Method with printStackTrace - CQ002 violation
    public void processData() {
        try {
            // Some processing
            int x = 1 / 0;
        } catch (Exception e) {
            e.printStackTrace();  // CQ002 HIGH violation
        }
    }
    
    // Method with Thread.sleep - CQ009 violation
    public void delay() {
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            // Empty catch - CQ004 violation
        }
    }
    
    // Method with System.exit - CQ008 violation
    public void shutdown() {
        System.exit(0);
    }
    
    // Boolean not starting with is/has/should - NAM007 violation
    private boolean active;
    
    // Constant not UPPER_SNAKE_CASE - NAM004 violation
    private static final int maxRetries = 3;
    
    // Commented out code - SEC008 violation
    // public void oldMethod() {
    //     String oldData = "test";
    //     processOldData(oldData);
    // }
    
    // Multiple consecutive blank lines - FMT002 violation


    
    
    // Trailing whitespace on next line - FMT001 violation
    private String value;    
}
// Missing newline at end - FMT004 violation

// Made with Bob
