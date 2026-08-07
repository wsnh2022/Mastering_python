# Python Automation Engineer Checklist (2026) – v3

A living checklist. Tick items as you gain confidence. Focus on understanding and application, not memorization.

---

## Phase 0 – Setup & Basics

- [ ] Install Python (3.12+) and a code editor (VS Code / PyCharm)
- [ ] Run Python scripts from the terminal
- [ ] Use the command line on your OS (PowerShell or Linux/macOS shell)
- [ ] Install packages with `pip`
- [ ] Create and activate a virtual environment
- [ ] Try `uv` as a faster alternative to pip + venv
- [ ] Initialize a Git repository
- [ ] Stage and commit changes
- [ ] Write meaningful commit messages
- [ ] Create a GitHub account and push a repo

*Why git this early: you'll be writing real projects by Phase 2. Committing from day one is a cheap habit to build and an expensive one to retrofit.*

---

## Phase 1 – Python Foundations

- [ ] Variables and basic data types (int, float, str, bool)
- [ ] Arithmetic and comparison operators
- [ ] Conditional statements (`if/elif/else`)
- [ ] Lists (create, index, slice, append, iterate)
- [ ] Tuples (create, unpack, use as immutable sequences)
- [ ] Dictionaries (create, access, update, iterate)
- [ ] Sets (create, add, membership tests)
- [ ] `for` loops (iterate over sequences and ranges)
- [ ] `while` loops (basic usage and exit conditions)
- [ ] Functions (parameters, return values, default arguments)
- [ ] Scope (local vs global variables)
- [ ] Context managers (`with` statements) - why they matter for files, connections, locks
- [ ] Reading and writing text files
- [ ] Reading and writing CSV files with the `csv` module
- [ ] Basic exception handling (`try/except`)
- [ ] Using `else` and `finally` with `try` blocks
- [ ] Raising exceptions (`raise`)
- [ ] Creating custom exception classes
- [ ] Importing modules and packages
- [ ] Using `__name__ == "__main__"`
- [ ] Basic classes (attributes and methods)
- [ ] Creating and using instances
- [ ] Type hints for function signatures (basic usage, not full generics)
- [ ] Read and explain a 100–200 line beginner script
- [ ] Commit each milestone script to your Phase 0 repo

---

## Phase 2 – Automation Fundamentals

### File & System Automation

- [ ] `pathlib.Path` (paths, files, directories)
- [ ] Listing files and filtering by extension
- [ ] Creating, moving, renaming, and deleting files
- [ ] Creating and cleaning directories
- [ ] Using `os` and `shutil` for advanced file operations

### Data & APIs

- [ ] Reading and writing JSON files
- [ ] Making GET requests with `requests`
- [ ] Making POST requests with `requests`
- [ ] Sending headers and query parameters
- [ ] Handling HTTP errors and timeouts
- [ ] Parsing JSON API responses
- [ ] Storing config in a `.env` file
- [ ] Loading environment variables with `python-dotenv`
- [ ] Never hard-code paths or credentials - use env vars from the start
- [ ] Basic logging with `logging` (levels: DEBUG, INFO, WARNING, ERROR)
- [ ] Writing logs to a file
- [ ] Using rotating file handlers

*This is the only place `.env` mechanics are taught. Later phases reference this habit rather than re-teaching it.*

### Testing Fundamentals (moved up from Phase 4)

- [ ] Install and run `pytest`
- [ ] Write simple test functions
- [ ] Use assertions in tests
- [ ] Use fixtures for setup/teardown
- [ ] Parametrize tests
- [ ] Run tests with verbose output
- [ ] Write unit tests for your Phase 2 functions (file ops, API parsing)
- [ ] Keep tests independent (no shared state)

*Why here: Phase 3 has you using `pytest-playwright` fixtures. You should understand what a fixture is in plain pytest before it shows up wrapped in browser-automation syntax.*

### Async Basics

- [ ] Understand why async matters for I/O-bound automation (many API calls, many pages)
- [ ] `async`/`await` syntax basics
- [ ] Concurrent requests with `httpx.AsyncClient` or `aiohttp`
- [ ] Know when async is worth the complexity and when sync is fine (most small scripts: sync is fine)

### Data Processing (pandas)

- [ ] Reading CSV files with `pandas`
- [ ] Reading Excel files with `pandas`
- [ ] Filtering rows by conditions
- [ ] Selecting and renaming columns
- [ ] Grouping and aggregating data
- [ ] Handling missing values
- [ ] Exporting DataFrames to CSV
- [ ] Exporting DataFrames to Excel

### Small Projects

- [ ] File organizer (by extension or date)
- [ ] Folder cleaner with logging
- [ ] CSV processor (clean/transform/summarize)
- [ ] API data fetcher + CSV/Excel report generator
- [ ] Simple CLI tool with `argparse` or `click`
- [ ] Each project: own git commits, `.env` for any secrets, at least one pytest test

---

## Phase 3 – Browser & Web Automation

### Web & HTML Basics

- [ ] Inspect HTML with browser DevTools
- [ ] Understand basic HTML structure (tags, attributes, classes, ids)
- [ ] Understand CSS selectors (id, class, attribute, hierarchy)
- [ ] Use `requests` + `BeautifulSoup` for static pages
- [ ] Extract text, links, and tables from HTML
- [ ] Handle simple pagination in scrapers
- [ ] Respect `robots.txt` and rate limits; know when scraping ToS matters

### Playwright (Primary Tool)

- [ ] Install Playwright for Python and browsers
- [ ] Launch a browser and create a page
- [ ] Navigate to a URL
- [ ] Use role-based locators (button, link, textbox, etc.)
- [ ] Click elements and fill inputs
- [ ] Use text and test-id locators
- [ ] Rely on auto-waiting (no manual sleeps)
- [ ] Write basic assertions on page content
- [ ] Take screenshots on failure
- [ ] Enable and view trace on failure
- [ ] Use `pytest-playwright` fixtures (builds directly on Phase 2 pytest fundamentals)
- [ ] Save and reuse authentication state (storage state)
- [ ] Run tests across multiple browsers

### Playwright Best Practices

- [ ] Prefer role-based locators over CSS/XPath where possible
- [ ] Trust auto-waiting; avoid `time.sleep()` from the start, not as a later fix
- [ ] Understand Page Object Model (POM) concept
- [ ] Separate page actions from test assertions
- [ ] Use codegen for quick scaffolding, then refactor by hand
- [ ] Combine API calls (for setup) with UI tests (for flows)

### Selenium (Legacy/Optional)

- [ ] Install Selenium and a WebDriver
- [ ] Launch a browser and navigate
- [ ] Locate elements (id, name, CSS, XPath)
- [ ] Click and send keys
- [ ] Understand explicit waits (`WebDriverWait`)
- [ ] Know when Selenium is still needed (legacy projects)

### Projects

- [ ] Login automation for a demo site
- [ ] Form filling automation (repeatable workflow)
- [ ] Static site scraper (requests + BeautifulSoup)
- [ ] Dynamic site scraper (Playwright)
- [ ] Automated report download from a dashboard
- [ ] One end-to-end business workflow (multi-step)

---

## Phase 4 – Professional Engineering Skills

### Git Workflows (basics were Phase 0 - this is the rest)

- [ ] Create and switch branches
- [ ] Merge branches
- [ ] Use a feature-branch workflow (even solo)
- [ ] Write a `.gitignore` (venvs, `.env`, cache files)

### Dependency Management

- [ ] Freeze dependencies (`requirements.txt`) or use `pyproject.toml`
- [ ] Install dependencies from a requirements file on a fresh machine
- [ ] Document environment setup in README

### Code Quality

- [ ] Set up `ruff` for linting and formatting
- [ ] Run `mypy` (or rely on your editor) for basic type checking
- [ ] Understand why consistent style matters for client-facing code

### Debugging & Logging

- [ ] Use the IDE debugger (breakpoints, step-through)
- [ ] Inspect variables during debugging
- [ ] Add descriptive log messages
- [ ] Log errors and stack traces
- [ ] Use structured (JSON) logs where useful

### Testing in Practice

*(Fundamentals were Phase 2 - this is applying them at project scale)*

- [ ] Write a few Playwright tests for critical flows
- [ ] Organize a growing test suite into files/folders sensibly
- [ ] Decide what's worth testing vs what isn't (diminishing returns)

### Secrets Management (principles - mechanics were Phase 2)

- [ ] Basic understanding of secret management beyond `.env` (vaults, CI secrets)
- [ ] Never commit secrets - set up `.gitignore` before your first `.env` file, not after
- [ ] Document required env vars in README without exposing values

### Documentation

- [ ] Write a clear README (setup, usage, examples)
- [ ] Document environment variables
- [ ] Add a short "architecture" note (what runs, when, how errors are handled)
- [ ] Add usage examples and sample commands

### Docker Basics

- [ ] Write a simple `Dockerfile` for a Python script
- [ ] Build a Docker image
- [ ] Run a container locally
- [ ] Use volume mounts for input/output folders
- [ ] Understand when Docker is useful (consistent environments)

### CI/CD Basics

- [ ] Understand what CI/CD is (continuous integration/deployment)
- [ ] Create a basic GitHub Actions workflow
- [ ] Run tests on push to a branch
- [ ] View CI logs and debug failing jobs

---

## Phase 5 – Scaling, Data & Orchestration (Optional but Powerful)

### Scheduling & Orchestration

- [ ] Use `schedule` or `APScheduler` for simple cron-like jobs
- [ ] Understand cron (Linux/macOS) or Task Scheduler (Windows)
- [ ] Design idempotent scripts (safe to re-run)
- [ ] Add retry logic for flaky APIs or network calls
- [ ] Build a multi-step workflow (fetch → transform → load → notify)

### Databases & SQL

- [ ] Basic SQL (SELECT, INSERT, UPDATE, DELETE)
- [ ] Connect to a SQLite database from Python
- [ ] Execute queries with `sqlite3` or `SQLAlchemy`
- [ ] Read data into a pandas DataFrame
- [ ] Write DataFrames back to a database table

### Monitoring & Notifications

- [ ] Add simple health checks (log entry, status file)
- [ ] Send email notifications on failure/completion
- [ ] Send notifications via Telegram or Slack webhooks

### Projects

- [ ] Daily or weekly automated report pipeline
- [ ] Multi-step workflow with notifications
- [ ] One robust script that runs unattended for weeks

---

## Phase 6 – Test Suite Maintenance & Quality

- [ ] Identify and fix flaky tests
- [ ] Remove duplicated setup/teardown code
- [ ] Split oversized fixtures into smaller ones
- [ ] Delete or skip obsolete tests
- [ ] Keep test suite fast and focused
- [ ] Run tests across browsers in CI

---

## Phase 7 – Portfolio & Career Readiness

- [ ] 3–5 automation projects on GitHub with READMEs
- [ ] At least one browser automation project (Playwright)
- [ ] At least one data/CSV automation project (with pandas)
- [ ] One "client-style" project with clear requirements
- [ ] One project with tests, logging, and config management
- [ ] Short write-ups explaining what each project does
- [ ] Basic understanding of SDLC and testing concepts
- [ ] Know common testing types (unit, integration, regression)
- [ ] Understand severity vs priority for defects
- [ ] Basic familiarity with JIRA or similar tools (optional)
- [ ] Prepare a simple resume highlighting automation projects
- [ ] Practice explaining your projects out loud

---

## AI Workflow Habits

- [ ] Attempt tasks yourself before asking AI
- [ ] Share code + error + what you tried + specific question
- [ ] Ask AI to explain, not just fix
- [ ] Refactor AI-suggested code yourself
- [ ] Add at least one test after AI-assisted changes
- [ ] Use AI to review logic and suggest improvements

---

## The Learning Loop (Per Topic)

- [ ] Learned the concept (docs/tutorial)
- [ ] Built a small project using it
- [ ] Intentionally broke the project
- [ ] Debugged the resulting errors
- [ ] Improved the design (functions, config, logging)
- [ ] Explained the code aloud or wrote a short note
- [ ] Moved to the next topic

---

## Daily Mindset (Quick Check)

Each study day, jot down:

- [ ] Concept learned
- [ ] What I built
- [ ] Bug I fixed
- [ ] Mistake that taught me something
- [ ] One thing to improve tomorrow

---
