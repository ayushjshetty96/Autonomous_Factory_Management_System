"""
Quick Start Guide
Getting started with the Autonomous Factory Management System
"""

from agents.robot_agent import RobotAgent
from task_system.task import Task
from task_system.task_allocator import TaskAllocator
from dashboard.status_display import ConsoleDashboard
from monitoring import log_event, EventType
from analytics import get_analytics


def quick_start():
    """Quick start example."""
    
    # 1. Create a task allocator
    allocator = TaskAllocator()
    
    # 2. Create and register robots
    robots = [
        RobotAgent("robot_A", (0, 0)),
        RobotAgent("robot_B", (50, 50)),
    ]
    
    for robot in robots:
        allocator.register_robot(robot)
        get_analytics().register_robot(robot.robot_id)
        log_event(EventType.ROBOT_CREATED, "demo", f"Created {robot.robot_id}")
    
    # 3. Create and add tasks
    tasks = [
        Task("job_1", "zone_A", "assembly", priority=1),
        Task("job_2", "zone_B", "transport", priority=2),
        Task("job_3", "zone_C", "inspection", priority=1),
    ]
    
    for task in tasks:
        allocator.add_task_to_queue(task)
        log_event(EventType.TASK_CREATED, "demo", f"Created {task.task_id}")
    
    # 4. Allocate tasks to robots
    result = allocator.allocate_available_tasks()
    print(f"\nAllocated {result['allocated_count']} tasks")
    
    # 5. Display status
    dashboard = ConsoleDashboard()
    dashboard.display_full_status(robots, allocator, get_analytics())
    
    # 6. Access analytics
    summary = get_analytics().get_summary()
    print("\nSystem Summary:")
    print(f"  Uptime: {summary['system']['uptime']}")
    print(f"  Completion Rate: {summary['tasks']['completion_rate_percent']:.1f}%")


if __name__ == "__main__":
    print("QUICK START GUIDE")
    print("=" * 60)
    quick_start()
