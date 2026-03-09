"""
Main Module
Entry point for the Autonomous Factory Management System

This module initializes all components including robots, task scheduler,
and task allocator, then demonstrates the system's capabilities.
"""

from agents.robot_agent import RobotAgent
from agents.scheduler_agent import SchedulerAgent
from task_system.task import Task
from task_system.task_allocator import TaskAllocator


def main() -> None:
    """Main function to run the factory management system."""
    
    print("=" * 60)
    print("Autonomous Factory Management System")
    print("=" * 60)
    
    # Initialize components
    scheduler = SchedulerAgent()
    allocator = TaskAllocator()
    
    # Create robots with initial positions
    robot_positions = [(0, 0), (10, 0), (0, 10), (10, 10), (5, 5)]
    robots = [
        RobotAgent(f"robot_{i}", position)
        for i, position in enumerate(robot_positions)
    ]
    
    # Register robots with allocator and scheduler
    for robot in robots:
        allocator.register_robot(robot)
        scheduler.register_robot(robot)
    
    # Create and add sample tasks
    tasks = [
        Task("task_1", "assembly", "assembly_line", priority=1),
        Task("task_2", "transport", "warehouse", priority=2),
        Task("task_3", "inspection", "quality_center", priority=1),
        Task("task_4", "packaging", "shipping_area", priority=3),
        Task("task_5", "cleaning", "maintenance_bay", priority=2),
    ]
    
    # Add tasks to allocator and scheduler
    for task in tasks:
        allocator.add_task_to_queue(task)
        scheduler.add_task(task)
    
    # Display initial status
    print(f"\nInitial Setup:")
    print(f"  Robots initialized: {len(robots)}")
    print(f"  Tasks created: {len(tasks)}")
    
    # Show robot status
    print(f"\nRobot Status:")
    for robot in robots:
        print(f"  {robot}")
    
    # Show task queue status
    queue_status = allocator.get_queue_status()
    print(f"\nTask Queue Status:")
    print(f"  Pending tasks: {queue_status['pending_tasks']}")
    print(f"  Registered robots: {queue_status['registered_robots']}")
    
    # Allocate tasks
    print(f"\nAllocating tasks to robots...")
    allocation_result = allocator.allocate_available_tasks()
    print(f"  Allocated: {allocation_result['allocated_count']}")
    print(f"  Failed: {allocation_result['failed_count']}")
    print(f"  Remaining pending: {allocation_result['pending_count']}")
    
    if allocation_result['allocations']:
        print(f"\n  Allocation Details:")
        for alloc in allocation_result['allocations']:
            print(f"    - {alloc['task_id']} -> {alloc['robot_id']} "
                  f"({alloc['task_type']} at {alloc['location']})")
    
    # Show robot status after allocation
    print(f"\nRobot Status After Allocation:")
    for robot_status in allocator.get_all_robots_status():
        print(f"  {robot_status['robot_id']}: {robot_status['status']} "
              f"(battery: {robot_status['battery_level']:.1f}%)")
    
    # Get scheduler availability
    availability = scheduler.get_robot_availability()
    print(f"\nScheduler Robot Availability:")
    print(f"  Total robots: {availability['total_robots']}")
    print(f"  Available: {availability['available_robots']}")
    print(f"  Busy: {availability['busy_robots']}")
    print(f"  Low battery: {availability['low_battery_robots']}")
    
    print(f"\n{'=' * 60}")
    print("System startup completed successfully")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
