# Python Automation Engineer Checklist (2026)

A living checklist. Tick items as you gain confidence. Focus on understanding and application, not memorization.

**Pace: 1-2 hours/day. Day ranges below are estimates, not deadlines - move on when the checklist items feel solid, not when the calendar says so.**

**Format: each item has a short note after the dash explaining what it means or why it matters. If a note doesn't make sense yet, that's a signal to slow down on that item, not skip it.**

---
### 3 Operating Principles (Read First - Apply Every Day)

*These three sections aren't a phase you complete and move past. They're how you should be working through every phase below, starting Day 1. Skim them now, then come back and re-read them after your first week - they'll mean more once you have something real to apply them to.*

### 1. AI Workflow Habits
*Ongoing - apply from Day 1 onward, not a separate block of days*
- [ ] Attempt tasks yourself before asking AI - builds the underlying skill instead of just outsourcing it
- [ ] Share code + error + what you tried + specific question - better context gets better answers, from AI or humans
- [ ] Ask AI to explain, not just fix - understanding the "why" is what actually sticks
- [ ] Refactor AI-suggested code yourself - retyping and adjusting it forces you to actually process it
- [ ] Add at least one test after AI-assisted changes - verify the AI's suggestion actually works as claimed
- [ ] Use AI to review logic and suggest improvements - a second pair of eyes on your own reasoning, not just a code generator

---
### 2. The Learning Loop (Per Topic)
*Ongoing - repeat for each topic throughout all phases*
- [ ] Learned the concept (docs/tutorial) - get the basic idea from a reliable source first
- [ ] Built a small project using it - apply it immediately; concepts that aren't used are quickly forgotten
- [ ] Intentionally broke the project - change something on purpose and see what error you get; builds intuition for debugging
- [ ] Debugged the resulting errors - actually fix what you broke, don't just revert it
- [ ] Improved the design (functions, config, logging) - go back and clean up once it works, don't leave it at "barely functional"
- [ ] Explained the code aloud or wrote a short note - if you can't explain it simply, you don't fully understand it yet
- [ ] Moved to the next topic - avoid getting stuck perfecting one thing indefinitely

---
### 3. Daily Mindset (Quick Check)
*Every single day*

Each study day, jot down:
- [ ] Concept learned - one sentence on what you covered today
- [ ] What I built - even something tiny counts
- [ ] Bug I fixed - the specific problem and what actually solved it
- [ ] Mistake that taught me something - honest reflection, not just wins
- [ ] One thing to improve tomorrow - keeps momentum pointed forward

---
## Phase 0 – Setup & Basics
*Days 1-2*
- [x] Install Python (3.12+) and a code editor (VS Code / PyCharm) - your two core tools; everything else runs through these
- [x] Run Python scripts from the terminal - `python script.py`, not just clicking "run" in an editor; you need this for automation later
- [x] Use the command line on your OS (PowerShell or Linux/macOS shell) - navigating folders (`cd`), listing files (`ls`/`dir`), running commands
- [x] Install packages with `pip` - `pip install requests`; how you add libraries other people wrote
- [ ] Create and activate a virtual environment - `python -m venv venv`; keeps each project's packages isolated so they don't conflict
- [ ] Try `uv` as a faster alternative to pip + venv - newer tool, does the same job much faster; worth adopting early
- [ ] Initialize a Git repository - `git init`; turns a folder into something Git can track changes in
- [ ] Stage and commit changes - `git add` + `git commit`; saves a snapshot of your code with a message
- [ ] Write meaningful commit messages - "fix CSV parsing bug" not "update"; future-you will thank present-you
- [ ] Create a GitHub account and push a repo - your code's public home; also doubles as your portfolio later

*Why git this early: you'll be writing real projects by Phase 2. Committing from day one is a cheap habit to build and an expensive one to retrofit.*

---

## Phase 1 – Python Foundations
*Days 3-22 (~20 days)*

- [ ] Variables and basic data types (int, float, str, bool) - naming and storing values; the atoms everything else is built from
- [ ] Arithmetic and comparison operators - `+ - * / ==  != < >`; math and logic checks
- [ ] Conditional statements (`if/elif/else`) - branching logic: "do this if that's true, otherwise do this"
*Days 3-4*

- [ ] Lists (create, index, slice, append, iterate) - ordered, changeable collections; `my_list[0]`, `my_list.append(x)`
- [ ] Tuples (create, unpack, use as immutable sequences) - like lists but can't be changed after creation; good for fixed data like coordinates
- [ ] Dictionaries (create, access, update, iterate) - key-value pairs, like `{"name": "Alice"}`; how you'll model most real-world data
- [ ] Sets (create, add, membership tests) - unordered collections with no duplicates; fast for checking "is this in here?"
*Days 5-7*

- [ ] `for` loops (iterate over sequences and ranges) - repeat an action for each item in a list, string, or range of numbers
- [ ] `while` loops (basic usage and exit conditions) - repeat until a condition becomes false; watch for infinite loops
- [ ] List, dict, and set comprehensions - compact one-line way to build a collection, e.g. `[x*2 for x in nums]`; idiomatic Python, used everywhere
*Days 8-9*

- [ ] Functions (parameters, return values, default arguments) - reusable blocks of code; `def greet(name="World"):`
- [ ] Scope (local vs global variables) - which parts of your code can see a given variable; a common source of bugs
*Days 10-11*

- [ ] Context managers (`with` statements) - why they matter for files, connections, locks - `with open(file) as f:` automatically closes things even if an error happens
- [ ] Reading and writing text files - `open()`, `.read()`, `.write()`; how scripts persist data to disk
- [ ] Reading and writing CSV files with the `csv` module - Python's built-in way to handle spreadsheet-style data before you learn pandas
*Days 12-13*

- [ ] Basic exception handling (`try/except`) - catch errors instead of letting your script crash
- [ ] Using `else` and `finally` with `try` blocks - `else` runs if no error occurred, `finally` always runs (cleanup code)
- [ ] Raising exceptions (`raise`) - intentionally trigger an error when something is wrong, e.g. invalid input
- [ ] Creating custom exception classes - your own named errors (e.g. `InvalidConfigError`) for clearer debugging later
*Days 14-15*

- [ ] Importing modules and packages - `import os`, `from datetime import datetime`; reusing code from the standard library or other files
- [ ] Using `__name__ == "__main__"` - lets a script be run directly or imported elsewhere without side effects
*Day 16*

- [ ] Basic classes (attributes and methods) - blueprints for objects that bundle data and behavior together
- [ ] Creating and using instances - `my_obj = MyClass()`; an actual object built from a class blueprint
*Days 17-18*

- [ ] Type hints for function signatures (basic usage, not full generics) - `def greet(name: str) -> str:`; documents intent and helps your editor catch mistakes
- [ ] `datetime`/`time` basics - parsing, formatting, timedeltas, timezones (you'll need this for logging, scheduling, and API timestamps)
*Days 19-20*

- [ ] Regular expressions (`re` module) - `match`, `search`, `findall`, `sub`, basic groups - pattern matching in text, e.g. pulling an email address out of a string
*Day 21*

- [ ] Read and explain a 100–200 line beginner script - test that you can trace through someone else's logic, not just write your own
- [ ] Commit each milestone script to your Phase 0 repo - keep building the git habit alongside the coding habit
*Day 22*

---

## Phase 2 – Automation Fundamentals
*Days 23-56 (~34 days)*

### File & System Automation
*Days 23-25*
- [ ] `pathlib.Path` (paths, files, directories) - modern, cross-platform way to handle file paths instead of raw strings
- [ ] Listing files and filtering by extension - e.g. find every `.csv` in a folder
- [ ] Creating, moving, renaming, and deleting files - the core file-management actions automation scripts perform
- [ ] Creating and cleaning directories - making folders and safely clearing out old ones
- [ ] Using `os` and `shutil` for advanced file operations - copying trees, permissions, and things `pathlib` doesn't cover alone

### Data & APIs
*Days 26-33*
- [ ] Reading and writing JSON files - Python's `json` module; the format most APIs speak
- [ ] Making GET requests with `requests` - fetching data from a URL/API, e.g. `requests.get(url)`
- [ ] Making POST requests with `requests` - sending data to an API, e.g. submitting a form or creating a record
- [ ] Sending headers and query parameters - extra info attached to a request, like auth tokens or filters
- [ ] Handling HTTP errors and timeouts - checking status codes, catching connection failures so your script doesn't just hang or crash
- [ ] Parsing JSON API responses - `response.json()`; turning an API's reply into a Python dict you can use
- [ ] API authentication patterns - API keys, bearer tokens, basic auth, and how OAuth differs (you don't need to implement OAuth yet, just recognize the flow) - knowing which auth method an API expects before you try to call it
- [ ] Storing config in a `.env` file - keeping settings like API keys out of your actual code
- [ ] Loading environment variables with `python-dotenv` - reads the `.env` file into your script at runtime
- [ ] Never hard-code paths or credentials - use env vars from the start - the habit that keeps secrets out of git and code portable across machines
- [ ] Basic logging with `logging` (levels: DEBUG, INFO, WARNING, ERROR) - structured way to record what your script did, better than scattering `print()` everywhere
- [ ] Writing logs to a file - so you can check what happened after a script ran unattended
- [ ] Using rotating file handlers - automatically archives old logs so a single log file doesn't grow forever

*This is the only place `.env` mechanics are taught. Later phases reference this habit rather than re-teaching it.*

### Data Validation
*Day 34*
- [ ] Basic `pydantic` models - why validating API/config data beats trusting raw dicts - catches bad or missing data early instead of failing mysteriously three steps later
- [ ] Validating required fields and types on incoming JSON before using it downstream - defensive coding for data you don't control

### Testing Fundamentals (moved up from Phase 4)
*Days 35-38*
- [ ] Install and run `pytest` - the standard Python testing framework; run tests with `pytest` in the terminal
- [ ] Write simple test functions - functions starting with `test_` that check your code behaves correctly
- [ ] Use assertions in tests - `assert result == expected`; the actual check inside a test
- [ ] Use fixtures for setup/teardown - reusable setup code (like a test database) shared across multiple tests
- [ ] Parametrize tests - run the same test logic against multiple inputs without copy-pasting
- [ ] Run tests with verbose output - `pytest -v`; see exactly which tests ran and their results
- [ ] Write unit tests for your Phase 2 functions (file ops, API parsing) - apply testing to code you've actually written, not just toy examples
- [ ] Keep tests independent (no shared state) - one test's outcome shouldn't affect another's; avoids flaky, order-dependent failures

*Why here: Phase 3 has you using `pytest-playwright` fixtures. You should understand what a fixture is in plain pytest before it shows up wrapped in browser-automation syntax.*

### Async Basics
*Days 39-41*
- [ ] Understand why async matters for I/O-bound automation (many API calls, many pages) - lets your script do other work while waiting on network responses instead of sitting idle
- [ ] `async`/`await` syntax basics - how you mark and call functions that can run concurrently
- [ ] Concurrent requests with `httpx.AsyncClient` or `aiohttp` - fetch many URLs at once instead of one at a time
- [ ] Know when async is worth the complexity and when sync is fine (most small scripts: sync is fine) - don't reach for async just because it's available
- [ ] Know the difference between I/O-bound and CPU-bound work - async/threading helps I/O-bound (waiting on network/disk), `multiprocessing` helps CPU-bound (heavy computation); most automation scripts are I/O-bound - picking the wrong tool here wastes real time debugging "why isn't this faster"

### Data Processing (pandas)
*Days 42-46*
- [ ] Reading CSV files with `pandas` - `pd.read_csv()`; loads tabular data into a DataFrame you can manipulate
- [ ] Reading Excel files with `pandas` - `pd.read_excel()`; same idea, for `.xlsx` files
- [ ] Filtering rows by conditions - e.g. `df[df["status"] == "active"]`; pulling out the rows you actually need
- [ ] Selecting and renaming columns - shaping the DataFrame to just the data you care about
- [ ] Grouping and aggregating data - `df.groupby("region").sum()`; summarizing data by category
- [ ] Handling missing values - deciding whether to drop, fill, or flag empty cells (`NaN`)
- [ ] Exporting DataFrames to CSV - `df.to_csv()`; saving your processed data back out
- [ ] Exporting DataFrames to Excel - `df.to_excel()`; same idea, for report-style output
- [ ] Cell-level Excel work with `openpyxl` - formatting, formulas, and styling that pandas' `.to_excel()` can't do on its own - use this when a client wants a polished, formatted report, not just raw data

### Small Projects
*Days 47-56*
- [ ] File organizer (by extension or date) - sorts a messy folder automatically; combines Phase 2's file ops
- [ ] Folder cleaner with logging - deletes/archives old files and records what it did
- [ ] CSV processor (clean/transform/summarize) - takes messy input data and outputs something usable
- [ ] API data fetcher + CSV/Excel report generator - pulls data from an API and turns it into a report; a realistic client-style task
- [ ] Simple CLI tool with `argparse` or `click` - lets someone run your script with options, e.g. `python tool.py --input file.csv`
- [ ] Each project: own git commits, `.env` for any secrets, at least one pytest test - treat these small projects like real code, not throwaway scripts

---

## Phase 3 – Browser & Web Automation
*Days 57-86 (~30 days)*

### Web & HTML Basics
*Days 57-60*
- [ ] Inspect HTML with browser DevTools - right-click → Inspect; how you find the exact element you need to interact with
- [ ] Understand basic HTML structure (tags, attributes, classes, ids) - the building blocks you'll be targeting with locators and selectors
- [ ] Understand CSS selectors (id, class, attribute, hierarchy) - how to precisely point at one element among many
- [ ] Use `requests` + `BeautifulSoup` for static pages - scraping HTML that doesn't need JavaScript to render
- [ ] Extract text, links, and tables from HTML - pulling structured data out of a page you've fetched
- [ ] Handle simple pagination in scrapers - following "next page" links to collect data across multiple pages
- [ ] Respect `robots.txt` and rate limits; know when scraping ToS matters - scraping responsibly and legally; not every site wants to be scraped

### Playwright (Primary Tool)
*Days 61-70*
- [ ] Install Playwright for Python and browsers - `pip install playwright`, then `playwright install` to get the actual browser binaries
- [ ] Launch a browser and create a page - the starting point of any Playwright script
- [ ] Navigate to a URL - `page.goto(url)`
- [ ] Use role-based locators (button, link, textbox, etc.) - `page.get_by_role("button", name="Submit")`; the recommended way to find elements
- [ ] Click elements and fill inputs - `.click()`, `.fill()`; the core interactions in any automated flow
- [ ] Use text and test-id locators - alternative ways to find elements when role-based locators don't fit
- [ ] Rely on auto-waiting (no manual sleeps) - Playwright waits for elements to be ready automatically; don't fight this with `time.sleep()`
- [ ] Write basic assertions on page content - checking the page shows what you expect after an action
- [ ] Take screenshots on failure - visual evidence of what went wrong when a test fails
- [ ] Enable and view trace on failure - Playwright's trace viewer replays exactly what happened step by step
- [ ] Use `pytest-playwright` fixtures (builds directly on Phase 2 pytest fundamentals) - `page` fixture and friends, wired into pytest
- [ ] Save and reuse authentication state (storage state) - log in once, reuse the session across tests instead of logging in every time
- [ ] Run tests across multiple browsers - Chromium, Firefox, WebKit; catching browser-specific bugs

### Playwright Best Practices
*Days 71-74*
- [ ] Prefer role-based locators over CSS/XPath where possible - more resilient to page changes, closer to how a user actually finds things
- [ ] Trust auto-waiting; avoid `time.sleep()` from the start, not as a later fix - sleeps make tests slow and still flaky; fix the root cause
- [ ] Understand Page Object Model (POM) concept - organizing page interactions into reusable classes instead of duplicating locators everywhere
- [ ] Separate page actions from test assertions - keeps "what the page does" separate from "what we're checking," easier to maintain
- [ ] Use codegen for quick scaffolding, then refactor by hand - `playwright codegen` records your clicks into code; a starting point, not the final product
- [ ] Combine API calls (for setup) with UI tests (for flows) - e.g. create test data via API, then test the UI flow; faster and more reliable than doing everything through the UI

### Selenium (Legacy/Optional)
*Days 75-77*
- [ ] Install Selenium and a WebDriver - the older browser automation library; still common in legacy codebases
- [ ] Launch a browser and navigate - Selenium's equivalent of Playwright's launch + goto
- [ ] Locate elements (id, name, CSS, XPath) - Selenium relies more heavily on these than role-based locators
- [ ] Click and send keys - `.click()`, `.send_keys()`; Selenium's interaction methods
- [ ] Understand explicit waits (`WebDriverWait`) - Selenium doesn't auto-wait like Playwright, so you handle timing manually
- [ ] Know when Selenium is still needed (legacy projects) - recognize it rather than assuming Playwright is always the answer

### Projects
*Days 78-86*
- [ ] Login automation for a demo site - practice the auth + storage state pattern end to end
- [ ] Form filling automation (repeatable workflow) - automate a task a human would otherwise do by hand repeatedly
- [ ] Static site scraper (requests + BeautifulSoup) - apply Phase 3's HTML basics to a real target
- [ ] Dynamic site scraper (Playwright) - scrape a page that requires JavaScript rendering, which `requests` alone can't handle
- [ ] Automated report download from a dashboard - a common real-world automation ask: log in, navigate, download a file
- [ ] One end-to-end business workflow (multi-step) - chain several actions together into one realistic automation, e.g. login → filter → export → save

---

## Phase 4 – Professional Engineering Skills
*Days 87-111 (~25 days)*

### Git Workflows (basics were Phase 0 - this is the rest)
*Days 87-88*
- [ ] Create and switch branches - `git branch`, `git checkout -b`; working on changes without touching the main codebase
- [ ] Merge branches - combining a branch's changes back into main
- [ ] Use a feature-branch workflow (even solo) - one branch per feature/fix, even if you're the only one working on it; builds good habits for team settings
- [ ] Write a `.gitignore` (venvs, `.env`, cache files) - tells git what NOT to track, so junk and secrets don't end up in your repo

### Dependency Management
*Day 89*
- [ ] Freeze dependencies (`requirements.txt`) or use `pyproject.toml` - lists exactly which packages (and versions) your project needs
- [ ] Install dependencies from a requirements file on a fresh machine - `pip install -r requirements.txt`; proving your setup is reproducible
- [ ] Document environment setup in README - so someone else (or future you) can get the project running without guessing

### Code Quality
*Days 90-91*
- [ ] Set up `ruff` for linting and formatting - catches style issues and common bugs automatically
- [ ] Run `mypy` (or rely on your editor) for basic type checking - verifies your type hints are actually consistent
- [ ] Understand why consistent style matters for client-facing code - readable code is code that can be handed off or maintained by someone else

### Debugging & Logging
*Days 92-94*
- [ ] Use the IDE debugger (breakpoints, step-through) - pause execution and inspect what's actually happening, faster than sprinkling `print()` statements
- [ ] Inspect variables during debugging - check the real values at the point something went wrong
- [ ] Add descriptive log messages - logs that explain what the script was doing, not just "error occurred"
- [ ] Log errors and stack traces - capture the full error detail, not just "something failed"
- [ ] Use structured (JSON) logs where useful - machine-readable logs that are easier to search and parse at scale

### Testing in Practice
*Days 95-96*

*(Fundamentals were Phase 2 - this is applying them at project scale)*
- [ ] Write a few Playwright tests for critical flows - focus testing effort on what actually matters to the business
- [ ] Organize a growing test suite into files/folders sensibly - so tests stay findable as the project grows
- [ ] Decide what's worth testing vs what isn't (diminishing returns) - not everything needs a test; know where to draw the line

### Secrets Management (principles - mechanics were Phase 2)
*Day 97*
- [ ] Basic understanding of secret management beyond `.env` (vaults, CI secrets) - how larger teams/projects handle credentials at scale
- [ ] Never commit secrets - set up `.gitignore` before your first `.env` file, not after - one leaked API key in git history is hard to fully undo
- [ ] Document required env vars in README without exposing values - list the variable names a project needs, not their actual secret values

### Documentation
*Days 98-99*
- [ ] Write a clear README (setup, usage, examples) - the first thing anyone sees; should answer "how do I run this?"
- [ ] Document environment variables - what each `.env` variable is for, without leaking real values
- [ ] Add a short "architecture" note (what runs, when, how errors are handled) - a quick mental map for anyone (including you, in six months) picking the project back up
- [ ] Add usage examples and sample commands - concrete copy-pasteable examples beat abstract explanations

### Docker Basics
*Days 100-104*
- [ ] Write a simple `Dockerfile` for a Python script - defines the environment your script needs to run, packaged up
- [ ] Build a Docker image - `docker build`; turns the Dockerfile into a runnable image
- [ ] Run a container locally - `docker run`; test that the packaged environment actually works
- [ ] Use volume mounts for input/output folders - let a container read/write files on your actual machine
- [ ] Understand when Docker is useful (consistent environments) - solves "works on my machine" problems, not needed for every small script

### CI/CD Basics
*Days 105-111*
- [ ] Understand what CI/CD is (continuous integration/deployment) - automatically testing and/or deploying code whenever it changes
- [ ] Create a basic GitHub Actions workflow - a YAML file that tells GitHub what to run automatically (e.g. on every push)
- [ ] Run tests on push to a branch - catch bugs before they reach main, automatically
- [ ] View CI logs and debug failing jobs - reading GitHub Actions output to figure out why a pipeline failed

---

## Phase 5 – Scaling, Data & Orchestration (Optional but Powerful)
*Days 112-139 (~28 days)*

### Scheduling & Orchestration
*Days 112-115*
- [ ] Use `schedule` or `APScheduler` for simple cron-like jobs - run a Python function on a recurring schedule from within your script
- [ ] Understand cron (Linux/macOS) or Task Scheduler (Windows) - the OS-level way to run a script automatically at set times
- [ ] Design idempotent scripts (safe to re-run) - running the script twice shouldn't create duplicate data or break things
- [ ] Add retry logic for flaky APIs or network calls - automatically retry a failed request a few times before giving up
- [ ] Build a multi-step workflow (fetch → transform → load → notify) - chaining automation steps into one coherent pipeline

### Databases & SQL
*Days 116-120*
- [ ] Basic SQL (SELECT, INSERT, UPDATE, DELETE) - the core commands for reading and changing data in a database
- [ ] Connect to a SQLite database from Python - SQLite is a lightweight, file-based database, good for learning and small projects
- [ ] Execute queries with `sqlite3` or `SQLAlchemy` - running SQL from Python code, either directly or through an ORM
- [ ] Read data into a pandas DataFrame - `pd.read_sql()`; pulling database results into a format you can analyze
- [ ] Write DataFrames back to a database table - `df.to_sql()`; saving processed data back to the database

### PDF Automation
*Days 121-124*
- [ ] Extract text and tables from PDFs (`pdfplumber` or `pypdf`) - pulling structured data out of PDF reports or invoices
- [ ] Generate PDF reports programmatically (`reportlab` or similar) - producing polished PDF output from your data
- [ ] Merge/split PDFs as part of a workflow - combining or breaking apart PDF files automatically
- [ ] Know this is one of the most commonly requested automation task in practice - don't skip it - clients ask for PDF handling constantly; it's an easy area to be underprepared for

### Email Automation
*Days 125-126*
- [ ] Send email with `smtplib` (attachments, HTML body) - programmatically sending emails, e.g. a completed report
- [ ] Read/parse inbox messages with `imaplib` or a library like `imap-tools` - pulling data out of incoming emails automatically
- [ ] Use an app password / OAuth token instead of a raw account password - the secure, modern way to authenticate email automation

### AI/LLM Integration
*Days 127-128*
- [ ] Call an LLM API (Anthropic or OpenAI SDK) from a script - integrating an AI model call as one step in a larger automation
- [ ] Use structured output (JSON mode / forced schema) to feed LLM output into the rest of a pipeline - getting reliable, parseable output instead of free-form text
- [ ] Know when an LLM call is the right tool vs when plain code/regex is more reliable and cheaper - don't reach for an LLM when a simple rule would do the job faster and more predictably

### Monitoring & Notifications
*Days 129-130*
- [ ] Add simple health checks (log entry, status file) - a quick way to confirm "yes, this ran successfully today"
- [ ] Send email notifications on failure/completion (builds on the `smtplib` item above) - get alerted automatically instead of discovering a failure days later
- [ ] Send notifications via Telegram or Slack webhooks - faster, more visible alerts than email for time-sensitive failures

### Projects
*Days 131-139*
- [ ] Daily or weekly automated report pipeline - a full fetch → process → deliver cycle running on a schedule
- [ ] Multi-step workflow with notifications - combine orchestration and monitoring into one realistic pipeline
- [ ] One robust script that runs unattended for weeks - the real test: does it keep working without you babysitting it?

---
## Phase 6 – Test Suite Maintenance & Quality
*Days 140-144*
- [ ] Identify and fix flaky tests - tests that fail intermittently for no code-related reason; usually a timing or state issue
- [ ] Remove duplicated setup/teardown code - consolidate repeated fixture logic instead of copy-pasting it across tests
- [ ] Split oversized fixtures into smaller ones - easier to understand and reuse than one giant setup function
- [ ] Delete or skip obsolete tests - tests for features that no longer exist just add noise and slow the suite down
- [ ] Keep test suite fast and focused - a slow test suite gets ignored or skipped; speed is a feature
- [ ] Run tests across browsers in CI - catch browser-specific issues automatically, not just when you remember to check manually

---
## Phase 7 – Portfolio & Career Readiness
*Days 145-158 (~14 days)*
- [ ] 3–5 automation projects on GitHub with READMEs - your actual proof of skill; more convincing than a resume line
- [ ] At least one browser automation project (Playwright) - demonstrates you can handle real-world web interaction, not just APIs
- [ ] At least one data/CSV automation project (with pandas) - demonstrates data-handling skill, a common client need
- [ ] One "client-style" project with clear requirements - simulate a real brief with defined scope, not just "practice"
- [ ] One project with tests, logging, and config management - shows you build production-minded code, not just working scripts
- [ ] Short write-ups explaining what each project does - a paragraph per project: the problem, your approach, the result
- [ ] Basic understanding of SDLC and testing concepts - Software Development Life Cycle; the phases a project typically moves through
- [ ] Know common testing types (unit, integration, regression) - unit tests check one piece in isolation, integration tests check pieces working together, regression tests catch old bugs coming back
- [ ] Understand severity vs priority for defects - severity is how bad the bug is, priority is how soon it needs fixing; they don't always match
- [ ] Basic familiarity with JIRA or similar tools (optional) - common in client/team environments for tracking work and bugs
- [ ] Prepare a simple resume highlighting automation projects - lead with what you built, not just tools you've "used"
- [ ] Practice explaining your projects out loud - being able to talk through your own code clearly matters as much as writing it

---
**Total: ~158 days at 1-2 hrs/day (roughly 5-5.5 months). Phases 5-7 are labeled optional in scope but not in the day count above - skip or compress them if you want to reach "portfolio-ready" faster.**
