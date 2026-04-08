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
import axios from 'axios';
import { Reminder, ReminderRequest } from '../types/Reminder';

const API_BASE_URL = 'http://localhost:8080/api/reminders';

const reminderService = {
  getAllReminders: async (): Promise<Reminder[]> => {
    const response = await axios.get<Reminder[]>(API_BASE_URL);
    return response.data;
  },

  getReminderById: async (id: number): Promise<Reminder> => {
    const response = await axios.get<Reminder>(`${API_BASE_URL}/${id}`);
    return response.data;
  },

  getRemindersByTodoId: async (todoId: number): Promise<Reminder[]> => {
    const response = await axios.get<Reminder[]>(`${API_BASE_URL}/todo/${todoId}`);
    return response.data;
  },

  createReminder: async (reminder: ReminderRequest): Promise<Reminder> => {
    const response = await axios.post<Reminder>(API_BASE_URL, reminder);
    return response.data;
  },

  markReminderAsSent: async (id: number): Promise<Reminder> => {
    const response = await axios.put<Reminder>(`${API_BASE_URL}/${id}/sent`);
    return response.data;
  },

  deleteReminder: async (id: number): Promise<void> => {
    await axios.delete(`${API_BASE_URL}/${id}`);
  }
};

export default reminderService;

// Made with Bob
