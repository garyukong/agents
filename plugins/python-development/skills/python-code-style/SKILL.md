---
name: python-code-style
description: Python code style, linting, formatting, naming conventions, and documentation standards. Use when writing new code, reviewing style, configuring linters, writing docstrings, or establishing project standards.
---

# Python Code Style & Documentation

Consistent code style and clear documentation make codebases maintainable and collaborative. This skill covers modern Python tooling, naming conventions, and documentation standards.

> Org override: When used inside this org, the Python Code Standards in @[/Users/garykong/.codeium/memories/global_rules.md] take precedence

## When to Use This Skill

- Setting up linting and formatting for a new project
- Writing or reviewing docstrings
- Establishing team coding standards
- Configuring ruff for linting and formatting
- Reviewing code for style consistency
- Creating project documentation

## Core Concepts

### 1. Automated Formatting

Let tools handle formatting debates. Configure once, enforce automatically.

### 2. Consistent Naming

Follow PEP 8 conventions with meaningful, descriptive names.

### 3. Documentation as Code

Docstrings should be maintained alongside the code they describe.

### 4. Type Annotations

Modern Python code should include type hints for all public APIs.

## Quick Start

```bash
# Install modern tooling
poetry add --group dev ruff

# Configure in pyproject.toml
[tool.ruff]
line-length = 99
target-version = "py313"  # Org default baseline is Python 3.13+
```

## Fundamental Patterns

### Pattern 1: Modern Python Tooling

Use `ruff` as an all-in-one linter and formatter. It replaces flake8, isort, and black with a single fast tool.

```toml
# pyproject.toml
[tool.ruff]
line-length = 99
target-version = "py313"  # Org default baseline is Python 3.13+

[tool.ruff.lint]
select = [
    "I",    # isort
    "E4",   # pycodestyle import errors
    "E7",   # pycodestyle statement errors
    "E9",   # pycodestyle runtime errors
    "F",    # pyflakes
]
# Optional: Enable additional rules for stricter checking
# "E",    # all pycodestyle errors
# "W",    # pycodestyle warnings
# "B",    # flake8-bugbear
# "C4",   # flake8-comprehensions
# "UP",   # pyupgrade
# "SIM",  # flake8-simplify

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

Run with:

```bash
ruff check --fix .  # Lint and auto-fix
ruff format .       # Format code
```

**Standalone Config File:** For monorepos or projects preferring a separate config file, use `ruff.toml` at the project root instead of `[tool.ruff]` in pyproject.toml:

```toml
# ruff.toml
line-length = 99
target-version = "py313"

[lint]
select = ["I", "E4", "E7", "E9", "F"]

[format]
quote-style = "double"
indent-style = "space"
docstring-code-format = true
```

### Pattern 2: Naming Conventions

Follow PEP 8 with emphasis on clarity over brevity.

**Files and Modules:**

```python
# Good: Descriptive snake_case
user_repository.py
order_processing.py
http_client.py

# Avoid: Abbreviations
usr_repo.py
ord_proc.py
http_cli.py
```

**Classes and Functions:**

```python
# Classes: PascalCase
class UserRepository:
    pass

class HTTPClientFactory:  # Acronyms stay uppercase
    pass

# Functions and variables: snake_case
def get_user_by_email(email: str) -> User | None:
    retry_count = 3
    max_connections = 100
```

**Constants:**

```python
# Module-level constants: SCREAMING_SNAKE_CASE
MAX_RETRY_ATTEMPTS = 3
DEFAULT_TIMEOUT_SECONDS = 30
API_BASE_URL = "https://api.example.com"
```

### Pattern 3: Import Organization

Group imports in a consistent order: standard library, third-party, local.

```python
# Standard library
import os
from collections.abc import Callable
from typing import Any

# Third-party packages
import httpx
from pydantic import BaseModel
from sqlalchemy import Column

# Local imports
from myproject.models import User
from myproject.services import UserService
```

Use absolute imports exclusively:

```python
# Preferred
from myproject.utils import retry_decorator

# Avoid relative imports
from ..utils import retry_decorator
```

## Advanced Patterns

### Pattern 4: Google-Style Docstrings

Write docstrings for all public classes, methods, and functions.

**Simple Function:**

```python
def get_user(user_id: str) -> User:
    """
    Retrieve a user by their unique identifier.
    """
    ...
```

**Complex Function:**

```python
def process_batch(
    items: list[Item],
    max_workers: int = 4,
    on_progress: Callable[[int, int], None] | None = None,
) -> BatchResult:
    """
    Process items concurrently using a worker pool.

    Processes each item in the batch using the configured number of
    workers. Progress can be monitored via the optional callback.

    Args:
        items: The items to process. Must not be empty.
        max_workers: Maximum concurrent workers. Defaults to 4.
        on_progress: Optional callback receiving (completed, total) counts.

    Returns:
        BatchResult containing succeeded items and any failures with
        their associated exceptions.

    Raises:
        ValueError: If items is empty.
        ProcessingError: If the batch cannot be processed.

    Example:
        >>> result = process_batch(items, max_workers=8)
        >>> print(f"Processed {len(result.succeeded)} items")
    """
    ...
```

**Class Docstring:**

```python
class UserService:
    """
    Service for managing user operations.

    Provides methods for creating, retrieving, updating, and
    deleting users with proper validation and error handling.

    Attributes:
        repository: The data access layer for user persistence.
        logger: Logger instance for operation tracking.

    Example:
        >>> service = UserService(repository, logger)
        >>> user = service.create_user(CreateUserInput(...))
    """

    def __init__(self, repository: UserRepository, logger: Logger) -> None:
        """
        Initialize the user service.

        Args:
            repository: Data access layer for users.
            logger: Logger for tracking operations.
        """
        self.repository = repository
        self.logger = logger
```

### Pattern 6: Line Length and Formatting

Set line length to 99 characters to match the org standard while maintaining readability.

```python
# Good: Readable line breaks
def create_user(
    email: str,
    name: str,
    role: UserRole = UserRole.MEMBER,
    notify: bool = True,
) -> User:
    ...

# Good: Chain method calls clearly
result = (
    db.query(User)
    .filter(User.active == True)
    .order_by(User.created_at.desc())
    .limit(10)
    .all()
)

# Good: Format long strings
error_message = (
    f"Failed to process user {user_id}: "
    f"received status {response.status_code} "
    f"with body {response.text[:100]}"
)
```

### Pattern 7: Project Documentation

**README Structure:**

```markdown
# Project Name

Brief description of what the project does.

## Installation

\`\`\`bash
poetry install --with dev
# or
uv sync --all-extras --dev
\`\`\`

## Quick Start

\`\`\`python
from myproject import Client

client = Client(api_key="...")
result = client.process(data)
\`\`\`

## Configuration

Document environment variables and configuration options.

## Development

\`\`\`bash
poetry run pytest
# or
uv run pytest
\`\`\`
```

**CHANGELOG Format (Keep a Changelog):**

```markdown
# Changelog

## [Unreleased]

### Added
- New feature X

### Changed
- Modified behavior of Y

### Fixed
- Bug in Z
```

## Best Practices Summary

1. **Use ruff** - Single tool for linting and formatting
2. **99 character lines** - Org standard for readability
3. **Type checking via IDE** - Use PyCharm's built-in type checker
4. **Descriptive names** - Clarity over brevity
5. **Absolute imports** - More maintainable than relative
6. **Google-style docstrings** - Consistent, readable documentation
7. **Document public APIs** - Every public function needs a docstring
8. **Keep docs updated** - Treat documentation as code
9. **Automate in CI** - Run linters on every commit
10. **Target Python 3.13+** - Org baseline for modern language features