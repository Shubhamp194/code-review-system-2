# Complete Rule Specifications

## 📋 Rule Categories & Implementation Details

---

## 🔴 HIGH PRIORITY RULES (P0 - Critical)

### SEC001: IBM License/Copyright Header
**Severity**: HIGH  
**Category**: Legal Compliance  
**Blocks Merge**: Yes

**Description**: Every Java file must start with IBM copyright/license header

**Detection Pattern**:
```python
def check_ibm_header(content):
    required_patterns = [
        r'Copyright.*IBM',
        r'Licensed under.*Apache License',
        r'SPDX-License-Identifier'
    ]
    first_50_lines = '\n'.join(content.split('\n')[:50])
    return all(re.search(p, first_50_lines, re.IGNORECASE) for p in required_patterns)
```

**Valid Example**:
```java
/*
 * Copyright IBM Corporation 2024
 * Licensed under the Apache License, Version 2.0
 * SPDX-License-Identifier: Apache-2.0
 */
package com.ibm.demo;
```

**Invalid Example**:
```java
package com.ibm.demo;  // Missing header
```

**Fix Suggestion**: Add IBM copyright header at the beginning of the file

---

### SEC002: No Hardcoded Secrets
**Severity**: CRITICAL  
**Category**: Security  
**Blocks Merge**: Yes

**Description**: Detects hardcoded passwords, API keys, tokens, and secrets

**Detection Patterns**:
```regex
password\s*=\s*["'][^"']+["']
api[_-]?key\s*=\s*["'][^"']+["']
secret\s*=\s*["'][^"']+["']
token\s*=\s*["'][^"']+["']
private[_-]?key\s*=\s*["'][^"']+["']
access[_-]?key\s*=\s*["'][^"']+["']
```

**Invalid Examples**:
```java
String password = "admin123";
String apiKey = "sk-1234567890abcdef";
String dbPassword = "P@ssw0rd!";
```

**Valid Examples**:
```java
String password = System.getenv("DB_PASSWORD");
String apiKey = config.getProperty("api.key");
String token = secretsManager.getSecret("auth-token");
```

**Fix Suggestion**: Use environment variables, configuration files, or secrets management systems

---

### SEC003: No SQL String Concatenation
**Severity**: CRITICAL  
**Category**: Security (SQL Injection)  
**Blocks Merge**: Yes

**Description**: Detects SQL queries built using string concatenation

**Detection Patterns**:
```regex
executeQuery\s*\([^)]*\+[^)]*\)
executeUpdate\s*\([^)]*\+[^)]*\)
"SELECT.*"\s*\+
"INSERT.*"\s*\+
"UPDATE.*"\s*\+
"DELETE.*"\s*\+
```

**Invalid Examples**:
```java
String query = "SELECT * FROM users WHERE id = " + userId;
stmt.executeQuery("SELECT * FROM " + tableName);
```

**Valid Examples**:
```java
String query = "SELECT * FROM users WHERE id = ?";
PreparedStatement stmt = conn.prepareStatement(query);
stmt.setInt(1, userId);
```

**Fix Suggestion**: Use PreparedStatement with parameterized queries

---

### SEC004: No Runtime.exec() with Variables
**Severity**: CRITICAL  
**Category**: Security (Command Injection)  
**Blocks Merge**: Yes

**Description**: Detects Runtime.exec() usage with variables

**Detection Pattern**:
```regex
Runtime\.getRuntime\(\)\.exec\([^"'][^)]*\)
ProcessBuilder\([^"'][^)]*\)
```

**Invalid Examples**:
```java
Runtime.getRuntime().exec("rm -rf " + userInput);
Runtime.getRuntime().exec(command);
```

**Valid Examples**:
```java
// Use ProcessBuilder with validated input
ProcessBuilder pb = new ProcessBuilder("ls", "-la");
// Or use allowlist validation
if (ALLOWED_COMMANDS.contains(command)) {
    Runtime.getRuntime().exec(command);
}
```

**Fix Suggestion**: Avoid Runtime.exec() or use strict input validation with allowlists

---

### SEC005: No Logging Sensitive Data
**Severity**: CRITICAL  
**Category**: Security (Data Exposure)  
**Blocks Merge**: Yes

**Description**: Detects logging of sensitive information

**Detection Patterns**:
```regex
log\.(info|debug|warn|error)\([^)]*password[^)]*\)
log\.(info|debug|warn|error)\([^)]*token[^)]*\)
log\.(info|debug|warn|error)\([^)]*secret[^)]*\)
log\.(info|debug|warn|error)\([^)]*apiKey[^)]*\)
```

**Invalid Examples**:
```java
log.info("User password: " + password);
log.debug("API token: " + token);
logger.error("Secret key: " + secretKey);
```

**Valid Examples**:
```java
log.info("User authenticated successfully");
log.debug("API call completed");
logger.error("Authentication failed");
```

**Fix Suggestion**: Never log sensitive data; log events without exposing credentials

---

### CQ001: No System.out/err.println
**Severity**: HIGH  
**Category**: Code Quality  
**Blocks Merge**: Yes

**Description**: Detects console output statements

**Detection Patterns**:
```regex
System\.out\.println
System\.err\.println
System\.out\.print\(
System\.err\.print\(
```

**Invalid Examples**:
```java
System.out.println("Debug message");
System.err.println("Error occurred");
```

**Valid Examples**:
```java
log.info("Debug message");
log.error("Error occurred");
```

**Fix Suggestion**: Use proper logging framework (SLF4J, Log4j, etc.)

---

### CQ002: No printStackTrace()
**Severity**: HIGH  
**Category**: Code Quality  
**Blocks Merge**: Yes

**Description**: Detects printStackTrace() usage

**Detection Pattern**:
```regex
\.printStackTrace\(\)
```

**Invalid Example**:
```java
catch (Exception e) {
    e.printStackTrace();
}
```

**Valid Example**:
```java
catch (Exception e) {
    log.error("Operation failed", e);
}
```

**Fix Suggestion**: Use proper logging with exception parameter

---

### CQ003: No TODO/FIXME Comments
**Severity**: HIGH  
**Category**: Code Quality  
**Blocks Merge**: Yes

**Description**: Detects TODO/FIXME comments in committed code

**Detection Patterns**:
```regex
//\s*TODO
//\s*FIXME
/\*\s*TODO
/\*\s*FIXME
```

**Invalid Examples**:
```java
// TODO: Implement error handling
// FIXME: This is a temporary hack
```

**Valid Approach**: Create issues/tickets instead of TODO comments

**Fix Suggestion**: Remove TODO/FIXME or create proper issue tracker items

---

### CQ004: No Empty Catch Blocks
**Severity**: CRITICAL  
**Category**: Exception Handling  
**Blocks Merge**: Yes

**Description**: Detects empty catch blocks

**Detection Pattern**:
```python
def check_empty_catch(content):
    pattern = r'catch\s*\([^)]+\)\s*\{\s*\}'
    return re.findall(pattern, content)
```

**Invalid Examples**:
```java
try {
    riskyOperation();
} catch (Exception e) {
}

try {
    process();
} catch (IOException e) {
    // Empty
}
```

**Valid Examples**:
```java
try {
    riskyOperation();
} catch (Exception e) {
    log.error("Operation failed", e);
    throw new CustomException("Failed", e);
}
```

**Fix Suggestion**: Log the exception or handle it appropriately

---

### CQ005: No Catching Generic Exception
**Severity**: HIGH  
**Category**: Exception Handling  
**Blocks Merge**: Yes

**Description**: Detects catching of generic Exception or Throwable

**Detection Patterns**:
```regex
catch\s*\(\s*Exception\s+
catch\s*\(\s*Throwable\s+
```

**Invalid Examples**:
```java
catch (Exception e) { }
catch (Throwable t) { }
```

**Valid Examples**:
```java
catch (IOException e) { }
catch (SQLException e) { }
catch (CustomException e) { }
```

**Fix Suggestion**: Catch specific exception types

---

### CQ006: No Hardcoded URLs
**Severity**: HIGH  
**Category**: Configuration  
**Blocks Merge**: Yes

**Description**: Detects hardcoded URLs

**Detection Patterns**:
```regex
https?://[^\s"']+
String\s+\w+\s*=\s*"https?://
```

**Invalid Examples**:
```java
String apiUrl = "https://api.example.com/v1";
String endpoint = "http://localhost:8080/api";
```

**Valid Examples**:
```java
String apiUrl = config.getProperty("api.url");
String endpoint = System.getenv("API_ENDPOINT");
```

**Fix Suggestion**: Use configuration files or environment variables

---

### CQ007: No Hardcoded File Paths
**Severity**: HIGH  
**Category**: Configuration  
**Blocks Merge**: Yes

**Description**: Detects hardcoded file system paths

**Detection Patterns**:
```regex
/tmp/
/home/
/usr/
C:\\
D:\\
```

**Invalid Examples**:
```java
String path = "/tmp/data.txt";
File file = new File("C:\\Users\\data");
```

**Valid Examples**:
```java
String path = System.getProperty("java.io.tmpdir") + "/data.txt";
File file = new File(config.getDataDirectory(), "data.txt");
```

**Fix Suggestion**: Use system properties or configuration

---

### CQ008: No Commented-Out Code
**Severity**: MEDIUM  
**Category**: Code Quality  
**Blocks Merge**: No

**Description**: Detects large blocks of commented-out code

**Detection Logic**:
```python
def check_commented_code(content):
    lines = content.split('\n')
    consecutive_comments = 0
    
    for line in lines:
        if re.match(r'^\s*//', line.strip()):
            consecutive_comments += 1
            if consecutive_comments > 5:
                return True
        else:
            consecutive_comments = 0
    return False
```

**Fix Suggestion**: Remove commented code; use version control instead

---

## 🟡 MEDIUM PRIORITY RULES (P1)

### IMP001: No Wildcard Imports
**Severity**: MEDIUM  
**Category**: Import Management  
**Blocks Merge**: No

**Detection Patterns**:
```regex
import\s+[a-zA-Z0-9.]+\.\*;
import\s+static\s+[a-zA-Z0-9.]+\.\*;
```

**Invalid Examples**:
```java
import java.util.*;
import static org.junit.Assert.*;
```

**Valid Examples**:
```java
import java.util.List;
import java.util.ArrayList;
import static org.junit.Assert.assertEquals;
```

**Fix Suggestion**: Import specific classes instead of using wildcards

---

### IMP002: No Duplicate Imports
**Severity**: LOW  
**Category**: Import Management  
**Blocks Merge**: No

**Detection Logic**:
```python
def check_duplicate_imports(content):
    imports = re.findall(r'import\s+([^;]+);', content)
    return [imp for imp in imports if imports.count(imp) > 1]
```

**Fix Suggestion**: Remove duplicate import statements

---

### FMT001: No Trailing Whitespace
**Severity**: LOW  
**Category**: Formatting  
**Blocks Merge**: No

**Detection Pattern**:
```regex
\s+$
```

**Fix Suggestion**: Remove trailing whitespace from lines

---

### FMT002: Max 2 Consecutive Blank Lines
**Severity**: LOW  
**Category**: Formatting  
**Blocks Merge**: No

**Detection Logic**:
```python
def check_blank_lines(content):
    lines = content.split('\n')
    consecutive_blank = 0
    
    for line in lines:
        if line.strip() == '':
            consecutive_blank += 1
            if consecutive_blank > 2:
                return True
        else:
            consecutive_blank = 0
    return False
```

**Fix Suggestion**: Limit consecutive blank lines to 2

---

### FMT003: Line Length ≤ 120 Characters
**Severity**: LOW  
**Category**: Formatting  
**Blocks Merge**: No

**Detection Logic**:
```python
def check_line_length(content):
    violations = []
    for i, line in enumerate(content.split('\n'), 1):
        if len(line) > 120:
            violations.append(i)
    return violations
```

**Fix Suggestion**: Break long lines into multiple lines

---

### FMT004: File Must End with Newline
**Severity**: LOW  
**Category**: Formatting  
**Blocks Merge**: No

**Detection Logic**:
```python
def check_file_ending(content):
    return not content.endswith('\n')
```

**Fix Suggestion**: Add newline at end of file

---

### CQ009: No Debug Flags
**Severity**: MEDIUM  
**Category**: Code Quality  
**Blocks Merge**: No

**Detection Patterns**:
```regex
boolean\s+debug\s*=\s*true
boolean\s+DEBUG\s*=\s*true
private\s+static\s+final\s+boolean\s+DEBUG\s*=\s*true
```

**Invalid Examples**:
```java
boolean debug = true;
private static final boolean DEBUG = true;
```

**Valid Example**:
```java
boolean debug = Boolean.parseBoolean(System.getProperty("debug", "false"));
```

**Fix Suggestion**: Use configuration or environment variables for debug flags

---

### CQ010: No System.exit()
**Severity**: MEDIUM  
**Category**: Code Quality  
**Blocks Merge**: No

**Detection Pattern**:
```regex
System\.exit\(
```

**Invalid Example**:
```java
System.exit(1);
```

**Valid Approach**: Throw exceptions or return error codes

**Fix Suggestion**: Use proper exception handling instead of System.exit()

---

### CQ011: No Thread.sleep()
**Severity**: MEDIUM  
**Category**: Code Quality  
**Blocks Merge**: No

**Detection Pattern**:
```regex
Thread\.sleep\(
```

**Invalid Example**:
```java
Thread.sleep(1000);
```

**Valid Examples**:
```java
TimeUnit.SECONDS.sleep(1);
ScheduledExecutorService.schedule(...);
```

**Fix Suggestion**: Use proper concurrency utilities

---

### CQ012: No String Concatenation in Loops
**Severity**: MEDIUM  
**Category**: Performance  
**Blocks Merge**: No

**Detection Pattern**:
```python
def check_string_concat_in_loop(content):
    # Look for += inside for/while loops
    in_loop = False
    violations = []
    
    for i, line in enumerate(content.split('\n'), 1):
        if re.search(r'\b(for|while)\s*\(', line):
            in_loop = True
        if in_loop and re.search(r'\w+\s*\+=\s*["\']', line):
            violations.append(i)
        if in_loop and line.strip() == '}':
            in_loop = False
    
    return violations
```

**Invalid Example**:
```java
String result = "";
for (String item : items) {
    result += item;
}
```

**Valid Example**:
```java
StringBuilder result = new StringBuilder();
for (String item : items) {
    result.append(item);
}
```

**Fix Suggestion**: Use StringBuilder for string concatenation in loops

---

### CQ013: No == for String Comparison
**Severity**: MEDIUM  
**Category**: Code Quality  
**Blocks Merge**: No

**Detection Pattern**:
```regex
\w+\s*==\s*"[^"]*"
"[^"]*"\s*==\s*\w+
```

**Invalid Examples**:
```java
if (name == "John") { }
if ("admin" == userRole) { }
```

**Valid Examples**:
```java
if ("John".equals(name)) { }
if ("admin".equals(userRole)) { }
```

**Fix Suggestion**: Use .equals() method for string comparison

---

### CQ014: No Public Fields
**Severity**: MEDIUM  
**Category**: Encapsulation  
**Blocks Merge**: No

**Detection Pattern**:
```regex
public\s+(?!class|interface|enum|static\s+final)\w+\s+\w+\s*;
```

**Invalid Example**:
```java
public String name;
public int count;
```

**Valid Examples**:
```java
private String name;
public static final String CONSTANT = "value";
```

**Fix Suggestion**: Make fields private and provide getters/setters

---

### CQ015: No Static Mutable Variables
**Severity**: MEDIUM  
**Category**: Thread Safety  
**Blocks Merge**: No

**Detection Pattern**:
```regex
static\s+(?!final)\w+\s+\w+\s*=
```

**Invalid Examples**:
```java
static List<String> cache = new ArrayList<>();
static int counter = 0;
```

**Valid Examples**:
```java
static final List<String> CONSTANTS = Collections.unmodifiableList(...);
private static final AtomicInteger counter = new AtomicInteger(0);
```

**Fix Suggestion**: Make static variables final or use thread-safe alternatives

---

## 🔤 NAMING RULES (P1)

### NAM001: Lowercase Package Names
**Severity**: MEDIUM  
**Category**: Naming Convention  
**Blocks Merge**: No

**Detection Pattern**:
```regex
package\s+[a-z0-9.]*[A-Z][a-z0-9.]*;
```

**Invalid Example**:
```java
package com.IBM.Demo;
```

**Valid Example**:
```java
package com.ibm.demo;
```

**Fix Suggestion**: Use lowercase for package names

---

### NAM002: UpperCamelCase Class Names
**Severity**: MEDIUM  
**Category**: Naming Convention  
**Blocks Merge**: No

**Detection Pattern**:
```regex
(class|interface|enum)\s+[a-z]
```

**Invalid Examples**:
```java
class myClass { }
interface userService { }
```

**Valid Examples**:
```java
class MyClass { }
interface UserService { }
```

**Fix Suggestion**: Use UpperCamelCase for class names

---

### NAM003: lowerCamelCase Method Names
**Severity**: MEDIUM  
**Category**: Naming Convention  
**Blocks Merge**: No

**Detection Pattern**:
```regex
(public|private|protected)\s+\w+\s+[A-Z]\w+\s*\(
```

**Invalid Example**:
```java
public void ProcessData() { }
```

**Valid Example**:
```java
public void processData() { }
```

**Fix Suggestion**: Use lowerCamelCase for method names

---

### NAM004: UPPER_SNAKE_CASE Constants
**Severity**: MEDIUM  
**Category**: Naming Convention  
**Blocks Merge**: No

**Detection Pattern**:
```regex
static\s+final\s+\w+\s+[a-z]
```

**Invalid Example**:
```java
static final String apiKey = "key";
```

**Valid Example**:
```java
static final String API_KEY = "key";
```

**Fix Suggestion**: Use UPPER_SNAKE_CASE for constants

---

### NAM005: No Generic Variable Names
**Severity**: LOW  
**Category**: Naming Convention  
**Blocks Merge**: No

**Blacklist**: temp, data, obj, var, thing, stuff, foo, bar

**Detection Pattern**:
```regex
\b(temp|data|obj|var|thing|stuff|foo|bar)\b
```

**Invalid Examples**:
```java
String temp = getValue();
Object obj = new Object();
```

**Valid Examples**:
```java
String userName = getValue();
User user = new User();
```

**Fix Suggestion**: Use descriptive variable names

---

### NAM006: No Single-Character Variables (except i,j,k)
**Severity**: LOW  
**Category**: Naming Convention  
**Blocks Merge**: No

**Detection Pattern**:
```regex
\b[a-hln-z]\b(?!\s*[=:])
```

**Invalid Examples**:
```java
int x = 10;
String s = "test";
```

**Valid Examples**:
```java
int count = 10;
String message = "test";
// Allowed in loops:
for (int i = 0; i < n; i++) { }
```

**Fix Suggestion**: Use descriptive names except for loop counters

---

### NAM007: Boolean Naming Convention
**Severity**: LOW  
**Category**: Naming Convention  
**Blocks Merge**: No

**Detection Pattern**:
```regex
boolean\s+(?!is|has|should|can|will)\w+
```

**Invalid Examples**:
```java
boolean active;
boolean valid;
```

**Valid Examples**:
```java
boolean isActive;
boolean hasPermission;
boolean shouldProcess;
```

**Fix Suggestion**: Boolean variables should start with is/has/should/can/will

---

## 📝 LOGGING RULES (P1)

### LOG001: No String Concatenation in Logging
**Severity**: MEDIUM  
**Category**: Performance  
**Blocks Merge**: No

**Detection Pattern**:
```regex
log\.(info|debug|warn|error)\([^)]*\+[^)]*\)
```

**Invalid Examples**:
```java
log.info("User: " + userName);
log.debug("Count: " + count);
```

**Valid Examples**:
```java
log.info("User: {}", userName);
log.debug("Count: {}", count);
```

**Fix Suggestion**: Use parameterized logging

---

### LOG002: Logger Variable Naming
**Severity**: LOW  
**Category**: Convention  
**Blocks Merge**: No

**Detection Pattern**:
```regex
Logger\s+(?!log|logger)\w+\s*=
```

**Invalid Example**:
```java
Logger myLogger = LoggerFactory.getLogger(...);
```

**Valid Examples**:
```java
Logger log = LoggerFactory.getLogger(...);
Logger logger = LoggerFactory.getLogger(...);
```

**Fix Suggestion**: Name logger variable as 'log' or 'logger'

---

## 🔧 EXCEPTION HANDLING RULES (P0/P1)

### EXC001: Exceptions Must Be Logged
**Severity**: HIGH  
**Category**: Exception Handling  
**Blocks Merge**: Yes

**Detection Logic**: Check if catch blocks contain log statements

**Invalid Example**:
```java
catch (Exception e) {
    return null;
}
```

**Valid Example**:
```java
catch (Exception e) {
    log.error("Operation failed", e);
    return null;
}
```

**Fix Suggestion**: Always log exceptions in catch blocks

---

### EXC002: No Throwing Generic Exception
**Severity**: MEDIUM  
**Category**: Exception Handling  
**Blocks Merge**: No

**Detection Pattern**:
```regex
throw\s+new\s+Exception\(
```

**Invalid Example**:
```java
throw new Exception("Error");
```

**Valid Example**:
```java
throw new CustomException("Error");
throw new IllegalArgumentException("Invalid input");
```

**Fix Suggestion**: Throw specific exception types

---

## 📦 IMPORT & STRUCTURE RULES (P1)

### STR001: Grouped Imports
**Severity**: LOW  
**Category**: Code Organization  
**Blocks Merge**: No

**Expected Order**:
1. java.*
2. javax.*
3. org.*
4. com.*
5. Project-specific

**Fix Suggestion**: Organize imports in standard groups

---

### STR002: No Imports in Class Body
**Severity**: MEDIUM  
**Category**: Code Organization  
**Blocks Merge**: No

**Detection**: Check if import statements appear after class declaration

**Fix Suggestion**: Move all imports to file header

---

### STR003: One Public Class Per File
**Severity**: MEDIUM  
**Category**: Code Organization  
**Blocks Merge**: No

**Detection Logic**:
```python
def check_multiple_public_classes(content):
    return len(re.findall(r'public\s+class\s+', content)) > 1
```

**Fix Suggestion**: Split into separate files

---

## 🔵 LOW PRIORITY RULES (P2/P3)

### ADV001: No Magic Numbers
**Severity**: LOW  
**Category**: Code Quality  
**Blocks Merge**: No

**Detection**: Numbers > 2 digits not in constants

**Fix Suggestion**: Extract to named constants

---

### ADV002: No Consecutive Semicolons
**Severity**: LOW  
**Category**: Code Quality  
**Blocks Merge**: No

**Detection Pattern**:
```regex
;;
```

**Fix Suggestion**: Remove extra semicolons

---

### ADV003: No Redundant Boolean Checks
**Severity**: LOW  
**Category**: Code Quality  
**Blocks Merge**: No

**Detection Patterns**:
```regex
if\s*\(\s*\w+\s*==\s*true\s*\)
if\s*\(\s*\w+\s*==\s*false\s*\)
```

**Invalid Examples**:
```java
if (flag == true) { }
if (isValid == false) { }
```

**Valid Examples**:
```java
if (flag) { }
if (!isValid) { }
```

**Fix Suggestion**: Use boolean directly

---

### ADV004: No Empty Methods
**Severity**: LOW  
**Category**: Code Quality  
**Blocks Merge**: No

**Detection Pattern**:
```regex
\w+\s*\([^)]*\)\s*\{\s*\}
```

**Fix Suggestion**: Implement method or remove if unused

---

### ADV005: No Deprecated API Usage
**Severity**: MEDIUM  
**Category**: Code Quality  
**Blocks Merge**: No

**Detection**: Check for @Deprecated annotation usage

**Fix Suggestion**: Use recommended alternatives

---

### ADV006: No @SuppressWarnings("all")
**Severity**: MEDIUM  
**Category**: Code Quality  
**Blocks Merge**: No

**Detection Pattern**:
```regex
@SuppressWarnings\("all"\)
```

**Fix Suggestion**: Suppress specific warnings only

---

## 📊 Rule Summary Statistics

| Category | Total Rules | P0 (Critical) | P1 (High) | P2 (Medium) | P3 (Low) |
|----------|-------------|---------------|-----------|-------------|----------|
| Security | 5 | 5 | 0 | 0 | 0 |
| Code Quality | 15 | 4 | 8 | 3 | 0 |
| Naming | 7 | 0 | 4 | 3 | 0 |
| Logging | 2 | 0 | 1 | 1 | 0 |
| Exception Handling | 3 | 2 | 1 | 0 | 0 |
| Import/Structure | 3 | 0 | 2 | 1 | 0 |
| Advanced | 6 | 0 | 0 | 2 | 4 |
| **TOTAL** | **41** | **11** | **16** | **10** | **4** |

---

## 🎯 Implementation Priority

### Phase 1 (Must Have - 2 hours)
- All P0 rules (11 rules)
- Critical security and quality checks

### Phase 2 (Should Have - 2 hours)
- All P1 rules (16 rules)
- Naming conventions and best practices

### Phase 3 (Nice to Have - 1 hour)
- P2 rules (10 rules)
- Advanced quality checks

### Phase 4 (Optional - 1 hour)
- P3 rules (4 rules)
- Polish and edge cases

---

**Total: 41 comprehensive rules covering all major Java code quality aspects! 🎯**