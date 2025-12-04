# Geofence Event Processing Service

## Overview
This service tracks vehicles and detects when they enter or exit defined geographic zones. It accepts real-time GPS location updates via an HTTP endpoint and provides vehicle status queries. The system is designed to be simple, efficient, and easily extensible.

## Challenge Details
This service implements a geofence event processing system for a taxi fleet. It receives real‑time GPS location updates via an HTTP endpoint, determines which predefined geographic zones the vehicle is in, detects entry/exit transitions, and provides a query endpoint to retrieve the current zone status of any vehicle.

## Design Decisions
| Decision | Reasoning |
|---|---|
| **FastAPI** | High‑performance async framework with automatic OpenAPI docs, ideal for HTTP APIs. |
| **Shapely** | Robust geometry library for point‑in‑polygon checks, avoiding custom error‑prone math. |
| **In‑memory dict store** | Simple, fast prototype without external dependencies; suitable for a 2‑hour challenge. |
| **Hard‑coded zones** | Keeps the example self‑contained; can be externalised to DB/config in production. |

## File Structure

```
geofence_service/
├── main.py              # Application entry point and API routes
├── geofence.py          # Geofencing logic and zone definitions
├── models.py            # Pydantic data models for API validation
├── store.py             # In-memory vehicle state storage
├── test_simulation.py   # Script to verify service functionality
└── requirements.txt     # Python dependencies
```

## Setup Instructions

1.  **Prerequisites**: Python 3.8+
2.  **Installation**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Service**:
    ```bash
    uvicorn main:app --reload
    ```
    The service will be available at `http://localhost:8000`.

## API Endpoints

### 1. Send Location Event
- **URL**: `/events`
- **Method**: `POST`
- **Body**:
    ```json
    {
        "vehicle_id": "taxi-123",
        "latitude": 0.01,
        "longitude": 0.01
    }
    ```
-   **Response**: Returns the updated vehicle status including the current zone.

### 2. Get Vehicle Status
-   **URL**: `/vehicles/{vehicle_id}/status`
-   **Method**: `GET`
-   **Response**: Returns the current status, zone, and last update timestamp.

## Architectural Decisions

### 1. Framework: FastAPI
*   **Decision**: Used FastAPI over Flask or Django.
*   **Reasoning**: FastAPI provides high performance (Starlette-based), automatic data validation (Pydantic), and auto-generated API documentation (Swagger UI). This reduces boilerplate code and ensures type safety for incoming data.
*   **Tradeoff**: Slightly higher learning curve than Flask for absolute beginners, but the benefits in code quality and speed outweigh this.

### 2. Geometry Engine: Shapely
*   **Decision**: Used `shapely` for geometric calculations.
*   **Reasoning**: Writing custom point-in-polygon logic is error-prone and hard to maintain. Shapely is a battle-tested, optimized library for planar geometry.
*   **Tradeoff**: Adds a dependency. For extremely high-performance low-latency systems, a specialized C extension or index (like R-tree) might be needed, but Shapely is sufficient for this scale.

### 3. Data Storage: In-Memory Dictionary
*   **Decision**: Used a simple Python `dict` to store vehicle state.
*   **Reasoning**: The requirements emphasized a 2-hour timeframe and simplicity. An in-memory store is the fastest way to implement state management without the overhead of setting up a database.
*   **Tradeoff**: **Data is lost on restart.** This is not suitable for production but is an acceptable tradeoff for a coding challenge/prototype. It also limits scalability to a single instance.

### 4. Zone Definition: Hardcoded
*   **Decision**: Zones are defined in code (`geofence.py`).
*   **Reasoning**: Keeps the application self-contained and easy to run without external config files or DB migrations.
*   **Tradeoff**: Changing zones requires a code deployment. In a real system, these would be loaded from a database or dynamic configuration service.

## Tradeoffs
- **In‑memory store**: Fast and simple but volatile; data loss on restart.
- **Hard‑coded zones**: Easy to prototype, but requires code change for updates.
- **FastAPI async**: Provides high performance, but adds async complexity for newcomers.
- **Shapely dependency**: Powerful geometry handling, adds extra package weight.
- **Single‑process deployment**: Simpler development, but not horizontally scalable.

1.  **Coordinate System**: We assume a simple Cartesian plane for geometry calculations. For small zones (like a city center), this approximation is acceptable. For global scale or high precision, a library handling geodesic coordinates (like `pyproj`) would be necessary to account for Earth's curvature.
2.  **Non-Overlapping Zones**: We assume zones do not overlap. If a point is in multiple zones, the behavior depends on the iteration order. A production system would need rules for handling overlaps (e.g., priority, nesting).
3.  **Sequential Events**: We assume events arrive roughly in order. We do not handle out-of-order events (e.g., a timestamp from 5 minutes ago arriving after a current one).
4.  **Single Instance**: The service runs as a single process. There is no distributed state handling.

## Future Improvements (if i have more time)

- **Persistence**: Switch the in‑memory store to a database (e.g., PostgreSQL + PostGIS).
- **Scalability**: Add a message queue (Kafka/RabbitMQ) and worker processes.
- **Dynamic Zones**: Provide CRUD APIs to manage zones at runtime.
- **Spatial Indexing**: Use an R‑tree or PostGIS index for fast zone lookups.
- **Observability**: Integrate Prometheus metrics and structured JSON logging.
