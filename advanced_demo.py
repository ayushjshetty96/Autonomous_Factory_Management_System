"""
Advanced Demo Module
Demonstrates all features of the autonomous factory management system.
"""

from agents.robot_agent import RobotAgent
from agents.scheduler_agent import SchedulerAgent
from task_system.task import Task
from task_system.task_allocator import TaskAllocator
from simulation.factory_layout.layout import create_default_factory, ZoneType
from dashboard.status_display import ConsoleDashboard
from analytics import get_analytics
from monitoring import get_logger, log_event, EventType
from config import get_config
import time


def advanced_demo():
    """Run an advanced demonstration of the system."""
    
    config = get_config()
    logger = get_logger()
    analytics = get_analytics()
    dashboard = ConsoleDashboard()
    factory = create_default_factory()
    
    # Log system start
    log_event(
        EventType.SYSTEM_START,
        "main",
        "Autonomous Factory Management System starting",
        {"config": config.to_dict()},
        "info"
    )
    
    print("\n" + "="*80)
    print("ADVANCED FACTORY MANAGEMENT SYSTEM DEMO".center(80))
    print("="*80 + "\n")
    
    # Display configuration
    print("System Configuration:")
    print(f"  System: {config.system_name} v{config.version}")
    print(f"  Factory Size: {config.factory_width}x{config.factory_height}")
    print(f"  Max Robots: {config.max_robots}")
    print(f"  Task Priority Levels: {config.task_config.priority_levels}\n")
    
    # Initialize components
    scheduler = SchedulerAgent()
    allocator = TaskAllocator()
    
    # Create robots
    print("Creating robots...")
    robot_positions = [
        (10, 10), (30, 10), (50, 10), (70, 10), (90, 10)
    ]
    robots = [
        RobotAgent(f"robot_{i}", pos)
        for i, pos in enumerate(robot_positions)
    ]
    
    for robot in robots:
        allocator.register_robot(robot)
        scheduler.register_robot(robot)
        analytics.register_robot(robot.robot_id)
        log_event(
            EventType.ROBOT_CREATED,
            "main",
            f"Robot {robot.robot_id} created",
            {"position": robot.current_position},
            "info"
        )
    
    print(f"  Created {len(robots)} robots\n")
    
    # Create diverse tasks
    print("Creating tasks...")
    tasks = [
        Task("task_001", "assembly_1", "assembly_line", priority=1),
        Task("task_002", "storage", "warehouse", priority=2),
        Task("task_003", "inspection", "quality_center", priority=1),
        Task("task_004", "packaging", "shipping_area", priority=3),
        Task("task_005", "assembly_2", "assembly_line", priority=2),
        Task("task_006", "transport", "transport_hub", priority=2),
        Task("task_007", "charging", "charging_station", priority=1),
        Task("task_008", "maintenance", "maintenance_bay", priority=1),
    ]
    
    for task in tasks:
        allocator.add_task_to_queue(task)
        scheduler.add_task(task)
        log_event(
            EventType.TASK_CREATED,
            "main",
            f"Task {task.task_id} created",
            {
                "task_type": task.task_type,
                "priority": task.priority,
                "location": task.location
            },
            "info"
        )
    
    print(f"  Created {len(tasks)} tasks\n")
    
    # Allocate tasks
    print("Allocating tasks to robots...")
    allocation_result = allocator.allocate_available_tasks()
    print(f"  Allocated: {allocation_result['allocated_count']} tasks")
    print(f"  Failed: {allocation_result['failed_count']} tasks")
    print(f"  Remaining: {allocation_result['pending_count']} tasks\n")
    
    for alloc in allocation_result['allocations']:
        log_event(
            EventType.TASK_ALLOCATED,
            "scheduler",
            f"Task {alloc['task_id']} allocated to {alloc['robot_id']}",
            {
                "task_id": alloc['task_id'],
                "robot_id": alloc['robot_id'],
                "task_type": alloc['task_type']
            },
            "info"
        )
    
    # Display factory layout
    print("\nFactory Layout Overview:")
    factory_status = factory.get_factory_status()
    print(f"  Total Zones: {factory_status['total_zones']}")
    print(f"  Total Capacity: {factory_status['total_capacity']}")
    for zone in factory_status['zones'][:3]:
        print(f"    - {zone['name']}: {zone['zone_id']}")
    
    # Simulate task execution
    print("\n" + "-"*80)
    print("Simulating task execution...\n")
    
    for i in range(3):
        print(f"Execution Cycle {i+1}:")
        
        # Execute tasks
        completed_count = 0
        for robot in robots:
            if robot.current_task:
                robot.execute_task()
                completed_count += 1
                log_event(
                    EventType.TASK_COMPLETED,
                    robot.robot_id,
                    f"Task completed",
                    {"task_id": robot.current_task.task_id if robot.current_task else None},
                    "info"
                )
        
        # Move robots
        for j, robot in enumerate(robots):
            if robot.is_available():
                # Random movement
                new_pos = (
                    (robot.current_position[0] + (j % 3) * 5) % 100,
                    (robot.current_position[1] + (j // 3) * 5) % 100
                )
                robot.move_to_position(new_pos)
        
        # Try to allocate more tasks
        if allocator.pending_tasks:
            alloc_result = allocator.allocate_available_tasks()
            if alloc_result['allocated_count'] > 0:
                print(f"  -> Allocated {alloc_result['allocated_count']} more tasks")
        
        # Update analytics
        analytics.update_task_statistics(
            completed=completed_count,
            pending=len(allocator.pending_tasks),
            failed=0
        )
        
        for robot in robots:
            analytics.update_robot_status(
                robot.robot_id,
                tasks_completed=robot.tasks_completed,
                distance_traveled=robot.total_distance_traveled,
                battery_level=robot.battery_level
            )
        
        print(f"  Completed: {completed_count} tasks")
        print(f"  Robots in use: {sum(1 for r in robots if r.current_task)}/{len(robots)}")
        time.sleep(0.5)
    
    # Display comprehensive dashboard
    print("\n" + "-"*80)
    dashboard.display_full_status(robots, allocator, analytics, factory)
    
    # Display event log
    print("\n" + "="*80)
    print("EVENT LOG (Last 10 Events)".center(80))
    print("="*80)
    recent_events = logger.get_events(limit=10)
    for event in recent_events[-10:]:
        print(f"  {event}")
    
    # Display statistics
    print("\n" + "="*80)
    print("SYSTEM EVENTS SUMMARY".center(80))
    print("="*80)
    stats = logger.get_stats()
    print(f"Total Events Logged: {stats['total_events']}")
    print(f"By Severity: {stats['by_severity']}")
    print(f"By Type: {stats['by_type']}")
    
    # Log system shutdown
    log_event(
        EventType.SYSTEM_SHUTDOWN,
        "main",
        "Autonomous Factory Management System shutting down",
        {"final_stats": analytics.get_summary()},
        "info"
    )
    
    print("\n" + "="*80)
    print("DEMO COMPLETED SUCCESSFULLY".center(80))
    print("="*80 + "\n")


if __name__ == "__main__":
    advanced_demo()
