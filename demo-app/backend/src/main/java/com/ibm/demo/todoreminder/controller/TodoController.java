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

import com.ibm.demo.todoreminder.dto.TodoRequest;
import com.ibm.demo.todoreminder.dto.TodoResponse;
import com.ibm.demo.todoreminder.service.TodoService;
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
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/**
 * REST controller for Todo operations.
 */
@RestController
@RequestMapping("/api/todos")
@CrossOrigin(origins = "*")
public class TodoController {

    private static final Logger LOGGER = LoggerFactory.getLogger(TodoController.class);

    private final TodoService todoService;

    @Autowired
    public TodoController(TodoService todoService) {
        this.todoService = todoService;
    }

    /**
     * Create a new todo.
     *
     * @param request todo request
     * @return created todo response
     */
    @PostMapping
    public ResponseEntity<TodoResponse> createTodo(@Valid @RequestBody TodoRequest request) {
        LOGGER.info("REST request to create todo");
        TodoResponse response = todoService.createTodo(request);
        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }

    /**
     * Get all todos or filter by completion status.
     *
     * @param isCompleted optional completion status filter
     * @return list of todos
     */
    @GetMapping
    public ResponseEntity<List<TodoResponse>> getAllTodos(
            @RequestParam(required = false) Boolean isCompleted) {
        LOGGER.info("REST request to get all todos");

        List<TodoResponse> todos;
        if (isCompleted != null) {
            todos = todoService.getTodosByStatus(isCompleted);
        } else {
            todos = todoService.getAllTodos();
        }

        return ResponseEntity.ok(todos);
    }

    /**
     * Get todo by id.
     *
     * @param id todo id
     * @return todo response
     */
    @GetMapping("/{id}")
    public ResponseEntity<TodoResponse> getTodoById(@PathVariable Long id) {
        LOGGER.info("REST request to get todo with id: {}", id);
        TodoResponse response = todoService.getTodoById(id);
        return ResponseEntity.ok(response);
    }

    /**
     * Update todo.
     *
     * @param id todo id
     * @param request todo request
     * @return updated todo response
     */
    @PutMapping("/{id}")
    public ResponseEntity<TodoResponse> updateTodo(
            @PathVariable Long id,
            @Valid @RequestBody TodoRequest request) {
        LOGGER.info("REST request to update todo with id: {}", id);
        TodoResponse response = todoService.updateTodo(id, request);
        return ResponseEntity.ok(response);
    }

    /**
     * Toggle todo completion status.
     *
     * @param id todo id
     * @return updated todo response
     */
    @PutMapping("/{id}/toggle")
    public ResponseEntity<TodoResponse> toggleTodoCompletion(@PathVariable Long id) {
        LOGGER.info("REST request to toggle completion for todo with id: {}", id);
        TodoResponse response = todoService.toggleTodoCompletion(id);
        return ResponseEntity.ok(response);
    }

    /**
     * Delete todo.
     *
     * @param id todo id
     * @return no content response
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteTodo(@PathVariable Long id) {
        LOGGER.info("REST request to delete todo with id: {}", id);
        todoService.deleteTodo(id);
        return ResponseEntity.noContent().build();
    }
}

// Made with Bob
