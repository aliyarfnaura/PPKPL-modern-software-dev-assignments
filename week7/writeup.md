# Week 7 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **Aliya Raffa Naura Ayu** \
SUNet ID: **N/A** \
Citations: **AI tools used for assistance (Warp AI and Graphite AI).**

This assignment took me about **3 hours** to do. 


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
> Pull Request: https://github.com/aliyarfnaura/PPKPL-modern-software-dev-assignments/pull/3

Branch: task3-add-models  
Commit: Add new database models and relationships using SQLAlchemy.

b. PR Description
> This pull request implements Task 3 from week7/docs/TASKS.md, which introduces a new database model and defines relationships with existing models in the application.

A new SQLAlchemy model was created following the existing project structure, including appropriate fields and a primary key. Relationships were defined between the new model and existing models to support relational data access.

The FastAPI application was updated to support interactions with the new model where necessary. Testing was performed using pytest, and all tests passed successfully. The implementation follows the current FastAPI and SQLAlchemy architecture to maintain consistency across the codebase.

c. Graphite Diamond generated code review
> Graphite Diamond performed an automated code review on this pull request and did not report any issues. This suggests that the structure of the new model, relationships, and integration with the existing codebase follow acceptable coding practices.

In addition to the automated review, a manual review was conducted to verify the correctness of the relationships and ensure that the new model integrates properly with the existing application logic.


## Task 4: Improve tests for pagination and sorting
a. Links to relevant commits/issues
> Pull Request: https://github.com/aliyarfnaura/PPKPL-modern-software-dev-assignments/pull/4

Branch: task4-improve-tests  
Commit: Improve pagination and sorting tests.

b. PR Description
> This pull request implements Task 4 from week7/docs/TASKS.md, which focuses on improving test coverage for pagination and sorting functionality in the application.

Additional test cases were added to validate the behavior of pagination using page and limit parameters. Sorting functionality was also tested to ensure that results are correctly returned in both ascending and descending order.

Edge cases such as empty results and invalid parameters were considered to ensure the application handles these scenarios properly.

Testing was performed using pytest, and all tests passed successfully.

c. Graphite Diamond generated code review
> Graphite Diamond performed an automated code review on this pull request and did not report any issues. This indicates that the additional test cases follow acceptable testing practices and integrate well with the existing test structure.

A manual review was also performed to ensure that the new tests correctly validate pagination and sorting behavior and improve the overall reliability of the application's test coverage.


## Brief Reflection 

a. The types of comments you typically made in your manual reviews (e.g., correctness, performance, security, naming, test gaps, API shape, UX, docs).

> During my manual review, I mainly focused on checking the correctness of the implementation and whether the new code fit well with the existing project structure. I also paid attention to naming consistency, basic input validation, and whether the logic would break existing functionality. In some cases I also checked whether the tests were sufficient to cover the new functionality that was introduced.

b. A comparison of **your** comments vs. **Graphite’s** AI-generated comments for each PR.

> In my case, Graphite’s AI-generated reviews did not report any issues for the pull requests. My manual review was more focused on verifying that the features worked as expected and that the implementation followed the project’s structure. Because Graphite did not flag any problems, the comparison mainly showed that both the manual review and AI review agreed that the code changes were acceptable and did not introduce obvious issues.

c. When the AI reviews were better/worse than yours (cite specific examples)

> In this assignment, Graphite’s AI review did not provide additional suggestions beyond confirming that no issues were found. Because of that, my manual review played a more important role in verifying the behavior of the implemented features, such as checking that the new endpoints, extraction logic, and tests behaved correctly. However, the AI review was still useful as an additional validation step to confirm that there were no obvious structural or code quality problems.

d. Your comfort level trusting AI reviews going forward and any heuristics for when to rely on them.

> This assignment made me realize that using AI tools like Warp for coding and Graphite for code review can make the development process feel much smoother. It feels more efficient because the AI can help generate or review code quickly, while I can focus on understanding the logic and verifying that everything works correctly.

> Going forward, I would feel comfortable using AI reviews as a supporting tool, especially for catching common issues or verifying code quality. However, I would still rely on manual review to ensure that the implementation truly meets the intended functionality and integrates correctly with the rest of the system.