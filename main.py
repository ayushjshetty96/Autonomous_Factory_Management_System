"""
Main Module
Entry point for the Autonomous Factory Management System
"""

from agents.robot_agent import RobotAgent
from agents.scheduler_agent import SchedulerAgent
from task_system.task import Task
from task_system.task_allocator import TaskAllocator


def main():
    """Main function to run the factory management system"""
    
    # Initialize components
    scheduler = SchedulerAgent()
    allocator = TaskAllocator()
    
    # Create robots
    robots = [RobotAgent(f"robot_{i}") for i in range(5)]
    
    # Register robots with allocator
    for robot in robots:
        allocator.register_robot(robot)
    
    # Create and add sample tasks
    tasks = [
        Task("task_1", "assembly", priority=1),
        Task("task_2", "transport", priority=2),
        Task("task_3", "inspection", priority=1),
    ]
    
    for task in tasks:
        allocator.add_task_to_queue(task)
    
    print("Autonomous Factory Management System Started")
    print(f"Robots initialized: {len(robots)}")
    print(f"Tasks created: {len(tasks)}")


if __name__ == "__main__":
    main()
