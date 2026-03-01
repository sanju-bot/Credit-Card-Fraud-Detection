# Contributing to Credit Card Fraud Detection System

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/credit-card-fraud-detection.git
   cd credit-card-fraud-detection
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Development Workflow

### Making Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and test thoroughly

3. **Format code** with Black:
   ```bash
   black src/ app/ --line-length=100
   ```

4. **Run linting** with Pylint:
   ```bash
   pylint src/ app/
   ```

5. **Run tests**:
   ```bash
   pytest tests/ -v
   ```

### Committing Changes

- Use clear, descriptive commit messages
- Reference issues where applicable: `Fixes #123`
- Keep commits atomic and focused

Example:
```bash
git commit -m "Feature: Add threshold optimization for fraud detection

- Implements adaptive thresholds based on fraud rate
- Improves recall by 5%
- Fixes #42"
```

## Code Style Guide

- Follow **PEP 8** standards
- Use **type hints** for function parameters
- Add **docstrings** to all functions and classes
- Keep functions focused and testable
- Maximum line length: 100 characters

### Example Function:

```python
def calculate_fraud_probability(amount: float, hour: int, merchant_type: str) -> float:
    """
    Calculate fraud probability based on transaction characteristics.
    
    Args:
        amount: Transaction amount in dollars
        hour: Hour of day (0-23)
        merchant_type: Category of merchant
        
    Returns:
        Fraud probability score (0.0-1.0)
    """
    # Implementation
    pass
```

## Testing

- Write tests for new features
- Maintain >80% code coverage
- Test edge cases and error conditions

```bash
pytest tests/ --cov=src --cov-report=html
```

## Documentation

- Update README.md for user-facing changes
- Document new features in docstrings
- Add examples for complex functionality
- Keep docs in sync with code

## Pull Request Process

1. **Update** README.md with new features
2. **Add tests** for new functionality
3. **Update** requirements.txt if dependencies change
4. **Verify** all tests pass locally
5. **Create PR** with descriptive title and body

PR Template:

```markdown
## Description
Brief description of changes

## Type
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update

## Testing
- [ ] Added tests
- [ ] All tests pass
- [ ] Tested locally

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No new warnings generated
```

## Issues & Bug Reports

### Reporting Bugs

Include:
- Python version and OS
- How to reproduce the issue
- Expected vs actual behavior
- Error messages/logs

### Feature Requests

Include:
- Problem statement
- Proposed solution
- Alternatives considered
- Use case/benefits

## Questions?

- Open a GitHub Discussion
- Check existing Issues
- Review documentation

---

Thank you for contributing! 🎉
