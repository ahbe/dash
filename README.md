# Pricing Derogation Dashboard

## Project Title & Description

This is a complete, production-ready analytics dashboard application built from scratch using the Dash framework by Plotly. It is highly modular, built entirely from reusable generic building blocks, visually polished, and designed for easy evolution and maintenance.

![Python version](https://img.shields.io/badge/Python-3.11%2B-blue)
![Dash Framework](https://img.shields.io/badge/Dash-Latest-red)

## Architecture Diagram

```mermaid
graph TD
    A[Data Layer: Connectors & Manager] --> B(Data Transformers)
    B --> C(Dash Callbacks)
    C --> D[Generic UI Components]
    D --> E(Layouts: Header, Sidebar, Main, Footer)
    E --> F[Dash Application]
    F -- Displays --> G[User Interface]
    H[External Integrations: MLflow, DVC] --> C
    I[Alert Engine] --> C
    J[Scheduler] --> A
```

## Screenshots/Mockups

```
+------------------------------------------------------+
| HEADER (App Title, Refresh Button)                   |
+------------------------------------------------------+
| SIDEBAR         | MAIN CONTENT AREA                  |
| (Filters,       |                                    |
| Model Info)     | +--------------------------------+ |
|                 | | ALERTS (if any)                | |
|                 | +--------------------------------+ |
|                 |                                    |
|                 | +-----------+  +-----------+     |
|                 | | METRIC 1  |  | METRIC 2  |     |
|                 | +-----------+  +-----------+     |
|                 | +-----------+  +-----------+     |
|                 | | METRIC 3  |  | METRIC 4  |     |
|                 | +-----------+  +-----------+     |
|                 |                                    |
|                 | +--------------------------------+ |
|                 | | CHART 1                        | |
|                 | +--------------------------------+ |
|                 |                                    |
|                 | +--------------------------------+ |
|                 | | CHART 2                        | |
|                 | +--------------------------------+ |
|                 |                                    |
|                 | +--------------------------------+ |
|                 | | DATA TABLE                     | |
|                 | +--------------------------------+ |
+------------------------------------------------------+
| FOOTER (Copyright, Links)                            |
+------------------------------------------------------+
```

## Prerequisites

- Python 3.11+
- `uv` package manager
- Docker (optional, for containerized deployment)

## Quick Start

1. Clone the repository:
   ```bash
   git clone <repo_url>
   cd pricing-derogation-dashboard
   ```

2. Sync dependencies using `uv`:
   ```bash
   uv sync
   ```

3. Create an environment file:
   ```bash
   cp .env.example .env
   # Edit .env with your specific settings (database URLs, API keys, etc.)
   ```

4. Generate sample data:
   ```bash
   uv run python scripts/generate_sample_data.py
   ```

5. Run the application locally:
   ```bash
   uv run python run_local.py
   # Open http://localhost:8050 in your browser
   ```

## Configuration Guide

All application settings are loaded from environment variables (or `.env` file) via `src/config.py`. Below is a list of configurable variables:

| Variable Name             | Description                                                   | Default Value    |
|---------------------------|---------------------------------------------------------------|------------------|
| `APP_TITLE`               | Title displayed in the browser and header.                    | `Pricing Derogation Dashboard` |
| `APP_THEME`               | Bootstrap theme name (e.g., `FLATLY`, `COSMO`).               | `FLATLY`         |
| `APP_DEBUG`               | Enable/disable Dash debug mode.                               | `False`          |
| `APP_HOST`                | Host for the Dash server.                                     | `0.0.0.0`        |
| `APP_PORT`                | Port for the Dash server.                                     | `8050`           |
| `POSTGRES_URL`            | SQLAlchemy connection string for PostgreSQL.                  | `None`           |
| `COS_ENDPOINT`            | IBM COS endpoint URL.                                         | `None`           |
| `COS_API_KEY`             | IBM COS API Key.                                              | `None`           |
| `COS_BUCKET`              | IBM COS bucket name.                                          | `None`           |
| `COS_INSTANCE_CRN`        | IBM COS service instance CRN.                                 | `None`           |
| `SHAREPOINT_URL`          | SharePoint site URL.                                          | `None`           |
| `SHAREPOINT_CLIENT_ID`    | SharePoint app client ID.                                     | `None`           |
| `SHAREPOINT_CLIENT_SECRET`| SharePoint app client secret.                                 | `None`           |
| `SHAREPOINT_TENANT_ID`    | SharePoint tenant ID.                                         | `None`           |
| `DOMINO_API_HOST`         | Domino Data Lab API host.                                     | `None`           |
| `DOMINO_API_KEY`          | Domino Data Lab user API key.                                 | `None`           |
| `DOMINO_PROJECT`          | Domino Data Lab project name.                                 | `None`           |
| `MLFLOW_TRACKING_URI`     | MLflow tracking server URI.                                   | `None`           |
| `CACHE_TTL_SECONDS`       | Data cache time-to-live in seconds.                           | `3600`           |
| `REFRESH_SCHEDULE_HOUR`   | Hour (0-23) for daily auto-refresh.                           | `2`              |
| `ALERT_RULES_PATH`        | Path to the YAML file defining alert rules.                   | `src/alerts/alert_rules.yaml` |
| `SAMPLE_DATA_PATH`        | Path to the sample CSV data file.                             | `data/sample/sample_data.csv` |

## Data Source Setup

### CSV / XLSX Connector (`src/data/connectors/csv_connector.py`)

This connector is used by default for the `sample_data.csv`. To use it for other local files, simply specify the path when calling `data_manager.get_data("csv", query="path/to/your/file.csv")`.

### PostgreSQL Connector (`src/data/connectors/postgres_connector.py`)

Configure the `POSTGRES_URL` environment variable with your database connection string, e.g.:

```
POSTGRES_URL="postgresql+psycopg2://user:password@host:port/database"
```

### IBM Cloud Object Storage (COS) Connector (`src/data/connectors/cos_connector.py`)

Set the following environment variables:

- `COS_ENDPOINT`
- `COS_API_KEY`
- `COS_BUCKET`
- `COS_INSTANCE_CRN`

### Domino Data Lab Connector (`src/data/connectors/domino_connector.py`)

Set the following environment variables:

- `DOMINO_API_HOST`
- `DOMINO_API_KEY`
- `DOMINO_PROJECT`

### Microsoft SharePoint Connector (`src/data/connectors/sharepoint_connector.py`)

Set the following environment variables:

- `SHAREPOINT_URL`
- `SHAREPOINT_CLIENT_ID`
- `SHAREPOINT_CLIENT_SECRET`
- `SHAREPOINT_TENANT_ID`

## Building Blocks Guide

The application is built with generic, reusable components. Here's how to use them:

### How to Add a New Filter (`components/filter_block.py`)

Use the `create_filter_block` function in `src/layouts/sidebar.py`. For example:

```python
from src.components.filter_block import create_filter_block, FilterType

new_filter = create_filter_block(
    filter_id="new-category",
    label="New Category",
    filter_type=FilterType.DROPDOWN,
    options=[{"label": "Option A", "value": "A"}, {"label": "Option B", "value": "B"}],
    default_value="A",
)
```

### How to Add a New Metric Card (`components/metric_card.py`)

Use the `create_metric_card` function in `src/layouts/main_content.py`. For example:

```python
from src.components.metric_card import create_metric_card

new_metric = create_metric_card(
    metric_id="new-kpi",
    title="New KPI",
    value="123.45",
    variation=5.2,
    variation_suffix="%",
    icon="star",
    color_scheme="success",
)
```

Remember to add logic to `src/callbacks/metric_callbacks.py` to update its value.

### How to Add a New Chart (`components/chart_block.py`)

Use the `create_chart_block` function in `src/layouts/main_content.py`. For example:

```python
from src.components.chart_block import create_chart_block, ChartType

new_chart = create_chart_block(
    chart_id="new-chart",
    title="New Data Visualization",
    chart_type=ChartType.BAR,
    x_field="date",
    y_fields=["value1", "value2"],
    color_field="category",
    height=350,
)
```

Remember to add logic to `src/callbacks/chart_callbacks.py` to populate its data.

### How to Add a New Alert Rule (`src/alerts/alert_rules.yaml`)

Edit the `src/alerts/alert_rules.yaml` file to define new rules. The structure is as follows:

```yaml
rules:
  - id: my-new-alert
    title: My New Alert
    column: some_metric_column
    condition: gt # or lt, eq
    threshold: 100.0
    severity: danger # or info, warning, success
    message_template: "Custom message: {value:.2f}"
```

The `alert_engine.py` will automatically load and evaluate new rules.

## MLflow & DVC Integration

### MLflow Setup

Configure `MLFLOW_TRACKING_URI` in your `.env` file to point to your MLflow Tracking Server. The `Model Info Card` will then automatically fetch and display model details.

### DVC Setup

Ensure your project is a DVC repository (`dvc init`). The `Model Info Card` will attempt to read `metrics.json` and `dvc.yaml` for status and metrics.

## Deployment Guide

### Local Development

See the [Quick Start](#quick-start) section.

### Production Server (Gunicorn/Waitress)

- **Linux (Gunicorn):**
  ```bash
  uv run gunicorn -w 4 -b 0.0.0.0:8050 run_server:server
  ```
- **Windows (Waitress):**
  ```bash
  uv run python run_server.py
  ```

### Docker

Build the Docker image:
```bash
docker build -t pricing-dashboard .
```

Run the Docker container (with optional PostgreSQL):
```bash
docker-compose up -d
```

### Domino Data Lab

The `domino_job.sh` script is provided to run the application as a scheduled job within a Domino environment. It ensures the `uv` environment is activated and the app is run.

```bash
#!/bin/bash
# domino_job.sh

# Activate uv environment
source ./.venv/bin/activate

# Run the Dash app
python run_server.py
```

## Testing

To run tests, navigate to the project root and execute:

```bash
uv run pytest
```

(Note: Test files are currently placeholders and require implementation.)

## Contributing Guidelines

Contributions are welcome! Please adhere to the following guidelines:

- **Code Style:** Follow PEP 8 strictly. Use `uv fmt` for formatting.
- **Docstrings:** All modules, classes, and functions must have Google-style docstrings.
- **Type Hints:** Use type hints on all function signatures.
- **Tests:** Provide unit and integration tests for new features/bug fixes.
- **Pull Requests:** Submit pull requests to the `main` branch with a clear description.

## Project Structure

```
pricing-derogation-dashboard/
│
├── pyproject.toml                     # Project metadata & dependencies (uv-managed)
├── README.md                          # Full documentation
├── .env.example                       # Example environment variables
├── .gitignore                         # Python/Dash appropriate gitignore
├── Dockerfile                         # Container deployment
├── docker-compose.yml                 # Multi-service orchestration (app + postgres)
├── domino_job.sh                      # Script to run as a Domino scheduled job
├── run_local.py                       # Entry point for local development
├── run_server.py                      # Entry point for production (gunicorn/waitress)
│
├── src/
│   ├── __init__.py                    # Marks src as a Python package
│   │
│   ├── app.py                         # Dash app factory — creates and configures the Dash instance
│   ├── index.py                       # Main layout assembly — composes the full dashboard page
│   ├── config.py                      # Centralized configuration (env vars, defaults, constants)
│   ├── settings.py                    # Placeholder for potential future data source registry & connection settings
│   │
│   ├── layouts/
│   │   ├── __init__.py                # Marks layouts as a Python package
│   │   ├── header.py                  # Top navigation bar / header component
│   │   ├── sidebar.py                 # Sidebar with filters and navigation
│   │   ├── main_content.py            # Main content area layout (metrics + charts + alerts)
│   │   └── footer.py                  # Footer component
│   │
│   ├── components/
│   │   ├── __init__.py                # Marks components as a Python package
│   │   ├── filter_block.py            # GENERIC reusable filter component (dropdown, date range, multi-select)
│   │   ├── metric_card.py             # GENERIC reusable KPI/metric card with value, variation, icon
│   │   ├── chart_block.py             # GENERIC reusable chart container (any Plotly chart type, any data)
│   │   ├── alert_block.py             # GENERIC reusable alert/notification component (threshold-based)
│   │   ├── data_table_block.py        # GENERIC reusable data table component
│   │   ├── refresh_button.py          # Manual data refresh button component
│   │   └── model_info_card.py         # MLflow/DVC model performance display card
│   │
│   ├── callbacks/
│   │   ├── __init__.py                # Marks callbacks as a Python package
│   │   ├── filter_callbacks.py        # Callbacks for all filter interactions (generic, pattern-matching)
│   │   ├── metric_callbacks.py        # Callbacks to update metric cards with live data
│   │   ├── chart_callbacks.py         # Callbacks to update charts based on filters/data
│   │   ├── alert_callbacks.py         # Callbacks to evaluate thresholds and trigger alerts
│   │   ├── refresh_callbacks.py       # Callbacks for manual & scheduled data refresh
│   │   └── model_callbacks.py         # Callbacks to fetch MLflow/DVC model info
│   │
│   ├── data/
│   │   ├── __init__.py                # Marks data as a Python package
│   │   ├── data_manager.py            # Central data orchestrator — abstracts all data source access
│   │   ├── connectors/
│   │   │   ├── __init__.py            # Marks connectors as a Python package
│   │   │   ├── base_connector.py      # Abstract base class for all data connectors
│   │   │   ├── csv_connector.py       # CSV / XLSX file upload & read connector
│   │   │   ├── postgres_connector.py  # PostgreSQL database connector (SQLAlchemy)
│   │   │   ├── cos_connector.py       # IBM Cloud Object Storage connector
│   │   │   ├── domino_connector.py    # Domino Data Lab dataset connector
│   │   │   └── sharepoint_connector.py # Microsoft SharePoint connector (via Office365 REST API)
│   │   │
│   │   ├── transformers/
│   │   │   ├── __init__.py            # Marks transformers as a Python package
│   │   │   ├── base_transformer.py    # Abstract base class for data transformers
│   │   │   ├── metric_transformer.py  # Compute metrics (derogation %, bps, usage, failed calls, margin, conversion rate)
│   │   │   └── filter_transformer.py  # Apply filter selections to dataframes
│   │   │
│   │   └── cache.py                   # Data caching layer (in-memory with TTL, or Redis-ready)
│   │
│   ├── integrations/
│   │   ├── __init__.py                # Marks integrations as a Python package
│   │   ├── mlflow_client.py           # MLflow integration — fetch model registry, metrics, run info
│   │   └── dvc_client.py              # DVC integration — fetch pipeline status, metrics, data versions
│   │
│   ├── alerts/
│   │   ├── __init__.py                # Marks alerts as a Python package
│   │   ├── alert_engine.py            # Alert evaluation engine — configurable thresholds & rules
│   │   └── alert_rules.yaml           # Default alert rule definitions (YAML config)
│   │
│   ├── scheduling/
│   │   ├── __init__.py                # Marks scheduling as a Python package
│   │   └── scheduler.py               # Background scheduler for daily auto-refresh (APScheduler)
│   │
│   ├── utils/
│   │   ├── __init__.py                # Marks utils as a Python package
│   │   ├── formatters.py              # Number formatting, percentage formatting, bps formatting
│   │   ├── validators.py              # Input validation utilities
│   │   ├── logger.py                  # Centralized logging configuration
│   │   └── helpers.py                 # General helper functions
│   │
│   └── assets/
│       ├── custom.css                 # Custom CSS overrides for Dash styling
│       └── logo.png                   # Application logo placeholder (create an empty file)
│
├── tests/
│   ├── __init__.py                    # Marks tests as a Python package
│   ├── conftest.py                    # Pytest fixtures (sample dataframes, mock connectors) - create an empty file
│   ├── test_components/
│   │   ├── __init__.py                # Marks test_components as a Python package
│   │   ├── test_filter_block.py       # Test for filter_block component - create an empty file
│   │   ├── test_metric_card.py        # Test for metric_card component - create an empty file
│   │   ├── test_chart_block.py        # Test for chart_block component - create an empty file
│   │   └── test_alert_block.py        # Test for alert_block component - create an empty file
│   ├── test_data/
│   │   ├── __init__.py                # Marks test_data as a Python package
│   │   ├── test_data_manager.py       # Test for data_manager - create an empty file
│   │   ├── test_connectors.py         # Test for data connectors - create an empty file
│   │   └── test_transformers.py       # Test for data transformers - create an empty file
│   ├── test_integrations/
│   │   ├── __init__.py                # Marks test_integrations as a Python package
│   │   ├── test_mlflow_client.py      # Test for mlflow_client - create an empty file
│   │   └── test_dvc_client.py         # Test for dvc_client - create an empty file
│   └── test_alerts/
│       ├── __init__.py                # Marks test_alerts as a Python package
│       └── test_alert_engine.py       # Test for alert_engine - create an empty file
│
├── data/
│   └── sample/
│       └── sample_data.csv            # Sample dataset for demo/testing
│
└── docs/
    ├── architecture.md                # Architecture decision records - create an empty file
    └── data_sources.md                # How to configure each data source - create an empty file
