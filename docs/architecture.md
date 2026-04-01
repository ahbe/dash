# Architecture Decision Records

## Project Overview

The Pricing Derogation Dashboard is built using the Dash framework (Python) with a modular, building-block approach. This design ensures that the application is scalable, maintainable, and easy to extend.

## Design Patterns

### 1. Module-Based Structure
The application is strictly divided into functional modules:
- `src/app.py`: App factory.
- `src/index.py`: Layout assembly.
- `src/components/`: Reusable, generic UI building blocks.
- `src/layouts/`: Composed layout sections (header, sidebar, etc.).
- `src/data/`: Data access and transformation layer.
- `src/callbacks/`: Interaction logic.

### 2. Generic Building Blocks
UI components like filters, metric cards, and charts are designed to be generic. They accept parameters and return Dash components. This allows for rapid development of new pages or dashboard sections.

### 3. Data Connector Pattern
An abstract base class (`BaseConnector`) defines the interface for data access. Concrete connectors (PostgreSQL, COS, SharePoint, etc.) implement this interface, allowing the `DataManager` to interact with any data source uniformly.

### 4. Pattern-Matching Callbacks
Dash pattern-matching callbacks are used to handle interactions with generic components (e.g., filters) using a single callback function for all instances of a component type.

### 5. Centralized Configuration
Configuration is managed using `pydantic-settings`, allowing settings to be loaded from environment variables or a `.env` file with validation.

## Data Flow

1. **User Interaction**: User changes a filter in the Sidebar.
2. **Callback Trigger**: A pattern-matching callback in `filter_callbacks.py` is triggered.
3. **Data Retrieval**: The callback requests data from `DataManager`.
4. **Caching**: `DataManager` checks the `DataCache`. If data is missing or expired, it uses the appropriate `BaseConnector` to fetch fresh data.
5. **Transformation**: The raw data is passed through `FilterTransformer` and `MetricTransformer`.
6. **UI Update**: The transformed data is used to update Metric Cards, Charts, and the Data Table.

## Security Considerations

- API keys and database URLs are stored in environment variables, never hardcoded.
- Data access is abstracted, allowing for future implementation of row-level security or other access controls.
- Docker containerization ensures a consistent and isolated runtime environment.
