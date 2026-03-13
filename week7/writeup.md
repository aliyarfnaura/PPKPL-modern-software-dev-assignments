# Week 7 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **TODO** \
SUNet ID: **TODO** \
Citations: **TODO**

This assignment took me about **TODO** hours to do. 


## Task 1: Add more endpoints and validations
a. Links to relevant commits/issues
> Pull Request: https://github.com/aliyarfnaura/PPKPL-modern-software-dev-assignments/pull/1

Branch: task1-add-endpoints
Commit: Implement additional endpoints with validation and error handling.

b. PR Description
> This pull request implements Task 1 from week7/docs/TASKS.md. The objective of this task is to add additional API endpoints and improve input validation and error handling in the application.

New endpoints were implemented following the existing FastAPI project structure, and input validation was added using Pydantic models. Error handling was also introduced to ensure the API properly handles invalid inputs and missing resources.

Testing was performed using pytest, and all tests passed successfully. The implementation maintains consistency with the existing architecture to ensure readability and maintainability of the codebase.

c. Graphite Diamond generated code review
> The Graphite Diamond AI review did not report any issues for this pull request. This indicates that the implementation follows acceptable coding practices and does not contain obvious structural or security problems.

Although no issues were flagged by the AI reviewer, a manual review was still performed to verify endpoint behavior, validation logic, and overall correctness of the implementation.

## Task 2: Extend extraction logic
a. Links to relevant commits/issues
> Pull Request: https://github.com/aliyarfnaura/PPKPL-modern-software-dev-assignments/pull/2

Branch: task2-extend-extraction
Commit: Extend action item extraction logic with additional pattern recognition.

b. PR Description
> This pull request implements Task 2 from week7/docs/TASKS.md, which aims to enhance the action item extraction logic with more advanced pattern recognition.

The extraction logic was improved by adding additional pattern matching to detect action-related keywords, possible deadlines, and task-like sentences within the input text. The implementation keeps the logic modular so that future improvements and additional patterns can be easily added.

Testing was performed using pytest, and all tests passed successfully.

c. Graphite Diamond generated code review
> Graphite Diamond performed an automated code review on this pull request and did not report any issues. The AI review indicated that the code changes follow acceptable coding practices and do not introduce structural or security concerns.

A manual review was still conducted to verify the correctness of the extraction logic and ensure that the implementation integrates properly with the existing system.

## Task 3: Try adding a new model and relationships
a. Links to relevant commits/issues
> TODO

b. PR Description
> TODO

c. Graphite Diamond generated code review
> TODO

## Task 4: Improve tests for pagination and sorting
a. Links to relevant commits/issues
> TODO

b. PR Description
> TODO

c. Graphite Diamond generated code review
> TODO

## Brief Reflection 
a. The types of comments you typically made in your manual reviews (e.g., correctness, performance, security, naming, test gaps, API shape, UX, docs).
> TODO 

b. A comparison of **your** comments vs. **Graphite’s** AI-generated comments for each PR.
> TODO

c. When the AI reviews were better/worse than yours (cite specific examples)
> TODO

d. Your comfort level trusting AI reviews going forward and any heuristics for when to rely on them.
>TODO 



