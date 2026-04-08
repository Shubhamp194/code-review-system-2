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
package com.ibm.demo.todoreminder.service;

import com.ibm.demo.todoreminder.dto.ReminderRequest;
import com.ibm.demo.todoreminder.dto.ReminderResponse;
import com.ibm.demo.todoreminder.exception.ResourceNotFoundException;
import com.ibm.demo.todoreminder.model.Reminder;
import com.ibm.demo.todoreminder.model.Todo;
import com.ibm.demo.todoreminder.repository.ReminderRepository;
import com.ibm.demo.todoreminder.repository.TodoRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Service class for Reminder business logic.
 */
@Service
@Transactional
public class ReminderService {

    private static final Logger LOGGER = LoggerFactory.getLogger(ReminderService.class);

    private final ReminderRepository reminderRepository;
    private final TodoRepository todoRepository;

    @Autowired
    public ReminderService(ReminderRepository reminderRepository, TodoRepository todoRepository) {
        this.reminderRepository = reminderRepository;
        this.todoRepository = todoRepository;
    }

    /**
     * Create a new reminder.
     *
     * @param request reminder request
     * @return created reminder response
     */
    public ReminderResponse createReminder(ReminderRequest request) {
        LOGGER.info("Creating new reminder for todo id: {}", request.getTodoId());

        Todo todo = todoRepository.findById(request.getTodoId())
                .orElseThrow(() -> new ResourceNotFoundException("Todo not found with id: " + request.getTodoId()));

        Reminder reminder = new Reminder();
        reminder.setTodo(todo);
        reminder.setReminderTime(request.getReminderTime());
        reminder.setMessage(request.getMessage());
        reminder.setSent(false);
        reminder.setCreatedAt(LocalDateTime.now());

        Reminder savedReminder = reminderRepository.save(reminder);
        LOGGER.info("Reminder created successfully with id: {}", savedReminder.getId());

        return mapToResponse(savedReminder);
    }

    /**
     * Get all reminders.
     *
     * @return list of reminder responses
     */
    @Transactional(readOnly = true)
    public List<ReminderResponse> getAllReminders() {
        LOGGER.info("Fetching all reminders");
        List<Reminder> reminders = reminderRepository.findAllByOrderByReminderTimeAsc();
        return reminders.stream()
                .map(this::mapToResponse)
                .collect(Collectors.toList());
    }

    /**
     * Get reminders for a specific todo.
     *
     * @param todoId todo id
     * @return list of reminder responses
     */
    @Transactional(readOnly = true)
    public List<ReminderResponse> getRemindersByTodoId(Long todoId) {
        LOGGER.info("Fetching reminders for todo id: {}", todoId);
        List<Reminder> reminders = reminderRepository.findByTodoId(todoId);
        return reminders.stream()
                .map(this::mapToResponse)
                .collect(Collectors.toList());
    }

    /**
     * Get reminder by id.
     *
     * @param id reminder id
     * @return reminder response
     */
    @Transactional(readOnly = true)
    public ReminderResponse getReminderById(Long id) {
        LOGGER.info("Fetching reminder with id: {}", id);
        Reminder reminder = reminderRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Reminder not found with id: " + id));
        return mapToResponse(reminder);
    }

    /**
     * Delete reminder.
     *
     * @param id reminder id
     */
    public void deleteReminder(Long id) {
        LOGGER.info("Deleting reminder with id: {}", id);

        if (!reminderRepository.existsById(id)) {
            throw new ResourceNotFoundException("Reminder not found with id: " + id);
        }

        reminderRepository.deleteById(id);
        LOGGER.info("Reminder deleted successfully with id: {}", id);
    }

    /**
     * Mark reminder as sent.
     *
     * @param id reminder id
     * @return updated reminder response
     */
    public ReminderResponse markReminderAsSent(Long id) {
        LOGGER.info("Marking reminder as sent with id: {}", id);

        Reminder reminder = reminderRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Reminder not found with id: " + id));

        reminder.setSent(true);
        reminder.setSentAt(LocalDateTime.now());

        Reminder updatedReminder = reminderRepository.save(reminder);
        LOGGER.info("Reminder marked as sent with id: {}", id);

        return mapToResponse(updatedReminder);
    }

    /**
     * Map Reminder entity to ReminderResponse DTO.
     *
     * @param reminder reminder entity
     * @return reminder response
     */
    private ReminderResponse mapToResponse(Reminder reminder) {
        ReminderResponse response = new ReminderResponse();
        response.setId(reminder.getId());
        response.setTodoId(reminder.getTodo().getId());
        response.setTodoTitle(reminder.getTodo().getTitle());
        response.setReminderTime(reminder.getReminderTime());
        response.setMessage(reminder.getMessage());
        response.setSent(reminder.isSent());
        response.setCreatedAt(reminder.getCreatedAt());
        response.setSentAt(reminder.getSentAt());
        return response;
    }
}

// Made with Bob
