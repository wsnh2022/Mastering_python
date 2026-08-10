# Automation Engineer Quick Reference (2026)

**Term → 1-line meaning → sample AI prompt**

Keep this as a daily reference while building automation projects.

---

# Core Programming

| Term        | 1-line explanation                                       | Sample AI prompt                                                                   |
| ----------- | -------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Function    | A reusable block of code that performs one task.         | `Refactor this script into small single-purpose functions with clear names.`       |
| Module      | A Python file that groups related functions and classes. | `Split this automation script into modules for API, file handling, and reporting.` |
| Variable    | A named value used during program execution.             | `Rename variables in this script to make their purpose obvious.`                   |
| Loop        | Repeats actions over a collection of items.              | `Explain this loop line by line and suggest a cleaner version.`                    |
| Conditional | Runs different code based on a condition.                | `Simplify these nested if statements without changing behavior.`                   |

---

# Data Handling

| Term       | 1-line explanation                                               | Sample AI prompt                                                      |
| ---------- | ---------------------------------------------------------------- | --------------------------------------------------------------------- |
| List       | Ordered collection of items.                                     | `Show me how to process each row in this list of dictionaries.`       |
| Dictionary | Key-value data structure used heavily with JSON APIs.            | `Extract name, email, and amount safely from this API response.`      |
| Set        | Collection of unique values.                                     | `Remove duplicate customer IDs using a set and explain why it works.` |
| JSON       | Standard text format for exchanging structured data.             | `Parse this JSON response and convert it into a pandas DataFrame.`    |
| CSV        | Comma-separated text file commonly used for reports and exports. | `Read this CSV, clean missing emails, and save the cleaned file.`     |

---

# File Automation

| Term       | 1-line explanation                             | Sample AI prompt                                                            |
| ---------- | ---------------------------------------------- | --------------------------------------------------------------------------- |
| Path       | The location of a file or folder.              | `Rewrite this code using pathlib instead of os.path.`                       |
| Read/Write | Loading data from a file and saving data back. | `Create a safe read-write workflow with UTF-8 encoding and error handling.` |
| Backup     | A copy of data kept before modification.       | `Add automatic backup creation before this script edits any files.`         |

---

# APIs & Integration

| Term           | 1-line explanation                                       | Sample AI prompt                                                            |
| -------------- | -------------------------------------------------------- | --------------------------------------------------------------------------- |
| API            | A service interface that allows programs to communicate. | `Write a Python requests example that calls this API and handles failures.` |
| Endpoint       | The specific URL of an API operation.                    | `Document the purpose and expected response of this endpoint.`              |
| Request        | Data sent to an API.                                     | `Build a POST request with headers, authentication, and JSON payload.`      |
| Response       | Data returned by an API.                                 | `Validate this API response before processing it.`                          |
| Status Code    | Numeric result of an HTTP request.                       | `Explain common HTTP status codes and add handling for 401, 404, and 500.`  |
| Authentication | Verifying identity when calling a service.               | `Store this API key securely using environment variables.`                  |
| Webhook        | An HTTP callback triggered by an event.                  | `Create a Flask webhook endpoint that logs incoming events.`                |

---

# Browser Automation

| Term       | 1-line explanation                                             | Sample AI prompt                                                               |
| ---------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Playwright | Modern browser automation framework for testing and workflows. | `Write a Playwright script that logs in and downloads a report.`               |
| Selector   | A rule that identifies an element on a page.                   | `Generate stable Playwright locators for this HTML snippet.`                   |
| Wait       | Pausing until a page or element is ready.                      | `Replace fixed sleeps with proper Playwright wait conditions.`                 |
| Headless   | Running a browser without showing the UI.                      | `Run this Playwright script in headless mode and save screenshots on failure.` |
| DOM        | The page structure that automation tools interact with.        | `Explain how this selector maps to the DOM structure.`                         |

---

# Reliability Engineering

| Term        | 1-line explanation                                   | Sample AI prompt                                                       |
| ----------- | ---------------------------------------------------- | ---------------------------------------------------------------------- |
| Exception   | An error that interrupts normal execution.           | `Add try/except blocks with meaningful error messages.`                |
| Logging     | Recording what the automation is doing.              | `Add INFO, WARNING, and ERROR logging to this script.`                 |
| Timeout     | Maximum time to wait for an operation.               | `Add request and browser timeouts with clear failure messages.`        |
| Retry       | Trying an operation again after a temporary failure. | `Implement retry logic with exponential backoff.`                      |
| Validation  | Checking that data is correct before using it.       | `Validate required columns and data types before processing this CSV.` |
| Idempotency | Running the automation multiple times safely.        | `Make this import process idempotent using a unique invoice ID.`       |

---

# Testing & Debugging

| Term            | 1-line explanation                                  | Sample AI prompt                                               |
| --------------- | --------------------------------------------------- | -------------------------------------------------------------- |
| Unit Test       | Automated test for a small piece of code.           | `Write pytest unit tests for this function.`                   |
| Assertion       | A check that verifies expected behavior.            | `Add assertions for valid and invalid inputs.`                 |
| Regression Test | A test that ensures a previous bug does not return. | `Create a regression test for this bug scenario.`              |
| Breakpoint      | A pause point used during debugging.                | `Explain where to place breakpoints to debug this function.`   |
| Stack Trace     | The call history shown when an error occurs.        | `Analyze this stack trace and identify the likely root cause.` |

---

# Configuration & Security

| Term                 | 1-line explanation                                      | Sample AI prompt                                                      |
| -------------------- | ------------------------------------------------------- | --------------------------------------------------------------------- |
| Environment Variable | External configuration value provided to the program.   | `Load API keys from a .env file using python-dotenv.`                 |
| Secret               | Sensitive information such as passwords or tokens.      | `Review this script for hardcoded secrets and replace them securely.` |
| Config File          | File that stores runtime settings separately from code. | `Create a config.yaml structure for this automation project.`         |

---

# Workflow Automation

| Term          | 1-line explanation                                   | Sample AI prompt                                               |
| ------------- | ---------------------------------------------------- | -------------------------------------------------------------- |
| Workflow      | A sequence of automated steps.                       | `Design a workflow: fetch → transform → save → notify.`        |
| Scheduler     | Tool that runs automation at a specific time.        | `Schedule this script daily at 8 AM using APScheduler.`        |
| Trigger       | Event that starts a workflow.                        | `List possible triggers for this invoice automation process.`  |
| Orchestration | Coordinating multiple automation tasks.              | `Convert these scripts into a Prefect flow with dependencies.` |
| Queue         | Temporary storage for tasks waiting to be processed. | `Explain when a task queue is useful in automation systems.`   |

---

# Observability

| Term         | 1-line explanation                              | Sample AI prompt                                                               |
| ------------ | ----------------------------------------------- | ------------------------------------------------------------------------------ |
| Monitoring   | Watching system health continuously.            | `Suggest metrics to monitor for this automation pipeline.`                     |
| Alert        | Notification when something goes wrong.         | `Create an alert strategy for repeated job failures.`                          |
| Dashboard    | Visual view of logs and metrics.                | `Design a simple Grafana dashboard for this workflow.`                         |
| Health Check | Quick test that confirms the system is working. | `Add a health-check endpoint that returns OK when dependencies are reachable.` |

---

# Cloud & Deployment

| Term       | 1-line explanation                                  | Sample AI prompt                                                               |
| ---------- | --------------------------------------------------- | ------------------------------------------------------------------------------ |
| Docker     | Packages the application with its dependencies.     | `Write a Dockerfile for this Python automation project.`                       |
| Container  | A running isolated application environment.         | `Explain how this script behaves inside a container.`                          |
| Deployment | Releasing automation to a server or cloud platform. | `Create a deployment checklist for this automation service.`                   |
| Serverless | Running code only when triggered.                   | `Explain whether this workflow is a good candidate for a serverless function.` |

---

# AI-Assisted Engineering

| Term             | 1-line explanation                                         | Sample AI prompt                                                            |
| ---------------- | ---------------------------------------------------------- | --------------------------------------------------------------------------- |
| Prompt           | Instruction given to an AI model.                          | `Improve this prompt to get production-quality Python code.`                |
| Prompt Template  | Reusable prompt structure for consistent results.          | `Create a reusable prompt template for API automation tasks.`               |
| Refactor         | Improve code structure without changing behavior.          | `Refactor this script for readability and maintainability.`                 |
| Code Review      | Evaluating code quality and risks.                         | `Review this code for bugs, security issues, and maintainability concerns.` |
| RAG              | AI answers questions using your own documents.             | `Design a simple RAG assistant for company SOP documents.`                  |
| Embedding        | Numeric representation of text for similarity search.      | `Explain embeddings in simple terms for an automation engineer.`            |
| Vector Database  | Database optimized for similarity search on embeddings.    | `Compare Qdrant and Chroma for a small internal RAG project.`               |
| Agentic Workflow | AI can choose actions and use tools within defined limits. | `Design a safe agentic workflow for processing support tickets.`            |
| Tool Calling     | AI invokes external functions or APIs.                     | `Show a Python example of an LLM calling a weather API tool.`               |

---

# Daily “Always-Ready” Prompt

Use this when working on almost any automation task.

```text
You are a senior Python Automation Engineer.

Goal: <describe the task>

Inputs: <files, API data, user input>
Expected output: <report, CSV, database update, email, etc.>
Constraints: Python 3.12, pathlib, requests/httpx, pandas where useful, logging, type hints, error handling, retries, idempotency, and clear function structure.

Tasks:
1. Explain the approach.
2. Write production-quality code.
3. Add logging and validation.
4. Add basic tests.
5. List edge cases and operational risks.
6. Suggest future improvements.
```

---

# The 15 Terms You Should Recall Instantly

If you can explain these without notes, you are already thinking like a professional automation engineer:

* API
* JSON
* Function
* Module
* Exception
* Logging
* Timeout
* Retry
* Idempotency
* Validation
* Workflow
* Scheduler
* Test
* Docker
* Prompt

These 15 terms appear in the majority of real-world automation projects.
