### Event Delivery Service
Creating a sample pubsub using Python.

### Architecture
Event -> Ingestion service -> Redis -> Delivery service -> Delivery endpoints.

### Commands
1. Launch all containers: `docker-compose up --build -d`
2. Launch specific container again: `docker-compose up -d --no-deps --build <service name>`
