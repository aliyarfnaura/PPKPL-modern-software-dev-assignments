# Week 4 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **Naura** \
SUNet ID: **N\A** \
Citations: **Claude Code Documentation, FastAPI Documentation**

This assignment took me about **4** hours to do. 


## YOUR RESPONSES
### Automation #1: /run-tests
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> The design of the /run-tests automation is inspired by Claude Code best practices for developer workflow automation. According to Claude Code documentation, automations should focus on repetitive tasks that developers perform frequently, such as running tests. Automation helps developers by reducing manual effort, ensuring consistency in test execution, and providing immediate feedback on code quality. This aligns with the principle that automations should enhance productivity without requiring complex inputs, making the development process more efficient and less error-prone.

b. Design of each automation, including goals, inputs/outputs, steps
> **Goals:** The primary goal of /run-tests is to execute the pytest test suite for the backend application and provide a clear summary of test results, including any failures. This ensures that code changes don't break existing functionality and maintains code quality.
> 
> **Inputs:** No explicit inputs are required - the automation operates on the current state of the codebase.
> 
> **Outputs:** The automation outputs pytest results including passed/failed test counts, detailed failure information with short tracebacks, and a summary of test execution status.
> 
> **Steps/Workflow:**
> 1. Change directory to the backend folder
> 2. Execute `python -m pytest tests/ -v --tb=short`
> 3. Display results with verbose output and minimal traceback information

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> **How to run:** Type `/run-tests` in Claude Code interface. The automation will execute automatically.
> 
> **Expected outputs:** 
> - Success: "X passed, Y failed" summary with detailed test results
> - Failure: Detailed error messages for failed tests with short tracebacks
> 
> **Rollback/Safety notes:** This automation is safe and read-only - it only runs tests without modifying code. No rollback needed as it doesn't change files. If tests fail, developers can fix the code and re-run the automation.

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before (Manual Workflow):** Developers had to manually navigate to the backend directory, remember the exact pytest command syntax (`cd backend && python -m pytest tests/ -v --tb=short`), execute it in terminal, and manually interpret the results. This process was time-consuming, prone to command typos, and inconsistent across different developers.
> 
> **After (Automated Workflow):** Developers simply type `/run-tests` and get immediate, consistent test execution with summarized results. The automation handles directory navigation and command execution, reducing cognitive load and ensuring all team members follow the same testing procedure.

e. How you used the automation to enhance the starter application
> I used the /run-tests automation while implementing the new /status endpoint in the FastAPI application. After adding the endpoint to `main.py`, I ran `/run-tests` to verify that the new code didn't break any existing functionality. The automation quickly executed all backend tests and confirmed that the application remained stable, allowing me to confidently commit the changes knowing the test suite passed.


### Automation #2: /fix-code
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> The /fix-code automation follows Claude Code best practices for code quality maintenance. Claude Code documentation emphasizes that automations should handle routine maintenance tasks like formatting and linting, which are essential but tedious for developers. This automation reduces the cognitive burden of remembering multiple tool commands and ensures consistent code style across the team, preventing style-related conflicts and maintaining professional code standards.

b. Design of each automation, including goals, inputs/outputs, steps
> **Goals:** The goal of /fix-code is to automatically format Python code using Black and fix linting issues using Ruff, maintaining consistent code style and catching potential problems before they become issues.
> 
> **Inputs:** No explicit inputs required - operates on the current Python files in the backend directory.
> 
> **Outputs:** Formatted Python files according to PEP 8 standards, automatically fixed linting issues, and a report of any remaining issues that require manual attention.
> 
> **Steps/Workflow:**
> 1. Change directory to the backend folder
> 2. Execute `black .` to format all Python files
> 3. Execute `ruff check . --fix` to automatically fix linting issues
> 4. Display any remaining issues that couldn't be auto-fixed

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> **How to run:** Type `/fix-code` in Claude Code interface. The automation executes automatically.
> 
> **Expected outputs:**
> - Black: Reformatted files with no output if successful, or summary of changes made
> - Ruff: List of fixed issues, or message indicating no issues found
> 
> **Rollback/Safety notes:** The automation modifies files, but changes are generally safe (formatting and auto-fixable linting issues). For safety, ensure code is committed before running. If unwanted changes occur, use `git checkout -- <file>` to revert specific files. Black and Ruff are industry-standard tools that preserve code functionality while improving style.

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before (Manual Workflow):** Developers had to manually run separate commands (`cd backend && black . && ruff check . --fix`), remember the correct syntax for each tool, and handle any errors individually. This was time-consuming and inconsistent, with some developers forgetting to run linting or using different formatting options.
> 
> **After (Automated Workflow):** A single `/fix-code` command handles both formatting and linting automatically, ensuring all team members apply the same standards consistently. The automation reduces the chance of human error and makes code quality maintenance effortless.

e. How you used the automation to enhance the starter application
> I used the /fix-code automation after implementing the /status endpoint. After writing the new endpoint code, I ran `/fix-code` to ensure the code followed proper formatting standards and didn't have any linting issues. The automation automatically formatted the code and fixed any style issues, ensuring the new endpoint code was consistent with the rest of the codebase and ready for commit.
> TODO


### *(Optional) Automation #3*
*If you choose to build additional automations, feel free to detail them here!*

a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> TODO

b. Design of each automation, including goals, inputs/outputs, steps
> TODO

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> TODO

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> TODO

e. How you used the automation to enhance the starter application
> TODO
