# Data Sources Configuration Guide

The Pricing Derogation Dashboard supports multiple data sources through its modular connector architecture.

## Global Configuration

The `DataManager` orchestrates all connectors. To add or modify a data source, you typically only need to set the corresponding environment variables in your `.env` file.

## Available Connectors

### 1. CSV / Excel Connector
- **Implementation**: `src/data/connectors/csv_connector.py`
- **Description**: Reads data from local `.csv`, `.xlsx`, or `.xls` files.
- **Usage**:
  ```python
  df = data_manager.get_data("csv", query="path/to/data.csv")
  ```

### 2. PostgreSQL Connector
- **Implementation**: `src/data/connectors/postgres_connector.py`
- **Description**: Connects to a PostgreSQL database using SQLAlchemy.
- **Environment Variable**: `POSTGRES_URL`
- **Usage**:
  ```python
  df = data_manager.get_data("postgres", query="SELECT * FROM derogations")
  ```

### 3. IBM Cloud Object Storage (COS)
- **Implementation**: `src/data/connectors/cos_connector.py`
- **Description**: Fetches objects from an IBM COS bucket.
- **Environment Variables**:
  - `COS_ENDPOINT`: The endpoint URL for your COS region.
  - `COS_API_KEY`: Your IBM Cloud API key.
  - `COS_BUCKET`: The name of the bucket containing your data.
  - `COS_INSTANCE_CRN`: The service instance CRN.
- **Usage**:
  ```python
  df = data_manager.get_data("cos", query="data_file.csv")
  ```

### 4. Domino Data Lab
- **Implementation**: `src/data/connectors/domino_connector.py`
- **Description**: Accesses datasets or files within a Domino Data Lab project. It automatically detects if it's running inside a Domino execution environment.
- **Environment Variables** (if running outside Domino):
  - `DOMINO_API_HOST`: Your Domino host URL.
  - `DOMINO_API_KEY`: Your Domino user API key.
  - `DOMINO_PROJECT`: The project identifier (e.g., `username/projectname`).
- **Usage**:
  ```python
  df = data_manager.get_data("domino", query="/mnt/data/derogations.csv")
  ```

### 5. Microsoft SharePoint
- **Implementation**: `src/data/connectors/sharepoint_connector.py`
- **Description**: Connects to SharePoint/OneDrive via the Office365 REST API.
- **Environment Variables**:
  - `SHAREPOINT_URL`: The base URL of your SharePoint site.
  - `SHAREPOINT_CLIENT_ID`: Azure App registration client ID.
  - `SHAREPOINT_CLIENT_SECRET`: Azure App registration client secret.
  - `SHAREPOINT_TENANT_ID`: Your Azure tenant ID.
- **Note**: This connector may require a manual authentication step (OAuth2) if a stored token is not present.
- **Usage**:
  ```python
  df = data_manager.get_data("sharepoint", query="Documents/Analytics/Pricing.xlsx")
  ```

## Adding a New Connector

1. Create a new file in `src/data/connectors/` (e.g., `my_new_connector.py`).
2. Inherit from `BaseConnector` and implement the abstract methods: `connect`, `fetch`, and `is_available`.
3. Register the new connector in `src/data/data_manager.py` within the `_register_default_connectors` method.
