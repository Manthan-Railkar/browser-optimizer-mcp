# Browser Optimizer MCP

An optimization middleware layer built on top of FastMCP and Playwright. It sits between AI agents (LLMs) and browser automation frameworks to drastically reduce token usage, latency, and API inference costs while maintaining high accuracy for repetitive browser tasks.

---

## Key Features

1. **Context Compression Engine**: Removes styling, scripts, headers, footers, SVGs, and empty DOM elements. Extracts only interactive elements (`input`, `button`, `select`, `a`, etc.) and basic accessibility structures.
2. **Rule-Based Page Classifier**: Auto-categorizes pages (e.g. login, product search, checkout, surveys, dashboards) to optimize data formatting.
3. **State Difference Engine**: Calculates incremental UI changes between steps, returning only added/removed elements to avoid feeding redundant contexts to LLMs.
4. **Semantic Cache & Fingerprinting**: Uses fast `xxhash` fingerprints and in-memory TTL caching to recall page contexts instantly without reloading.
5. **Deterministic Action Executor**: Executing browser events (typing, clicking, dropdown selection, scrolling) directly using rule-based playbooks without querying the LLM for every single action.
6. **Telemetry & Metrics**: Tracks and logs overall token savings, cache hits, and performance latency.

---

## Project Structure

```text
├── app/
│   ├── browser/       # Playwright browser manager & navigation
│   ├── classifier/    # Rule-based page classifier
│   ├── compressor/    # DOM element optimizer and cleaner
│   ├── config/        # Environment configurations
│   ├── extractor/     # DOM & Accessibility Tree extraction
│   ├── schemas/       # Typed Pydantic data models
│   ├── server/        # FastMCP Server with exposed tools
│   └── utils/         # Logger and basic helpers
├── docker/            # Dockerfile and docker-compose orchestration
├── tests/             # Pytest unit testing suite
└── requirements.txt   # Python dependency manifest
```

---

## Installation & Setup

### 1. Local Python Setup
Make sure you have Python 3.11+ installed.

```bash
# Create a virtual environment
python -m venv venv
venv\Scripts\activate     # On Windows
source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser binaries
playwright install chromium
```

### 2. Configure Environment
Create or edit the `.env` file in the root directory:

```env
LOG_LEVEL=INFO
HEADLESS=True
CACHE_ENABLED=True
CACHE_TTL=300
CACHE_MAX_SIZE=100
BROWSER_TIMEOUT=30000
```

---

## Exposed MCP Tools

The server registers and exposes the following tools to any connected AI Agent:

1. **`extract_context(url)`**: Navigates to a URL, performs cleanup and compression, classifies the page type, and returns clean, structured interactable elements + AX tree.
2. **`page_diff(url)`**: Computes and returns only the delta changes (added/removed elements) compared to the previous page state.
3. **`execute_action(action, selector, value)`**: Deterministically performs interactions: `click`, `type`, `select`, `scroll`, `wait`, or `navigate` without triggering LLM thinking.
4. **`summarize_page(url)`**: Provides a human-readable summary of the page, listing interactive counts and raw text content snippets.
5. **`classify_page(url)`**: Evaluates UI controls to determine the page category (e.g. login, product search, checkout).
6. **`wait_until_ready(url, timeout)`**: Blocks execution until the target page reaches browser stabilization.
7. **`cache_lookup(url)`**: Performs a lookup in the local semantic cache to verify if optimized data exists for the URL.
8. **`get_metrics()`**: Returns system stats (total bytes saved, cache hits/misses, compression ratios).

---

## Running the Server

Start the MCP server locally over standard input/output (stdio):

```bash
python -m app.server.main
```

---

## Running Tests

Run the unit test suite using `pytest`:

```bash
pytest tests/ -v
```

---

## Container Deployment

Run the server inside a Docker container:

```bash
# Build and run using Docker Compose
docker compose -f docker/docker-compose.yml up --build
```
