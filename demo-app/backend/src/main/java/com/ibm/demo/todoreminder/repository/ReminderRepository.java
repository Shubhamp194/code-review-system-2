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

import com.ibm.demo.todoreminder.model.Reminder;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

/**
 * Repository interface for Reminder entity operations.
 */
@Repository
public interface ReminderRepository extends JpaRepository<Reminder, Long> {

    /**
     * Find all reminders for a specific todo.
     *
     * @param todoId todo id
     * @return list of reminders
     */
    List<Reminder> findByTodoId(Long todoId);

    /**
     * Find all unsent reminders that are due.
     *
     * @param currentTime current time
     * @return list of due reminders
     */
    List<Reminder> findByIsSentFalseAndReminderTimeBefore(LocalDateTime currentTime);

    /**
     * Find all reminders ordered by reminder time.
     *
     * @return list of reminders
     */
    List<Reminder> findAllByOrderByReminderTimeAsc();
}

// Made with Bob
