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
package com.ibm.demo.todoreminder.repository;

import com.ibm.demo.todoreminder.model.Priority;
import com.ibm.demo.todoreminder.model.Todo;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repository interface for Todo entity operations.
 */
@Repository
public interface TodoRepository extends JpaRepository<Todo, Long> {

    /**
     * Find all todos by completion status.
     *
     * @param isCompleted completion status
     * @return list of todos
     */
    List<Todo> findByIsCompleted(boolean isCompleted);

    /**
     * Find all todos by priority.
     *
     * @param priority priority level
     * @return list of todos
     */
    List<Todo> findByPriority(Priority priority);

    /**
     * Find all todos ordered by creation date descending.
     *
     * @return list of todos
     */
    List<Todo> findAllByOrderByCreatedAtDesc();
}

// Made with Bob
