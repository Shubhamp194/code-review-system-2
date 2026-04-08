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

import com.ibm.demo.todoreminder.dto.TodoRequest;
import com.ibm.demo.todoreminder.dto.TodoResponse;
import com.ibm.demo.todoreminder.exception.ResourceNotFoundException;
import com.ibm.demo.todoreminder.model.Priority;
import com.ibm.demo.todoreminder.model.Todo;
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
 * Service class for Todo business logic.
 */
@Service
@Transactional
public class TodoService {

    private static final Logger LOGGER = LoggerFactory.getLogger(TodoService.class);

    private final TodoRepository todoRepository;

    @Autowired
    public TodoService(TodoRepository todoRepository) {
        this.todoRepository = todoRepository;
    }

    /**
     * Create a new todo.
     *
     * @param request todo request
     * @return created todo response
     */
    public TodoResponse createTodo(TodoRequest request) {
        LOGGER.info("Creating new todo with title: {}", request.getTitle());

        Todo todo = new Todo();
        todo.setTitle(request.getTitle());
        todo.setDescription(request.getDescription());
        todo.setPriority(request.getPriority() != null ? request.getPriority() : Priority.MEDIUM);
        todo.setCompleted(false);
        todo.setCreatedAt(LocalDateTime.now());
        todo.setUpdatedAt(LocalDateTime.now());

        Todo savedTodo = todoRepository.save(todo);
        LOGGER.info("Todo created successfully with id: {}", savedTodo.getId());

        return mapToResponse(savedTodo);
    }

    /**
     * Get all todos.
     *
     * @return list of todo responses
     */
    @Transactional(readOnly = true)
    public List<TodoResponse> getAllTodos() {
        LOGGER.info("Fetching all todos");
        List<Todo> todos = todoRepository.findAllByOrderByCreatedAtDesc();
        return todos.stream()
                .map(this::mapToResponse)
                .collect(Collectors.toList());
    }

    /**
     * Get todo by id.
     *
     * @param id todo id
     * @return todo response
     */
    @Transactional(readOnly = true)
    public TodoResponse getTodoById(Long id) {
        LOGGER.info("Fetching todo with id: {}", id);
        Todo todo = todoRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Todo not found with id: " + id));
        return mapToResponse(todo);
    }

    /**
     * Update todo.
     *
     * @param id todo id
     * @param request todo request
     * @return updated todo response
     */
    public TodoResponse updateTodo(Long id, TodoRequest request) {
        LOGGER.info("Updating todo with id: {}", id);

        Todo todo = todoRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Todo not found with id: " + id));

        todo.setTitle(request.getTitle());
        todo.setDescription(request.getDescription());
        todo.setPriority(request.getPriority() != null ? request.getPriority() : todo.getPriority());
        todo.setUpdatedAt(LocalDateTime.now());

        Todo updatedTodo = todoRepository.save(todo);
        LOGGER.info("Todo updated successfully with id: {}", updatedTodo.getId());

        return mapToResponse(updatedTodo);
    }

    /**
     * Toggle todo completion status.
     *
     * @param id todo id
     * @return updated todo response
     */
    public TodoResponse toggleTodoCompletion(Long id) {
        LOGGER.info("Toggling completion status for todo with id: {}", id);

        Todo todo = todoRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Todo not found with id: " + id));

        todo.setCompleted(!todo.isCompleted());
        todo.setUpdatedAt(LocalDateTime.now());

        if (todo.isCompleted()) {
            todo.setCompletedAt(LocalDateTime.now());
            LOGGER.info("Todo marked as completed with id: {}", id);
        } else {
            todo.setCompletedAt(null);
            LOGGER.info("Todo marked as incomplete with id: {}", id);
        }

        Todo updatedTodo = todoRepository.save(todo);
        return mapToResponse(updatedTodo);
    }

    /**
     * Delete todo.
     *
     * @param id todo id
     */
    public void deleteTodo(Long id) {
        LOGGER.info("Deleting todo with id: {}", id);

        if (!todoRepository.existsById(id)) {
            throw new ResourceNotFoundException("Todo not found with id: " + id);
        }

        todoRepository.deleteById(id);
        LOGGER.info("Todo deleted successfully with id: {}", id);
    }

    /**
     * Get todos by completion status.
     *
     * @param isCompleted completion status
     * @return list of todo responses
     */
    @Transactional(readOnly = true)
    public List<TodoResponse> getTodosByStatus(boolean isCompleted) {
        LOGGER.info("Fetching todos with completion status: {}", isCompleted);
        List<Todo> todos = todoRepository.findByIsCompleted(isCompleted);
        return todos.stream()
                .map(this::mapToResponse)
                .collect(Collectors.toList());
    }

    /**
     * Map Todo entity to TodoResponse DTO.
     *
     * @param todo todo entity
     * @return todo response
     */
    private TodoResponse mapToResponse(Todo todo) {
        TodoResponse response = new TodoResponse();
        response.setId(todo.getId());
        response.setTitle(todo.getTitle());
        response.setDescription(todo.getDescription());
        response.setPriority(todo.getPriority());
        response.setCompleted(todo.isCompleted());
        response.setCreatedAt(todo.getCreatedAt());
        response.setUpdatedAt(todo.getUpdatedAt());
        response.setCompletedAt(todo.getCompletedAt());
        return response;
    }
}

// Made with Bob
