/*
 * Copyright IBM Corporation 2026
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package com.ibm.demo.todoreminder;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Main application class for Todo and Reminder application.
 * This class bootstraps the Spring Boot application.
 */
@SpringBootApplication
public class TodoReminderApplication {

    private static final Logger LOGGER = LoggerFactory.getLogger(TodoReminderApplication.class);

    /**
     * Main method to start the Spring Boot application.
     *
     * @param args command line arguments
     */
    public static void main(String[] args) {
        LOGGER.info("Starting Todo and Reminder Application");
        SpringApplication.run(TodoReminderApplication.class, args);
        LOGGER.info("Todo and Reminder Application started successfully");
    }
}

// Made with Bob
