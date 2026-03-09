"""
Scheduler Agent Module
Manages task scheduling and allocation across robots
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
import heapq


class SchedulerAgent:
    """
    Agent responsible for scheduling and allocating tasks to robots.
    
    Uses priority-based scheduling to ensure high-priority tasks are completed first.
    Optimizes robot assignments based on availability and proximity to tasks.
    """
    
    def __init__(self) -> None:
        """Initialize the scheduler agent."""
        self.task_queue: List[Any] = []  # Priority queue of tasks
        self.robot_pool: List[Any] = []
        self.schedule: Dict[str, List[Any]] = {}  # robot_id -> list of tasks
        self.completed_tasks: List[Any] = []
        self.creation_time: datetime = datetime.now()
    
    def register_robot(self, robot: Any) -> None:
        """
        Register a robot with the scheduler.
        
        Args:
            robot: The RobotAgent to register
        """
        if robot not in self.robot_pool:
            self.robot_pool.append(robot)
            self.schedule[robot.robot_id] = []
    
    def add_task(self, task: Any) -> None:
        """
        Add a task to the scheduling queue.
        
        Args:
            task: The Task object to schedule
        """
        # Store in priority queue by priority (lower number = higher priority)
        heapq.heappush(self.task_queue, (task.priority, task.task_id, task))
    
    def allocate_tasks(self) -> Dict[str, Any]:
        """
        Allocate tasks to available robots.
        
        Returns:
            Dictionary with allocation results
        """
        allocations = {"allocated": 0, "failed": 0, "details": []}
        
        # Get available robots
        available_robots = [r for r in self.robot_pool if r.is_available()]
        
        # Allocate tasks by priority
        while self.task_queue and available_robots:
            priority, task_id, task = heapq.heappop(self.task_queue)
            
            # Find closest available robot
            best_robot = self._find_best_robot(task, available_robots)
            
            if best_robot and best_robot.accept_task(task):
                self.schedule[best_robot.robot_id].append(task)
                allocations["allocated"] += 1
                allocations["details"].append({
                    "task_id": task.task_id,
                    "robot_id": best_robot.robot_id
                })
                available_robots.remove(best_robot)
            else:
                allocations["failed"] += 1
                # Re-queue the task if allocation failed
                heapq.heappush(self.task_queue, (priority, task_id, task))
        
        return allocations
    
    def _find_best_robot(self, task: Any, available_robots: List[Any]) -> Optional[Any]:
        """
        Find the best robot to execute a task (closest to task location).
        
        Args:
            task: The task to assign
            available_robots: List of available robots
        
        Returns:
            The best RobotAgent, or None if no suitable robot found
        """
        if not available_robots:
            return None
        
        from utils.distance import euclidean_distance
        
        # For now, just return the first available robot
        # In a real system, you'd calculate distances to task locations
        return available_robots[0] if available_robots else None
    
    def optimize_schedule(self) -> Dict[str, Any]:
        """
        Optimize the current task schedule.
        
        Returns:
            Dictionary with optimization metrics
        """
        metrics = {
            "robots_active": 0,
            "tasks_pending": len(self.task_queue),
            "tasks_completed": len(self.completed_tasks),
            "average_tasks_per_robot": 0.0,
            "optimization_timestamp": datetime.now().isoformat(),
        }
        
        # Count active robots
        active_robots = [r for r in self.robot_pool if r.status != "idle"]
        metrics["robots_active"] = len(active_robots)
        
        # Calculate average
        if self.robot_pool:
            total_tasks = sum(len(tasks) for tasks in self.schedule.values())
            metrics["average_tasks_per_robot"] = total_tasks / len(self.robot_pool)
        
        return metrics
    
    def get_robot_availability(self) -> Dict[str, Any]:
        """
        Get availability status of all robots.
        
        Returns:
            Dictionary with robot availability information
        """
        availability = {
            "total_robots": len(self.robot_pool),
            "available_robots": 0,
            "busy_robots": 0,
            "low_battery_robots": 0,
            "robots": []
        }
        
        for robot in self.robot_pool:
            status = {
                "robot_id": robot.robot_id,
                "available": robot.is_available(),
                "status": robot.status,
                "battery_level": robot.battery_level,
                "current_task": robot.current_task.task_id if robot.current_task else None,
            }
            availability["robots"].append(status)
            
            if robot.is_available():
                availability["available_robots"] += 1
            elif robot.current_task is not None:
                availability["busy_robots"] += 1
            
            if robot.battery_level < 20:
                availability["low_battery_robots"] += 1
        
        return availability
    
    def get_queue_status(self) -> Dict[str, Any]:
        """
        Get status of the task queue.
        
        Returns:
            Dictionary with queue information
        """
        return {
            "pending_tasks": len(self.task_queue),
            "completed_tasks": len(self.completed_tasks),
            "total_tasks": len(self.task_queue) + len(self.completed_tasks),
            "queue_timestamp": datetime.now().isoformat(),
        }
    
    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        return (
            f"SchedulerAgent(robots={len(self.robot_pool)}, "
            f"pending_tasks={len(self.task_queue)}, "
            f"completed_tasks={len(self.completed_tasks)})"
        )
