# Resource Scheduler


## Overview

Resource Scheduler is a Flask web application designed to optimize the allocation of resources (such as bank tellers or call center agents) to customer requests. The application simulates a service environment with dynamic customer arrivals and implements various scheduling algorithms to minimize wait times and maximize resource utilization.

## Table of Contents

1. [Installation](#installation)
2. [Getting Started](#getting-started)
3. [Key Features](#key-features)
4. [System Architecture](#system-architecture)
5. [API Reference](#api-reference)
6. [Configuration](#configuration)
7. [Scheduling Algorithms](#scheduling-algorithms)
8. [Performance Metrics](#performance-metrics)
9. [User Interface](#user-interface)
10. [Troubleshooting](#troubleshooting)
11. [Contributing](#contributing)

## Installation

```bash
# Clone the repository
git clone https://github.com/AmosMuhanguzi/resource_scheduler.git
cd resource_scheduler

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the application
python app.py
```

## Getting Started

1. Access the application at `http://localhost:5000`
2. Configure the initial number of agents
3. Select a scheduling algorithm
4. Click "Start Simulation" to begin
5. Monitor real-time metrics in the dashboard

## Key Features

### Customer Management
- Dynamic customer generation with configurable arrival rates
- Customer classification (VIP, Corporate, Normal)
- Unique customer tracking and wait time monitoring
- Customizable service requirements

### Agent Management
- automatically three agents are assigned on start
- Add or remove agents during simulation
- Real-time agent status monitoring
- Workload distribution visualization
- Agent performance metrics

### Scheduling Algorithms
- Round Robin: where each agent receives tasks equally
- Priority-based: Prioritizes VIP and Corporate customers
- Shortest Job Next: Assigns customers with shortest expected service time first

### Simulation Control
- Start/pause functionality
- Reset/ stop capabilities
- Real-time system state updates

## System Architecture

The application follows a Model-View-Controller (MVC) architecture:

- **Models**: Define customer, agent, and queue data structures
- **Views**: Flask templates for UI rendering
- **Controllers**: Route handlers and business logic

Key components:
- Flask web server
- SQLite/PostgreSQL database
- WebSockets for real-time updates
- Background task scheduler

## API Reference

### RESTful Endpoints

```
GET /api/status - System status and metrics
GET /api/agents - List all agents
POST /api/agents - Add a new agent
DELETE /api/agents/{id} - Remove an agent
GET /api/customers - List all customers in queue
POST /api/simulation/start - Start simulation
POST /api/simulation/pause - Pause simulation
POST /api/simulation/reset - Reset simulation
PUT /api/algorithm/{algorithm_type} - Change scheduling algorithm
```

### WebSocket Events

```
agent_update - Real-time agent status changes
customer_update - Customer queue changes
metrics_update - Performance metrics updates
```


## Scheduling Algorithms

### Round Robin
Distributes customers to agents in a circular, sequential manner, ensuring fair workload distribution. Suitable for scenarios with similar service requirements.

### Priority-based
Prioritizes customers based on their classification:
1. VIP customers (highest priority)
2. Corporate customers (medium priority)
3. Normal customers (standard priority)

### Shortest Job Next
Minimizes average wait time by assigning customers with the shortest expected service duration first. Most efficient for overall throughput but may cause starvation for complex requests.

## Performance Metrics

The application tracks and displays:

- **Average Wait Time**: Mean time customers spend waiting
- **Agent Utilization**: which measures how much time agents spend working versus being idle
- **Queue Length**: Current number of waiting customers
- **task fairnes**: ensuring tasks are evenly distributed among agents to prevent bottlenecks
- **customers being served**: number of customers served within target time

## User Interface

The UI consists of:

1. **Control Panel**: Buttons for simulation control and algorithm selection
2. **Agent Dashboard**: Visual representation of agent status and workload
3. **Queue Monitor**: Live view of waiting customers
4. **Performance Metrics**: Real-time charts and statistics
5. **Configuration Panel**: Settings for adjusting simulation parameters

## Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| Application fails to start | Check database connection and configuration settings |
| High memory usage | Reduce maximum customer limit or increase processing interval |
| Slow UI updates | Check WebSocket connection, reduce update frequency |
| Agent overloading | Adjust maximum workload capacity or add more agents |

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

Please follow coding standards and add unit tests for new features.