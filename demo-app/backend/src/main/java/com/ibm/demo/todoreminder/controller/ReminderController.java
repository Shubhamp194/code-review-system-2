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
package com.ibm.demo.todoreminder.controller;

import com.ibm.demo.todoreminder.dto.ReminderRequest;
import com.ibm.demo.todoreminder.dto.ReminderResponse;
import com.ibm.demo.todoreminder.service.ReminderService;
import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/**
 * REST controller for Reminder operations.
 */
@RestController
@RequestMapping("/api/reminders")
@CrossOrigin(origins = "*")
public class ReminderController {

    private static final Logger LOGGER = LoggerFactory.getLogger(ReminderController.class);

    private final ReminderService reminderService;

    @Autowired
    public ReminderController(ReminderService reminderService) {
        this.reminderService = reminderService;
    }

    /**
     * Create a new reminder.
     *
     * @param request reminder request
     * @return created reminder response
     */
    @PostMapping
    public ResponseEntity<ReminderResponse> createReminder(@Valid @RequestBody ReminderRequest request) {
        LOGGER.info("REST request to create reminder");
        ReminderResponse response = reminderService.createReminder(request);
        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }

    /**
     * Get all reminders.
     *
     * @return list of reminders
     */
    @GetMapping
    public ResponseEntity<List<ReminderResponse>> getAllReminders() {
        LOGGER.info("REST request to get all reminders");
        List<ReminderResponse> reminders = reminderService.getAllReminders();
        return ResponseEntity.ok(reminders);
    }

    /**
     * Get reminders for a specific todo.
     *
     * @param todoId todo id
     * @return list of reminders
     */
    @GetMapping("/todo/{todoId}")
    public ResponseEntity<List<ReminderResponse>> getRemindersByTodoId(@PathVariable Long todoId) {
        LOGGER.info("REST request to get reminders for todo id: {}", todoId);
        List<ReminderResponse> reminders = reminderService.getRemindersByTodoId(todoId);
        return ResponseEntity.ok(reminders);
    }

    /**
     * Get reminder by id.
     *
     * @param id reminder id
     * @return reminder response
     */
    @GetMapping("/{id}")
    public ResponseEntity<ReminderResponse> getReminderById(@PathVariable Long id) {
        LOGGER.info("REST request to get reminder with id: {}", id);
        ReminderResponse response = reminderService.getReminderById(id);
        return ResponseEntity.ok(response);
    }

    /**
     * Mark reminder as sent.
     *
     * @param id reminder id
     * @return updated reminder response
     */
    @PutMapping("/{id}/sent")
    public ResponseEntity<ReminderResponse> markReminderAsSent(@PathVariable Long id) {
        LOGGER.info("REST request to mark reminder as sent with id: {}", id);
        ReminderResponse response = reminderService.markReminderAsSent(id);
        return ResponseEntity.ok(response);
    }

    /**
     * Delete reminder.
     *
     * @param id reminder id
     * @return no content response
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteReminder(@PathVariable Long id) {
        LOGGER.info("REST request to delete reminder with id: {}", id);
        reminderService.deleteReminder(id);
        return ResponseEntity.noContent().build();
    }
}

// Made with Bob
