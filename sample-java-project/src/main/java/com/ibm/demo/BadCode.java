package com.ibm.demo;

import java.util.*;
import java.sql.*;
import java.io.*;

public class BadCode {
    
    // Violation: Public field
    public String username;
    
    // Violation: Static mutable variable
    static List<String> cache = new ArrayList<>();
    
    // Violation: Hardcoded secret
    private String password = "admin123";
    private String apiKey = "sk-1234567890abcdef";
    
    // Violation: Generic variable name
    public void processData() {
        String temp = "test";
        Object obj = new Object();
        
        // Violation: System.out.println
        System.out.println("Processing data");
        
        // Violation: TODO comment
        // TODO: Implement proper error handling
        
        // Violation: Hardcoded URL
        String apiUrl = "https://api.example.com/v1/users";
        
        // Violation: Hardcoded path
        String logFile = "/tmp/app.log";
    }
    
    // Violation: Method name not lowerCamelCase
    public void ProcessUser(String userId) {
        try {
            // Violation: SQL concatenation
            String query = "SELECT * FROM users WHERE id = " + userId;
            
            // Violation: Catching generic Exception
        } catch (Exception e) {
            // Violation: printStackTrace
            e.printStackTrace();
            
            // Violation: Empty catch block would be here
        }
    }
    
    // Violation: No logging in catch
    public void riskyOperation() {
        try {
            throw new Exception("test");
        } catch (Exception e) {
            // No logging
        }
    }
    
    // Violation: String concatenation in loop
    public String buildString(List<String> items) {
        String result = "";
        for (String item : items) {
            result += item;
        }
        return result;
    }
    
    // Violation: == for string comparison
    public boolean checkName(String name) {
        if (name == "admin") {
            return true;
        }
        return false;
    }
    
    // Violation: Boolean naming
    boolean active = true;
    boolean valid = false;
    
    // Violation: Debug flag
    private static final boolean DEBUG = true;
    
    // Violation: System.exit
    public void shutdown() {
        System.exit(0);
    }
    
    // Violation: Thread.sleep
    public void wait(int seconds) throws InterruptedException {
        Thread.sleep(seconds * 1000);
    }
    
    // Violation: Runtime.exec with variable
    public void executeCommand(String cmd) throws IOException {
        Runtime.getRuntime().exec(cmd);
    }
    
    // Violation: Logging sensitive data
    public void login(String user, String pass) {
        System.out.println("Login attempt with password: " + pass);
    }
    
    // Violation: String concatenation in logging
    public void logMessage(String msg) {
        // Assuming log is defined
        // log.info("Message: " + msg);
    }
    
    // Violation: Throwing generic Exception
    public void doSomething() throws Exception {
        throw new Exception("Generic exception");
    }
    
    // Violation: Line too long (if this line exceeds 120 characters it would be flagged as a violation for being too long and should be split)
    
    // Violation: Trailing whitespace on next line
    public void trailingSpace() {    
        String test = "value";    
    }
}

// Commented out code block - violation
// public class OldCode {
//     public void oldMethod() {
//         System.out.println("old");
//     }
// }
// More commented code
// Even more
// And more
// Still more

// Made with Bob
