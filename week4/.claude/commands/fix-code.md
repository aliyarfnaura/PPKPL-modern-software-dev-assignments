# Fix Code

This automation runs code formatting and linting tools to maintain code quality.

```bash
cd backend && black . && ruff check . --fix
```

## Summary

This command will:

1. Change to the backend directory
2. Run `black` to format all Python files according to PEP 8 standards
3. Run `ruff` with `--fix` to automatically fix any linting issues it can resolve
4. Display any remaining issues that require manual attention

This ensures consistent code style and catches potential issues before they become problems.