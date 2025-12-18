# Contributing to Swasthya Monitor

Thank you for your interest in contributing to Swasthya Monitor! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Follow the project's coding standards
- Maintain medical accuracy and safety

## Development Setup

1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Create a virtual environment: `python -m venv venv`
4. Activate virtual environment and install dependencies: `pip install -r requirements.txt`
5. Create `.streamlit/secrets.toml` with your API keys (see README.md)

## Coding Standards

### Python Style

- Follow PEP 8 style guide
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use descriptive variable and function names

### Documentation

- Add docstrings to all functions and classes
- Use Google-style docstrings
- Include parameter descriptions and return types
- Update README.md for user-facing changes

### Code Organization

- Keep functions focused and single-purpose
- Maximum file length: 300 lines (aim for <200)
- Separate concerns (logic, data, presentation)
- Add error handling for all external calls

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes with clear, descriptive commits
3. Add/update tests if applicable
4. Update documentation as needed
5. Ensure all checks pass
6. Submit pull request with clear description

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
How was this tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes
```

## Medical Accuracy

- All clinical thresholds must reference established guidelines (ICMR, AHA, etc.)
- Changes to risk calculation algorithms require medical validation
- Include citations for new medical standards
- Maintain backward compatibility with existing risk scores

## Testing

- Add unit tests for new functions
- Test edge cases and error conditions
- Verify UI changes in both English and Hindi
- Test with sample patient data

## Questions?

Open an issue for:
- Feature requests
- Bug reports
- Questions about implementation
- Medical guideline clarifications

---

Thank you for contributing to Swasthya Monitor! 🏥

