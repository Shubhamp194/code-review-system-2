# Contributing to Code Review System

Welcome to the team! This guide will help you get started with contributing to the IBM Bob-a-thon code review automation project.

## 🚀 Quick Start for Team Members

### 1. Clone the Repository

```bash
git clone git@github.ibm.com:Shubham-Pandey7/code-review-system.git
cd code-review-system
```

### 2. Install Dependencies

```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Verify installation
python3 -m src.analyzer.main --help
```

### 3. Test the System

```bash
# Run analyzer on test file
python3 -m src.analyzer.main file sample-java-project/src/main/java/com/ibm/demo/TestPRFile.java

# Expected: 50 violations detected
```

## 📚 Essential Documentation

Before contributing, please read:

1. **PROJECT_PLAN.md** - Overall architecture and roadmap
2. **IMPLEMENTATION_GUIDE.md** - Technical implementation details
3. **LOCAL_TEST_RESULTS.md** - Test results and demo script
4. **ALTERNATIVE_TESTING_WITHOUT_ACTIONS.md** - Testing without GitHub Actions

## 🎯 Current Status

### ✅ Phase 1 Complete (100%)
- 36 automated rules implemented
- Rule engine with pattern matching
- CLI tool with colorized output
- GitHub Actions workflow (architecture ready)
- Comprehensive documentation
- Local testing validated (50 violations detected)

### 🔄 Phase 2 In Progress (0%)
These are the areas where we need contributions:

#### Priority 1: Bob AI Integration
**Goal:** Add semantic code analysis using IBM Bob's AI capabilities

**Tasks:**
- [ ] Implement Bob API client (`src/analyzer/bob_client.py`)
- [ ] Add quality scoring algorithm (0-100 scale)
- [ ] Create advisory recommendation system
- [ ] Integrate with existing rule engine
- [ ] Add configuration for Bob API endpoint

**Files to Create:**
- `src/analyzer/bob_client.py`
- `src/analyzer/ai_analyzer.py`
- `config/bob_config.yaml`

**Reference:** See `AI_ENHANCEMENT_PLAN.md` for detailed specifications

#### Priority 2: AI Code Explanation Feature
**Goal:** Auto-generate detailed code explanations for PRs

**Tasks:**
- [ ] Implement code explanation generator
- [ ] Add PR comment formatter
- [ ] Create explanation templates
- [ ] Integrate with Bob AI
- [ ] Add configuration options

**Files to Create:**
- `src/analyzer/code_explainer.py`
- `templates/explanation_template.md`

**Reference:** See `AI_CODE_EXPLANATION_FEATURE.md` for specifications

#### Priority 3: Web Dashboard
**Goal:** Create real-time visualization dashboard

**Tasks:**
- [ ] Set up Flask web server
- [ ] Create dashboard UI (HTML/CSS/JS)
- [ ] Add real-time metrics display
- [ ] Implement trend analysis
- [ ] Add team leaderboard

**Files to Create:**
- `src/web/app.py`
- `src/web/templates/dashboard.html`
- `src/web/static/css/style.css`
- `src/web/static/js/dashboard.js`

**Reference:** See `EXTENSIBILITY_ARCHITECTURE.md` for design

#### Priority 4: Unit Testing
**Goal:** Achieve 80%+ code coverage

**Tasks:**
- [ ] Write tests for rule engine
- [ ] Write tests for each rule
- [ ] Add integration tests
- [ ] Set up pytest configuration
- [ ] Add CI/CD for tests

**Files to Create:**
- `tests/test_rule_engine.py`
- `tests/test_rules.py`
- `tests/test_integration.py`
- `pytest.ini`

## 🔧 Development Workflow

### Creating a New Feature

1. **Create a feature branch:**
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes:**
```bash
# Edit files
# Test locally
python3 -m src.analyzer.main file <test-file>
```

3. **Commit with descriptive message:**
```bash
git add .
git commit -m "feat: Add Bob AI integration for semantic analysis

- Implemented Bob API client
- Added quality scoring algorithm
- Integrated with rule engine
- Added configuration options"
```

4. **Push to GitHub:**
```bash
git push origin feature/your-feature-name
```

5. **Create Pull Request:**
- Go to GitHub repository
- Click "New Pull Request"
- Select your branch
- Fill in description
- Request review

### Commit Message Format

Use conventional commits:

```
<type>: <description>

[optional body]

[optional footer]
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Adding tests
- `refactor:` Code refactoring
- `style:` Formatting changes
- `chore:` Maintenance tasks

**Examples:**
```bash
feat: Add Bob AI quality scoring
fix: Correct regex pattern for SQL injection detection
docs: Update API documentation
test: Add unit tests for rule engine
```

## 📁 Project Structure

```
code-review-system/
├── src/
│   ├── analyzer/
│   │   ├── main.py              # CLI entry point
│   │   ├── rule_engine.py       # Core rule engine
│   │   ├── rules/
│   │   │   ├── base.py          # Base rule classes
│   │   │   ├── high_priority.py # Security & quality rules
│   │   │   ├── medium_priority.py # Best practices
│   │   │   └── naming_rules.py  # Naming conventions
│   │   ├── bob_client.py        # [TODO] Bob AI client
│   │   └── ai_analyzer.py       # [TODO] AI analysis
│   └── web/                     # [TODO] Web dashboard
├── config/
│   ├── rules.yaml               # Rule definitions
│   └── bob_config.yaml          # [TODO] Bob AI config
├── tests/                       # [TODO] Unit tests
├── sample-java-project/         # Test cases
└── docs/                        # Documentation

[TODO] = Needs implementation
```

## 🧪 Testing Your Changes

### Run Local Tests

```bash
# Test on single file
python3 -m src.analyzer.main file sample-java-project/src/main/java/com/ibm/demo/TestPRFile.java

# Test on project
python3 -m src.analyzer.main project sample-java-project/src/main/java/

# Run unit tests (when implemented)
pytest tests/
```

### Verify Rule Detection

When adding new rules:

1. Add test case to `sample-java-project/`
2. Run analyzer on test file
3. Verify violation is detected
4. Check severity classification
5. Validate suggestion text

## 🎨 Code Style Guidelines

### Python Code Style

- Follow PEP 8
- Use type hints
- Add docstrings to functions
- Keep functions under 50 lines
- Use meaningful variable names

**Example:**
```python
def analyze_file(file_path: str, config: dict) -> AnalysisResult:
    """
    Analyze a Java file for code violations.
    
    Args:
        file_path: Path to the Java file
        config: Configuration dictionary
        
    Returns:
        AnalysisResult with violations found
    """
    # Implementation
    pass
```

### Documentation Style

- Use Markdown for all docs
- Include code examples
- Add table of contents for long docs
- Use emojis for visual clarity
- Keep line length under 120 chars

## 🐛 Reporting Issues

Found a bug? Please create an issue with:

1. **Title:** Brief description
2. **Description:** Detailed explanation
3. **Steps to Reproduce:** How to trigger the bug
4. **Expected Behavior:** What should happen
5. **Actual Behavior:** What actually happens
6. **Environment:** OS, Python version, etc.

## 💡 Suggesting Features

Have an idea? Create an issue with:

1. **Title:** Feature name
2. **Problem:** What problem does it solve?
3. **Solution:** How would it work?
4. **Alternatives:** Other approaches considered
5. **Impact:** Who benefits and how?

## 📞 Getting Help

### Documentation Resources

- **PROJECT_PLAN.md** - Architecture overview
- **IMPLEMENTATION_GUIDE.md** - Technical details
- **RULE_SPECIFICATIONS.md** - All 36 rules documented
- **AI_ENHANCEMENT_PLAN.md** - Bob AI integration specs
- **EXTENSIBILITY_ARCHITECTURE.md** - Plugin system design

### Communication

- **GitHub Issues:** For bugs and features
- **Pull Request Comments:** For code review discussions
- **Team Meetings:** For planning and coordination

## 🎯 Contribution Areas

### For Backend Developers
- Bob AI integration
- Rule engine enhancements
- API development
- Performance optimization

### For Frontend Developers
- Web dashboard UI
- Real-time visualization
- Interactive charts
- Responsive design

### For DevOps Engineers
- CI/CD pipeline setup
- Docker containerization
- Deployment automation
- Monitoring setup

### For QA Engineers
- Unit test development
- Integration testing
- Performance testing
- Test automation

### For Technical Writers
- Documentation improvements
- API documentation
- User guides
- Tutorial creation

## 🏆 Recognition

Contributors will be:
- Listed in project README
- Credited in hackathon presentation
- Recognized in final submission

## 📋 Checklist for New Contributors

- [ ] Clone repository
- [ ] Install dependencies
- [ ] Run local tests
- [ ] Read essential documentation
- [ ] Choose a task from Phase 2
- [ ] Create feature branch
- [ ] Make changes
- [ ] Test locally
- [ ] Commit with good message
- [ ] Push and create PR
- [ ] Respond to review feedback

## 🚀 Ready to Contribute?

1. Pick a task from Phase 2 priorities above
2. Create a feature branch
3. Start coding!
4. Ask questions if stuck
5. Submit PR when ready

**Let's build an amazing code review system together!** 🎉

---

**Questions?** Check the documentation or create an issue.

**Need help?** Reach out to the team lead or other contributors.

**Happy coding!** 💻