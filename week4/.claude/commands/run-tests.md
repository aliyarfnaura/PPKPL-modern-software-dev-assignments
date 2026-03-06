# Run Tests

This automation runs the pytest test suite for the backend and summarizes the results.

```bash
cd backend && python -m pytest tests/ -v --tb=short
```

## Summary

After running the tests, this command will:

1. Change to the backend directory
2. Run pytest with verbose output and short traceback
3. Display the test results including passed/failed tests
4. Show any errors or failures with minimal traceback information

This helps maintain code quality by ensuring all tests pass before committing changes.