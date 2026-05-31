# Contributing to BatchPrint Pro

Thank you for your interest in contributing to BatchPrint Pro. This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Community](#community)

## Code of Conduct

By participating in this project, you agree to abide by the following principles:

- **Be respectful**: Treat all contributors with respect and professionalism
- **Be inclusive**: Welcome newcomers and help them get started
- **Be constructive**: Provide actionable feedback and accept criticism gracefully
- **Be honest**: Do not plagiarize or misrepresent your contributions

## How to Contribute

There are many ways to contribute to BatchPrint Pro:

### Report Bugs

- Use the [GitHub Issues](https://github.com/yourusername/BatchPrintPro/issues) page
- Search existing issues before creating a new one
- Use the bug report template if available
- Include steps to reproduce, expected behavior, and actual behavior

### Suggest Features

- Open an issue with the "enhancement" label
- Clearly describe the proposed feature and its use case
- Discuss the feature with maintainers before implementing

### Submit Code

- Fork the repository
- Create a feature branch
- Make your changes
- Submit a pull request

### Improve Documentation

- Fix typos or unclear wording
- Add missing documentation
- Translate documentation to other languages

## Development Setup

### Prerequisites

- Python 3.13 or higher
- Git
- A GitHub account

### Setting Up the Development Environment

1. **Fork the repository** on GitHub

2. **Clone your fork** locally:

   ```bash
   git clone https://github.com/yourusername/BatchPrintPro.git
   cd BatchPrintPro
   ```

3. **Create a virtual environment**:

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies (optional)
   ```

5. **Run the application**:

   ```bash
   python main.py
   ```

6. **Add the upstream remote**:

   ```bash
   git remote add upstream https://github.com/originalusername/BatchPrintPro.git
   ```

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use 4 spaces for indentation (no tabs)
- Limit lines to 79 characters (or 88 for Black formatter)
- Use meaningful variable and function names

### Documentation

- Write docstrings for all public functions and classes
- Follow [Google Style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) for docstrings
- Comment complex logic

Example:

```python
def print_document(file_path: str, printer_name: str) -> tuple[bool, str]:
    """
    Print a document to the specified printer.
    
    Args:
        file_path: Path to the document file
        printer_name: Name of the target printer
        
    Returns:
        Tuple of (success: bool, message: str)
        
    Raises:
        FileNotFoundError: If file_path does not exist
        PrinterError: If printer_name is not available
    """
    pass
```

### Type Hints

Use type hints for function signatures:

```python
from typing import Optional

def get_printer_status(printer_name: str) -> Optional[dict]:
    """Get the status of a printer."""
    pass
```

### MVVM Architecture

Respect the MVVM separation of concerns:

- **Models** (`src/models/`): Data structures and business logic
- **Views** (`src/views/`): User interface components only
- **ViewModels** (`src/viewmodels/`): Presentation logic and state management
- **Services** (`src/services/`): External integrations and utilities

Do not:

- Access UI components from Models or Services
- Put business logic in Views
- Mix presentation logic with data access

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Build process or auxiliary tool changes

Examples:

```
feat(print): add support for TIFF image format

fix(ui): correct task list selection behavior

docs(readme): update installation instructions
```

## Pull Request Process

### Before Creating a PR

1. **Update your fork** with the latest upstream changes:

   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create a feature branch**:

   ```bash
   git checkout -b feat/add-tiff-support
   ```

3. **Make your changes** and commit them:

   ```bash
   git add .
   git commit -m "feat(print): add support for TIFF image format"
   ```

4. **Run tests** (if available):

   ```bash
   python -m pytest tests/
   ```

5. **Update documentation** if necessary

### Creating the PR

1. **Push your branch** to your fork:

   ```bash
   git push origin feat/add-tiff-support
   ```

2. **Open a Pull Request** on GitHub:
   - Go to your fork on GitHub
   - Click "Compare & pull request"
   - Fill in the PR template
   - Link related issues

3. **PR Title Format**: `feat(scope): description` (same as commit messages)

4. **PR Description** should include:
   - What changes were made and why
   - How to test the changes
   - Screenshots (if UI changes)
   - Related issue numbers

### Review Process

- Maintainers will review your PR
- Address feedback by pushing additional commits
- Once approved, a maintainer will merge your PR

### After Merge

- Delete your feature branch
- Update your local main branch

```bash
git checkout main
git pull upstream main
git branch -d feat/add-tiff-support
```

## Issue Reporting

### Bug Reports

Use the following template:

```markdown
**Description**
A clear description of the bug.

**Steps to Reproduce**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g., Windows 11]
- Python version: [e.g., 3.13.0]
- Package versions: [e.g., PySide6 6.11.1]

**Screenshots**
If applicable, add screenshots.

**Additional Context**
Any other context about the problem.
```

### Feature Requests

Use the following template:

```markdown
**Feature Description**
A clear description of the proposed feature.

**Use Case**
Why is this feature needed?

**Proposed Solution**
How should this feature work?

**Alternatives Considered**
Are there alternative approaches?

**Additional Context**
Any other context or screenshots.
```

## Community

### Getting Help

- Check the [documentation](README.md)
- Search [existing issues](https://github.com/yourusername/BatchPrintPro/issues)
- Open a new issue with the "question" label

### Recognition

Contributors will be acknowledged in:
- The project's README.md
- Release notes for significant contributions

---

Thank you for contributing to BatchPrint Pro!
