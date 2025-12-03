# Geofence Event Processing Service

## Overview
This service tracks vehicles and detects when they enter or exit defined geographic zones. It accepts real-time GPS location updates via an HTTP endpoint and provides vehicle status queries. The system is designed to be simple, efficient, and easily extensible.

## File Structure

```
geofence_service/
├── main.py              # Application entry point and API routes
├── geofence.py          # Geofencing logic and zone definitions
├── models.py            # Pydantic data models for API validation
├── store.py             # In-memory vehicle state storage
├── test_simulation.py   # Script to verify service functionality
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── .gitignore           # Git ignore rules
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

## Architectural Decisions & Tradeoffs

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

## Assumptions

1.  **Coordinate System**: We assume a simple Cartesian plane for geometry calculations. For small zones (like a city center), this approximation is acceptable. For global scale or high precision, a library handling geodesic coordinates (like `pyproj`) would be necessary to account for Earth's curvature.
2.  **Non-Overlapping Zones**: We assume zones do not overlap. If a point is in multiple zones, the behavior depends on the iteration order. A production system would need rules for handling overlaps (e.g., priority, nesting).
3.  **Sequential Events**: We assume events arrive roughly in order. We do not handle out-of-order events (e.g., a timestamp from 5 minutes ago arriving after a current one).
4.  **Single Instance**: The service runs as a single process. There is no distributed state handling.

## Future Improvements

### 1. Persistence Layer
*   **Change**: Replace the in-memory `VehicleStore` with a persistent database.
*   **Recommendation**: **PostgreSQL with PostGIS**. PostGIS is the industry standard for geospatial data, allowing for efficient spatial indexing and queries (e.g., "Find all vehicles in zone X"). Redis could be used for high-speed real-time state caching.

### 2. Scalability & Concurrency
*   **Change**: Decouple ingestion from processing.
*   **Recommendation**: Introduce a message queue (e.g., **Kafka** or **RabbitMQ**). The API would publish events to a queue, and worker services would consume them to update state. This handles backpressure and allows scaling workers independently.
*   **Locking**: If multiple updates for the same vehicle occur simultaneously, we need distributed locking (e.g., via Redis) to prevent race conditions.

### 3. Dynamic Zone Management
*   **Change**: Allow runtime updates to zones.
*   **Recommendation**: Create CRUD APIs for zones and store them in the database. Cache them in memory for fast lookups, refreshing periodically or via pub/sub notifications.

### 4. Spatial Indexing
*   **Change**: Optimize zone lookups.
*   **Recommendation**: If the number of zones grows to thousands, iterating through a list is inefficient ($O(N)$). Use a spatial index like an **R-tree** (available in `rtree` or PostGIS) to find candidate zones in $O(\log N)$ time.

### 5. Observability
*   **Change**: Production-grade monitoring.
*   **Recommendation**: Add **Prometheus** metrics (events/sec, latency) and structured logging (JSON format) for better debugging and alerting.
