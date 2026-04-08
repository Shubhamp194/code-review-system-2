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
import { Todo, TodoRequest } from '../types/Todo';

const API_BASE_URL = 'http://localhost:8080/api/todos';

const todoService = {
  getAllTodos: async (): Promise<Todo[]> => {
    const response = await axios.get<Todo[]>(API_BASE_URL);
    return response.data;
  },

  getTodoById: async (id: number): Promise<Todo> => {
    const response = await axios.get<Todo>(`${API_BASE_URL}/${id}`);
    return response.data;
  },

  createTodo: async (todo: TodoRequest): Promise<Todo> => {
    const response = await axios.post<Todo>(API_BASE_URL, todo);
    return response.data;
  },

  updateTodo: async (id: number, todo: TodoRequest): Promise<Todo> => {
    const response = await axios.put<Todo>(`${API_BASE_URL}/${id}`, todo);
    return response.data;
  },

  toggleTodoCompletion: async (id: number): Promise<Todo> => {
    const response = await axios.put<Todo>(`${API_BASE_URL}/${id}/toggle`);
    return response.data;
  },

  deleteTodo: async (id: number): Promise<void> => {
    await axios.delete(`${API_BASE_URL}/${id}`);
  },

  getTodosByStatus: async (isCompleted: boolean): Promise<Todo[]> => {
    const response = await axios.get<Todo[]>(`${API_BASE_URL}?isCompleted=${isCompleted}`);
    return response.data;
  }
};

export default todoService;

// Made with Bob
