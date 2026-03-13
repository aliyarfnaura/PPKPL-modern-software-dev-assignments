# Week 5 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **Aliya Raffa Naura Ayu** \
SUNet ID: **N/A** \
Citations: **Warp Documentation (warp.dev), FastAPI Documentation, Pytest Documentation**

This assignment took me about **4-5 hours** hours to do. 


## YOUR RESPONSES
### Automation A: Warp Drive saved prompts, rules, MCP servers

a. Design of each automation, including goals, inputs/outputs, steps
> For this automation, I created a Warp Drive workflow command that automatically runs code formatting, lint checks, and tests for the project. The goal of this automation is to simplify the development workflow by combining several common development tasks into a single command.

The input for this automation is the codebase in the backend directory. The output is the result of formatting checks, lint results, and unit test results.

The automation uses the following command:

black backend; ruff check backend --fix; python -m pytest backend/tests -q

Steps performed by the automation:
1. Run Black to ensure the code formatting is consistent.
2. Run Ruff to perform lint checking and automatically fix minor issues.
3. Run Pytest to execute all backend tests.
4. Provide a summary of the results.

This automation helps streamline the development process by running multiple validation steps automatically.

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> Before using this automation, developers had to run multiple commands manually, such as:

black backend
ruff check backend
pytest backend/tests

This process required running each command separately and it was easy to forget one of the steps.

After implementing the Warp Drive automation, all of these steps can be executed with a single command. This makes the development workflow faster, more consistent, and easier to manage.

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> The automation runs with controlled autonomy. Warp executes the commands automatically, but the developer still supervises the results shown in the terminal.

The permissions used are limited to running development commands such as formatting, lint checking, and testing within the repository. Since the automation does not make large structural changes to the codebase, the risk level is relatively low.

The developer monitors the output to make sure the commands run successfully and that no errors occur.

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> This automation was used together with a multi-agent workflow in Warp.

In this setup:

Agent 1 was responsible for implementing tasks from docs/TASKS.md.
Agent 2 was responsible for running tests and validating code quality using the automation workflow.

Both agents operated in separate Warp tabs, allowing tasks to be performed in parallel.

The main advantage of this setup is improved development speed because feature implementation and validation can happen at the same time. A potential risk is conflicting changes, but this can be mitigated by reviewing changes before committing them.

e. How you used the automation (what pain point it resolves or accelerates)
> This automation was mainly used to speed up the validation process after making changes to the repository.

Normally, developers would need to manually run multiple commands to ensure the code is properly formatted, free of lint issues, and that all tests pass.

By using this automation, all of these checks can be performed with a single command. This significantly improves efficiency and reduces the chance of forgetting important validation steps before committing code.



### Automation B: Multi‑agent workflows in Warp 

a. Design of each automation, including goals, inputs/outputs, steps
> The second automation focuses on multi-agent workflows using Warp to handle development tasks in parallel.

In this workflow, two agents were used:

Agent 1 was responsible for reading docs/TASKS.md and implementing one of the selected tasks in the backend.
Agent 2 was responsible for running tests and verifying code quality using the automation workflow.

The input for this workflow is the project repository and the tasks listed in docs/TASKS.md. The output includes updated backend code and test results verifying that the implementation works correctly.

Steps in the workflow:

1. Agent 1 reads docs/TASKS.md.
2. Agent 1 selects a task to implement.
3. Agent 1 modifies the backend code.
4. Agent 2 runs tests and lint checks.
5. Agent 2 summarizes the validation result 

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> Before using the multi-agent workflow, developers would typically implement features first and then run tests afterward.

With the multi-agent workflow, feature implementation and testing can run in parallel in separate Warp tabs. This allows developers to validate changes more quickly and reduces the overall development time.

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> The agents were given permission to read the repository, run testing commands, and suggest code changes.

However, the developer remained responsible for supervising the agents’ actions and reviewing any modifications before finalizing them.

This setup allows automation to assist with development tasks while still maintaining human oversight.

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> The multi-agent workflow was implemented by opening multiple Warp tabs.

The roles of the agents were:

Agent 1
→ responsible for implementing tasks from docs/TASKS.md.

Agent 2
→ responsible for running tests and validating code quality.

The coordination strategy involved letting Agent 1 implement changes while Agent 2 focused on verifying the results.

The main benefit of this concurrency approach is improved efficiency, since development and validation tasks can run simultaneously.

e. How you used the automation (what pain point it resolves or accelerates)
> The multi-agent workflow helps speed up development by allowing multiple tasks to run at the same time.

Normally, developers need to finish implementation before running tests. With multi-agent workflows, testing and validation can start almost immediately while development continues.

This approach makes the development process faster, more organized, and easier to manage as projects grow.


### (Optional) Automation C: Any Additional Automations
a. Design of each automation, including goals, inputs/outputs, steps
> TODO

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> TODO

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> TODO

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> TODO

e. How you used the automation (what pain point it resolves or accelerates)
> TODO

