# Autonomous Factory Management System

A comprehensive Python-based system for managing autonomous robots in a factory environment. Features intelligent task allocation, real-time monitoring, analytics, and a flexible simulation framework.

## Features

### 🤖 Robot Management
- **RobotAgent**: Autonomous agents with battery management, task execution, and movement capabilities
- Real-time status tracking (position, battery level, task status)
- Distance-based movement simulation with battery consumption
- Task acceptance and execution logic

### 📋 Task System
- **Task Management**: Create, allocate, and track factory tasks
- **Priority-based Scheduling**: 5-level priority system for task prioritization
- **Task Allocator**: Intelligent allocation to available robots using priority queues
- Task lifecycle tracking (created → allocated → completed)

### 🎯 Scheduling & Allocation
- **SchedulerAgent**: Intelligent task scheduling and robot management
- **Priority Queue**: Ensures high-priority tasks are executed first
- **Load Balancing**: Distributes work across available robots
- Robot availability tracking and utilization metrics

### 📊 Analytics & Monitoring
- **Analytics Module**: Comprehensive system performance tracking
- **EventLogger**: Real-time event logging and system monitoring
- **Metrics Tracking**: Robot efficiency, task completion rates, battery levels
- Event history with filtering and export capabilities

### 🏭 Factory Simulation
- **Factory Layout**: Modular zone-based factory representation
- **Zone Types**: Assembly, Transport, Storage, Inspection, Packaging, Charging, Maintenance
- **Capacity Management**: Track zone occupancy and robot movement
- **Default Factory**: Pre-configured factory layout for quick start

### 📈 Dashboard & Visualization
- **Console Dashboard**: Real-time console-based status display
- **HTML Dashboard**: Web-ready HTML output for dashboards
- **Status Reports**: Robot, task, system, and factory status displays
- Formatted output with tables and metrics

### ⚙️ Configuration Management
- **Centralized Config**: Robot, task, scheduler, and system configuration
- **Dataclass-based**: Type-safe configuration objects
- **Dictionary Export**: Easy configuration serialization

## Project Structure

```
Autonomus_Factory_Management/
├── agents/                      # Agent implementations
│   ├── robot_agent.py          # Robot agent class
│   └── scheduler_agent.py       # Scheduler agent class
├── task_system/                 # Task management
│   ├── task.py                 # Task class
│   └── task_allocator.py        # Task allocation logic
├── dashboard/                   # Visualization components
│   └── status_display.py        # Console and HTML dashboards
├── simulation/                  # Simulation components
│   └── factory_layout/
│       └── layout.py            # Factory layout definitions
├── utils/                       # Utility functions
│   └── distance.py              # Distance calculation utilities
├── config.py                    # Configuration management
├── monitoring.py                # Event logging and monitoring
├── analytics.py                 # System analytics
├── main.py                      # Basic entry point
├── advanced_demo.py             # Full-featured demo
└── quick_start.py               # Quick start example
```

## Quick Start

### Basic Usage

```python
from agents.robot_agent import RobotAgent
from task_system.task import Task
from task_system.task_allocator import TaskAllocator

# Create allocator and robots
allocator = TaskAllocator()
robots = [RobotAgent("robot_0"), RobotAgent("robot_1")]

for robot in robots:
    allocator.register_robot(robot)

# Create and allocate tasks
task = Task("task_1", "assembly", "assembly_line", priority=1)
allocator.add_task_to_queue(task)

# Allocate pending tasks
result = allocator.allocate_available_tasks()
print(f"Allocated {result['allocated_count']} tasks")
```

### Running Examples

```bash
# Basic example
python main.py

# Advanced demo with all features
python advanced_demo.py

# Quick start guide
python quick_start.py
```

## Core Classes

### RobotAgent
```python
robot = RobotAgent("robot_0", initial_position=(0, 0))
robot.accept_task(task)
robot.execute_task()
robot.move_to_position((10, 10))
status = robot.report_status()
```

### Task
```python
task = Task("task_1", "zone_A", "assembly", priority=1)
task.assign_robot("robot_0")
task.mark_completed()
status = task.is_assigned()
```

### TaskAllocator
```python
allocator = TaskAllocator()
allocator.register_robot(robot)
allocator.add_task_to_queue(task)
result = allocator.allocate_available_tasks()
```

### Analytics
```python
from analytics import get_analytics

analytics = get_analytics()
analytics.register_robot("robot_0")
summary = analytics.get_summary()
analytics.take_snapshot()
```

### EventLogger
```python
from monitoring import log_event, EventType

log_event(
    EventType.TASK_ALLOCATED,
    "scheduler",
    "Task allocated to robot",
    {"task_id": "task_1", "robot_id": "robot_0"},
    "info"
)
```

### Factory Layout
```python
from simulation.factory_layout.layout import create_default_factory

factory = create_default_factory()
zone = factory.get_zone("assembly_1")
factory.connect_zones("assembly_1", "transport")
status = factory.get_factory_status()
```

### Dashboard
```python
from dashboard.status_display import ConsoleDashboard

dashboard = ConsoleDashboard()
dashboard.display_robot_status(robots)
dashboard.display_task_status(allocator)
dashboard.display_system_stats(analytics)
dashboard.display_full_status(robots, allocator, analytics, factory)
```

## Configuration

```python
from config import get_config, SystemConfig

# Get default config
config = get_config()

# Customize
config.max_robots = 100
config.robot_config.initial_battery = 100.0
config.task_config.default_priority = 2

# Access sub-configs
robot_battery = config.robot_config.initial_battery
task_timeout = config.task_config.task_timeout_seconds
```

## Key Features Explained

### Priority-Based Task Allocation
- Tasks are organized in a min-heap priority queue
- Lower priority values = higher urgency
- Tasks allocated in priority order when robots become available

### Robot Battery System
- Robots consume battery when moving and executing tasks
- Battery consumption scales with distance traveled
- Robots with insufficient battery cannot accept tasks
- Status tracking includes battery available percentage

### Event Logging
- All significant system events are logged with timestamps
- Events include: robot creation, task allocation, task completion, errors
- Events can be filtered by type, source, or severity
- Event history can be exported to JSON

### Analytics Pipeline
- Real-time metrics tracking for all system components
- Compute efficiency ratios, completion rates, and utilization percentages
- Snapshots for historical analysis
- Comprehensive summary generation

### Zone Management
- Factory divided into functional zones (assembly, storage, etc.)
- Zones track capacity and current occupancy
- Support for zone connectivity and pathfinding
- Robot movement simulation between zones

## Performance Metrics

Track the following metrics in real-time:

**Robot Metrics:**
- Tasks completed
- Distance traveled
- Average battery level
- Error count
- Efficiency (tasks per distance)

**Task Metrics:**
- Total/Completed/Pending/Failed counts
- Completion rate (%)
- Success rate (%)
- Average completion time

**System Metrics:**
- Uptime (formatted)
- Robot utilization (%)
- Average robot efficiency
- Task allocation success rate

## Dependencies

- Python 3.7+
- Standard library only (no external dependencies)
  - `dataclasses` for configuration
  - `heapq` for priority queues
  - `enum` for type definitions
  - `datetime` for timestamps
  - `json` for export

## Usage Examples

### Example 1: Simple Task Allocation

```python
from agents.robot_agent import RobotAgent
from task_system.task import Task
from task_system.task_allocator import TaskAllocator

allocator = TaskAllocator()
robots = [RobotAgent(f"robot_{i}") for i in range(3)]

for robot in robots:
    allocator.register_robot(robot)

for i in range(5):
    task = Task(f"task_{i}", f"zone_{i%3}", "type", priority=i%3)
    allocator.add_task_to_queue(task)

result = allocator.allocate_available_tasks()
print(f"Success: {result['allocated_count']} tasks allocated")
```

### Example 2: Monitor System with Analytics

```python
from analytics import get_analytics
from monitoring import log_event, EventType

analytics = get_analytics()
analytics.register_robot("robot_0")

# Simulate work
analytics.update_robot_status("robot_0", tasks_completed=5, distance_traveled=50.5, battery_level=75)
analytics.update_task_statistics(completed=5, pending=3, failed=0)

# Get summary
summary = analytics.get_summary()
print(f"Completion Rate: {summary['tasks']['completion_rate_percent']:.1f}%")
```

### Example 3: View System Dashboard

```python
from dashboard.status_display import ConsoleDashboard
from analytics import get_analytics

dashboard = ConsoleDashboard()
dashboard.display_full_status(robots, allocator, get_analytics(), factory)
```

## Error Handling

The system includes validation and error handling for:
- Invalid task priorities (must be 1-5)
- Coordinate validation for positions
- Robot availability checks
- Task allocation failures with re-queuing
- Battery level constraints

## Testing

Run the included examples to verify functionality:

```bash
python main.py              # Basic test
python advanced_demo.py     # Full feature test
python quick_start.py       # Quick start example
```

## Architecture

The system follows a modular, component-based architecture:

1. **Agents**: Autonomous entities (robots, scheduler)
2. **Tasks**: Work units with priority and lifecycle
3. **Allocation**: Intelligent task-to-robot matching
4. **Simulation**: Factory floor representation
5. **Monitoring**: Event logging and system observation
6. **Analytics**: Performance metrics and analysis
7. **Dashboard**: Visualization and reporting
8. **Configuration**: Centralized system settings

## Future Enhancements

Potential improvements for future versions:
- Pathfinding algorithms for optimal robot movement
- Multi-robot collision avoidance
- Machine learning-based task scheduling
- Web-based dashboard with real-time updates
- Database persistence for historical analysis
- ROS (Robot Operating System) integration
- 3D factory visualization
- Real robot hardware integration

## License

[Specify your license]

## Contributing

Contributions are welcome! Please ensure:
- Code follows PEP 8 style guide
- All classes have docstrings
- Type hints are included
- New features include examples

## Support

For issues or questions:
1. Check the Quick Start Guide (`quick_start.py`)
2. Review the Advanced Demo (`advanced_demo.py`)
3. Examine the module docstrings
4. Check example usage in test files

---

**Version:** 1.0.0  
**Last Updated:** March 2026
