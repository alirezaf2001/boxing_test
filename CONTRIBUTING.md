# Contributing to TaskForge

Thank you for your interest in contributing to TaskForge! We welcome contributions from the community.

## Development Setup

1. Fork the repository on GitHub
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/taskforge.git
   cd taskforge
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

5. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Development Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Run tests:
   ```bash
   pytest
   ```

4. Run linting and formatting:
   ```bash
   ruff check .
   ruff format .
   ```

5. Run type checking:
   ```bash
   mypy src/
   ```

6. Commit your changes:
   ```bash
   git commit -m "Add your commit message"
   ```

7. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

8. Create a Pull Request on GitHub

## Code Style

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Write docstrings for modules, classes, and functions
- Keep functions small and focused on a single responsibility
- Use descriptive variable and function names

## Testing

- Write unit tests for new functionality
- Ensure all tests pass before submitting a PR
- Aim for good test coverage
- Use descriptive test names

## Documentation

- Update documentation for any new features
- Ensure code examples work
- Keep the README up to date

## Commit Messages

Use clear, descriptive commit messages. Follow this format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Maintenance tasks

## Issues

- Check existing issues before creating new ones
- Use issue templates when available
- Provide clear reproduction steps for bugs
- Suggest features with detailed descriptions

## Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. By participating, you agree to:

- Be respectful and inclusive
- Focus on constructive feedback
- Accept responsibility for mistakes
- Show empathy towards other contributors
- Help create a positive community

## License

By contributing to TaskForge, you agree that your contributions will be licensed under the same MIT License that covers the project.