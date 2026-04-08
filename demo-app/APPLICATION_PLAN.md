# Todo & Reminder Full-Stack Application Plan

## Overview
A complete full-stack application demonstrating clean code practices that will pass all code review checks.

## Technology Stack

### Backend
- **Framework**: Spring Boot 3.2.0
- **Language**: Java 17
- **Database**: H2 (in-memory for demo)
- **Build Tool**: Maven
- **Key Dependencies**:
  - Spring Web
  - Spring Data JPA
  - Spring Validation
  - Lombok
  - SLF4J for logging

### Frontend
- **Framework**: React 18
- **Language**: TypeScript
- **Build Tool**: Vite
- **Styling**: SCSS with modern design
- **State Management**: React Hooks
- **HTTP Client**: Axios

## Backend Structure

```
demo-app/backend/
├── pom.xml
├── src/
│   └── main/
│       ├── java/com/ibm/demo/todoreminder/
│       │   ├── TodoReminderApplication.java          # Main application
│       │   ├── config/
│       │   │   ├── CorsConfig.java                   # CORS configuration
│       │   │   └── WebConfig.java                    # Web configuration
│       │   ├── model/
│       │   │   ├── Todo.java                         # Todo entity
│       │   │   ├── Reminder.java                     # Reminder entity
│       │   │   └── Priority.java                     # Priority enum
│       │   ├── repository/
│       │   │   ├── TodoRepository.java               # Todo data access
│       │   │   └── ReminderRepository.java           # Reminder data access
│       │   ├── service/
│       │   │   ├── TodoService.java                  # Todo business logic
│       │   │   └── ReminderService.java              # Reminder business logic
│       │   ├── controller/
│       │   │   ├── TodoController.java               # Todo REST API
│       │   │   └── ReminderController.java           # Reminder REST API
│       │   ├── dto/
│       │   │   ├── TodoRequest.java                  # Todo request DTO
│       │   │   ├── TodoResponse.java                 # Todo response DTO
│       │   │   ├── ReminderRequest.java              # Reminder request DTO
│       │   │   └── ReminderResponse.java             # Reminder response DTO
│       │   └── exception/
│       │       ├── ResourceNotFoundException.java    # Custom exception
│       │       └── GlobalExceptionHandler.java       # Exception handler
│       └── resources/
│           ├── application.yml                       # Application config
│           └── data.sql                              # Sample data
```

## Frontend Structure

```
demo-app/frontend/
├── package.json
├── tsconfig.json
├── vite.config.ts
├── index.html
├── public/
│   └── favicon.ico
└── src/
    ├── main.tsx                                      # Entry point
    ├── App.tsx                                       # Main app component
    ├── vite-env.d.ts                                 # Vite types
    ├── api/
    │   ├── axios.ts                                  # Axios configuration
    │   ├── todoApi.ts                                # Todo API calls
    │   └── reminderApi.ts                            # Reminder API calls
    ├── components/
    │   ├── TodoList.tsx                              # Todo list component
    │   ├── TodoItem.tsx                              # Todo item component
    │   ├── TodoForm.tsx                              # Todo form component
    │   ├── ReminderList.tsx                          # Reminder list component
    │   ├── ReminderItem.tsx                          # Reminder item component
    │   ├── ReminderForm.tsx                          # Reminder form component
    │   ├── Header.tsx                                # Header component
    │   └── Footer.tsx                                # Footer component
    ├── types/
    │   ├── todo.ts                                   # Todo types
    │   └── reminder.ts                               # Reminder types
    ├── hooks/
    │   ├── useTodos.ts                               # Todo custom hook
    │   └── useReminders.ts                           # Reminder custom hook
    ├── styles/
    │   ├── main.scss                                 # Main styles
    │   ├── variables.scss                            # SCSS variables
    │   ├── components/
    │   │   ├── todo.scss                             # Todo styles
    │   │   ├── reminder.scss                         # Reminder styles
    │   │   ├── header.scss                           # Header styles
    │   │   └── footer.scss                           # Footer styles
    │   └── utils/
    │       ├── mixins.scss                           # SCSS mixins
    │       └── animations.scss                       # Animations
    └── utils/
        ├── dateFormatter.ts                          # Date utilities
        └── validators.ts                             # Validation utilities
```

## Features

### Todo Management
1. **Create Todo**
   - Title (required)
   - Description (optional)
   - Priority (LOW, MEDIUM, HIGH)
   - Due date (optional)
   - Status (PENDING, IN_PROGRESS, COMPLETED)

2. **List Todos**
   - View all todos
   - Filter by status
   - Filter by priority
   - Sort by due date

3. **Update Todo**
   - Edit title, description
   - Change priority
   - Update status
   - Modify due date

4. **Delete Todo**
   - Remove todo from list

### Reminder Management
1. **Create Reminder**
   - Title (required)
   - Description (optional)
   - Reminder date/time (required)
   - Repeat option (NONE, DAILY, WEEKLY, MONTHLY)

2. **List Reminders**
   - View all reminders
   - Filter by date range
   - Sort by reminder time

3. **Update Reminder**
   - Edit title, description
   - Change reminder time
   - Update repeat option

4. **Delete Reminder**
   - Remove reminder from list

## API Endpoints

### Todo Endpoints
```
GET    /api/todos              # Get all todos
GET    /api/todos/{id}         # Get todo by ID
POST   /api/todos              # Create new todo
PUT    /api/todos/{id}         # Update todo
DELETE /api/todos/{id}         # Delete todo
GET    /api/todos/status/{status}  # Get todos by status
GET    /api/todos/priority/{priority}  # Get todos by priority
```

### Reminder Endpoints
```
GET    /api/reminders          # Get all reminders
GET    /api/reminders/{id}     # Get reminder by ID
POST   /api/reminders          # Create new reminder
PUT    /api/reminders/{id}     # Update reminder
DELETE /api/reminders/{id}     # Delete reminder
GET    /api/reminders/upcoming # Get upcoming reminders
```

## Code Quality Standards

### All code will follow:
1. ✅ IBM license header on all files
2. ✅ No hardcoded secrets or URLs
3. ✅ Proper logging with SLF4J (no System.out)
4. ✅ No TODO/FIXME comments
5. ✅ Proper exception handling (no empty catch blocks)
6. ✅ Specific exception types (no generic Exception)
7. ✅ PreparedStatement for SQL (no string concatenation)
8. ✅ No wildcard imports
9. ✅ Proper naming conventions:
   - Classes: UpperCamelCase
   - Methods: lowerCamelCase
   - Constants: UPPER_SNAKE_CASE
   - Packages: lowercase
10. ✅ Boolean variables start with is/has/should
11. ✅ No trailing whitespace
12. ✅ Lines under 120 characters
13. ✅ Proper TypeScript types (no `any`)
14. ✅ SCSS with design tokens (no hardcoded colors)

## UI Design

### Color Scheme
- Primary: IBM Blue (#0f62fe)
- Secondary: IBM Purple (#8a3ffc)
- Success: #24a148
- Warning: #f1c21b
- Danger: #da1e28
- Background: #f4f4f4
- Text: #161616

### Layout
- Responsive design (mobile-first)
- Clean, modern interface
- Card-based layout for todos and reminders
- Smooth animations and transitions
- Accessible (WCAG 2.1 AA compliant)

## Development Steps

### Phase 1: Backend (Clean Code)
1. Create Spring Boot application structure
2. Define entities with proper annotations
3. Create repositories with JPA
4. Implement services with business logic
5. Build REST controllers with validation
6. Add exception handling
7. Configure CORS for frontend
8. Add sample data

### Phase 2: Frontend (Clean Code)
1. Initialize React + TypeScript + Vite project
2. Set up Axios for API calls
3. Create type definitions
4. Build reusable components
5. Implement custom hooks
6. Add SCSS styling with design tokens
7. Implement responsive layout
8. Add form validation

### Phase 3: Integration
1. Connect frontend to backend
2. Test all CRUD operations
3. Verify error handling
4. Test responsive design
5. Ensure code passes all review checks

### Phase 4: Enhancement Branches (With Violations)
1. **Branch 1: feature/add-notifications**
   - Add violations: hardcoded secrets, System.out, TODO comments
   - Should fail code review

2. **Branch 2: feature/add-search**
   - Add violations: SQL injection, empty catch blocks, wildcard imports
   - Should fail code review

## Testing Strategy

### Backend Tests
- Unit tests for services
- Integration tests for repositories
- Controller tests with MockMvc

### Frontend Tests
- Component tests with React Testing Library
- API integration tests
- E2E tests with Playwright (optional)

## Deployment

### Backend
- Package as JAR
- Run with: `java -jar todo-reminder-backend-1.0.0.jar`
- Default port: 8080

### Frontend
- Build with: `npm run build`
- Serve with: `npm run preview`
- Default port: 5173

## Next Steps

1. Generate all backend files with clean code
2. Generate all frontend files with clean code
3. Test locally to ensure everything works
4. Commit and push to main branch
5. Create enhancement branches with violations
6. Create PRs to test code review system

---

**Status**: Ready to implement
**Estimated Files**: ~40 files total
**Estimated Time**: 2-3 hours for complete implementation