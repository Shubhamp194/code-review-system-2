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
import { useState, useEffect } from 'react';
import { Todo, TodoRequest, Priority } from './types/Todo';
import todoService from './services/todoService';
import './App.css';

function App() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newTodoTitle, setNewTodoTitle] = useState('');
  const [newTodoDescription, setNewTodoDescription] = useState('');
  const [newTodoPriority, setNewTodoPriority] = useState<Priority>(Priority.MEDIUM);
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');

  useEffect(() => {
    loadTodos();
  }, []);

  const loadTodos = async () => {
    try {
      setIsLoading(true);
      const data = await todoService.getAllTodos();
      setTodos(data);
      setError(null);
    } catch (err) {
      setError('Failed to load todos. Please make sure the backend is running.');
      console.error('Error loading todos:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateTodo = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTodoTitle.trim()) {
      return;
    }

    try {
      const todoRequest: TodoRequest = {
        title: newTodoTitle,
        description: newTodoDescription,
        priority: newTodoPriority
      };
      const createdTodo = await todoService.createTodo(todoRequest);
      setTodos([createdTodo, ...todos]);
      setNewTodoTitle('');
      setNewTodoDescription('');
      setNewTodoPriority(Priority.MEDIUM);
      setError(null);
    } catch (err) {
      setError('Failed to create todo');
      console.error('Error creating todo:', err);
    }
  };

  const handleToggleComplete = async (id: number) => {
    try {
      const updatedTodo = await todoService.toggleTodoCompletion(id);
      setTodos(todos.map(todo => todo.id === id ? updatedTodo : todo));
      setError(null);
    } catch (err) {
      setError('Failed to update todo');
      console.error('Error toggling todo:', err);
    }
  };

  const handleDeleteTodo = async (id: number) => {
    try {
      await todoService.deleteTodo(id);
      setTodos(todos.filter(todo => todo.id !== id));
      setError(null);
    } catch (err) {
      setError('Failed to delete todo');
      console.error('Error deleting todo:', err);
    }
  };

  const getFilteredTodos = () => {
    switch (filter) {
      case 'active':
        return todos.filter(todo => !todo.isCompleted);
      case 'completed':
        return todos.filter(todo => todo.isCompleted);
      default:
        return todos;
    }
  };

  const getPriorityColor = (priority: Priority) => {
    switch (priority) {
      case Priority.HIGH:
        return '#ff4444';
      case Priority.MEDIUM:
        return '#ffaa00';
      case Priority.LOW:
        return '#44ff44';
      default:
        return '#888';
    }
  };

  const filteredTodos = getFilteredTodos();
  const activeCount = todos.filter(t => !t.isCompleted).length;
  const completedCount = todos.filter(t => t.isCompleted).length;

  return (
    <div className="app">
      <header className="app-header">
        <h1>📝 Todo List</h1>
        <p className="subtitle">IBM Code Review System Demo</p>
      </header>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <div className="container">
        <form onSubmit={handleCreateTodo} className="todo-form">
          <input
            type="text"
            placeholder="What needs to be done?"
            value={newTodoTitle}
            onChange={(e) => setNewTodoTitle(e.target.value)}
            className="todo-input"
          />
          <textarea
            placeholder="Description (optional)"
            value={newTodoDescription}
            onChange={(e) => setNewTodoDescription(e.target.value)}
            className="todo-textarea"
            rows={2}
          />
          <div className="form-row">
            <select
              value={newTodoPriority}
              onChange={(e) => setNewTodoPriority(e.target.value as Priority)}
              className="priority-select"
            >
              <option value={Priority.LOW}>Low Priority</option>
              <option value={Priority.MEDIUM}>Medium Priority</option>
              <option value={Priority.HIGH}>High Priority</option>
            </select>
            <button type="submit" className="add-button">
              Add Todo
            </button>
          </div>
        </form>

        <div className="filter-tabs">
          <button
            className={filter === 'all' ? 'active' : ''}
            onClick={() => setFilter('all')}
          >
            All ({todos.length})
          </button>
          <button
            className={filter === 'active' ? 'active' : ''}
            onClick={() => setFilter('active')}
          >
            Active ({activeCount})
          </button>
          <button
            className={filter === 'completed' ? 'active' : ''}
            onClick={() => setFilter('completed')}
          >
            Completed ({completedCount})
          </button>
        </div>

        {isLoading ? (
          <div className="loading">Loading todos...</div>
        ) : filteredTodos.length === 0 ? (
          <div className="empty-state">
            {filter === 'all' ? 'No todos yet. Create one above!' :
             filter === 'active' ? 'No active todos!' :
             'No completed todos!'}
          </div>
        ) : (
          <ul className="todo-list">
            {filteredTodos.map(todo => (
              <li key={todo.id} className={`todo-item ${todo.isCompleted ? 'completed' : ''}`}>
                <div className="todo-content">
                  <input
                    type="checkbox"
                    checked={todo.isCompleted}
                    onChange={() => handleToggleComplete(todo.id)}
                    className="todo-checkbox"
                  />
                  <div className="todo-details">
                    <h3 className="todo-title">{todo.title}</h3>
                    {todo.description && (
                      <p className="todo-description">{todo.description}</p>
                    )}
                    <div className="todo-meta">
                      <span
                        className="priority-badge"
                        style={{ backgroundColor: getPriorityColor(todo.priority) }}
                      >
                        {todo.priority}
                      </span>
                      <span className="todo-date">
                        {new Date(todo.createdAt).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                </div>
                <button
                  onClick={() => handleDeleteTodo(todo.id)}
                  className="delete-button"
                  title="Delete todo"
                >
                  🗑️
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>

      <footer className="app-footer">
        <p>Built with React + Spring Boot | IBM Code Review System</p>
      </footer>
    </div>
  );
}

export default App;

// Made with Bob
