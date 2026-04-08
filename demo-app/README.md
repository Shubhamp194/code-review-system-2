# Todo List Application

A full-stack Todo List application built with React and Spring Boot to demonstrate the IBM Code Review System.

## Architecture

- **Backend**: Spring Boot 3.2.0 with Java 17
- **Frontend**: React 18 with TypeScript and Vite
- **Database**: H2 (in-memory)

## Prerequisites

- Java 17 or higher
- Maven 3.6+
- Node.js 18+ and npm
- Git

## Running the Application

### 1. Start the Backend

```bash
cd demo-app/backend
mvn clean install
mvn spring-boot:run
```

The backend will start on `http://localhost:8080`

API endpoints:
- `GET /api/todos` - Get all todos
- `POST /api/todos` - Create a new todo
- `GET /api/todos/{id}` - Get todo by ID
- `PUT /api/todos/{id}` - Update todo
- `PUT /api/todos/{id}/toggle` - Toggle completion status
- `DELETE /api/todos/{id}` - Delete todo

### 2. Start the Frontend

Open a new terminal:

```bash
cd demo-app/frontend
npm install
npm run dev
```

The frontend will start on `http://localhost:3000`

### 3. Access the Application

Open your browser and navigate to:
```
http://localhost:3000
```

## Features

### Current Features (Main Branch)
- ✅ Create todos with title, description, and priority
- ✅ Mark todos as complete/incomplete
- ✅ Delete todos
- ✅ Filter todos (All, Active, Completed)
- ✅ Priority levels (Low, Medium, High)
- ✅ Responsive design
- ✅ Real-time updates

### Upcoming Features (Reminder Branch)
- 🔔 Set reminders for todos
- ⏰ Reminder notifications
- 📅 Due date tracking
- 🔄 Recurring reminders

## Code Quality

This application follows IBM coding standards:
- ✅ Proper IBM license headers
- ✅ SLF4J logging (no System.out)
- ✅ Proper exception handling
- ✅ No hardcoded secrets
- ✅ Descriptive variable names
- ✅ TypeScript type safety
- ✅ Clean architecture (Controller → Service → Repository)

## Testing the Code Review System

This application is designed to demonstrate the automated code review system:

1. **Main Branch**: Contains clean, well-written code that passes all checks
2. **Reminder Feature Branches**: Will contain enhancements that demonstrate PR review process

## Project Structure

```
demo-app/
├── backend/
│   ├── src/main/java/com/ibm/demo/todoreminder/
│   │   ├── TodoReminderApplication.java
│   │   ├── model/
│   │   │   ├── Todo.java
│   │   │   └── Priority.java
│   │   ├── repository/
│   │   │   └── TodoRepository.java
│   │   ├── service/
│   │   │   └── TodoService.java
│   │   ├── controller/
│   │   │   └── TodoController.java
│   │   ├── dto/
│   │   │   ├── TodoRequest.java
│   │   │   └── TodoResponse.java
│   │   ├── exception/
│   │   │   ├── ResourceNotFoundException.java
│   │   │   └── GlobalExceptionHandler.java
│   │   └── config/
│   │       └── WebConfig.java
│   └── pom.xml
└── frontend/
    ├── src/
    │   ├── App.tsx
    │   ├── App.css
    │   ├── main.tsx
    │   ├── types/
    │   │   └── Todo.ts
    │   └── services/
    │       └── todoService.ts
    ├── package.json
    ├── vite.config.ts
    └── tsconfig.json
```

## API Examples

### Create a Todo
```bash
curl -X POST http://localhost:8080/api/todos \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive README and API docs",
    "priority": "HIGH"
  }'
```

### Get All Todos
```bash
curl http://localhost:8080/api/todos
```

### Toggle Todo Completion
```bash
curl -X PUT http://localhost:8080/api/todos/1/toggle
```

### Delete a Todo
```bash
curl -X DELETE http://localhost:8080/api/todos/1
```

## Development

### Backend Development
- Uses Spring Boot DevTools for hot reload
- H2 Console available at: `http://localhost:8080/h2-console`
  - JDBC URL: `jdbc:h2:mem:tododb`
  - Username: `sa`
  - Password: (empty)

### Frontend Development
- Vite provides hot module replacement
- TypeScript for type safety
- Axios for API calls
- CSS for styling (no framework dependencies)

## Troubleshooting

### Backend Issues
- **Port 8080 already in use**: Change port in `application.properties`
- **Maven build fails**: Ensure Java 17+ is installed
- **Database errors**: H2 is in-memory, data resets on restart

### Frontend Issues
- **npm install fails**: Clear npm cache: `npm cache clean --force`
- **Port 3000 in use**: Vite will automatically use next available port
- **API connection fails**: Ensure backend is running on port 8080

## License

Copyright IBM Corporation 2026

Licensed under the Apache License, Version 2.0