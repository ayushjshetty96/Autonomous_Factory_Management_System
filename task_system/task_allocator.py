"""
Task Allocator Module
Handles task queue management and robot assignment
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
import heapq


class TaskAllocator:
    """
    Manages task allocation to available robots.
    
    Maintains a queue of pending tasks and matches them with available robots
    based on priority, location proximity, and robot capabilities.
    """
    
    def __init__(self) -> None:
        """Initialize the task allocator."""
        self.pending_tasks: List[Any] = []  # Priority queue
        self.assigned_tasks: Dict[str, Any] = {}  # task_id -> task
        self.robot_registry: Dict[str, Any] = {}  # robot_id -> robot
        self.allocation_history: List[Dict[str, Any]] = []
        self.creation_time: datetime = datetime.now()
    
    def register_robot(self, robot: Any) -> None:
        """
        Register a robot with the allocator.
        
        Args:
            robot: The RobotAgent to register
        """
        if robot.robot_id not in self.robot_registry:
            self.robot_registry[robot.robot_id] = robot
    
    def add_task_to_queue(self, task: Any) -> None:
        """
        Add a task to the pending queue.
        
        Args:
            task: The Task object to add
        """
        # Store in priority queue by priority (lower number = higher priority)
        heapq.heappush(self.pending_tasks, (task.priority, task.task_id, task))
    
    def allocate_available_tasks(self) -> Dict[str, Any]:
        """
        Allocate pending tasks to available robots.
        
        Returns:
            Dictionary with allocation results
        """
        results = {
            "allocated_count": 0,
            "failed_count": 0,
            "pending_count": len(self.pending_tasks),
            "timestamp": datetime.now().isoformat(),
            "allocations": []
        }
        
        # Get available robots
        available_robots = self._get_available_robots()
        
        # Allocate tasks by priority
        temp_queue = []
        
        while self.pending_tasks and available_robots:
            priority, task_id, task = heapq.heappop(self.pending_tasks)
            
            # Find the best robot for this task
            best_robot = self._find_best_robot_for_task(task, available_robots)
            
            if best_robot and best_robot.accept_task(task):
                self.assigned_tasks[task.task_id] = task
                available_robots.remove(best_robot)
                
                results["allocated_count"] += 1
                results["allocations"].append({
                    "task_id": task.task_id,
                    "robot_id": best_robot.robot_id,
                    "location": task.location,
                    "task_type": task.task_type,
                    "priority": task.priority,
                })
                
                # Record in history
                self.allocation_history.append({
                    "task_id": task.task_id,
                    "robot_id": best_robot.robot_id,
                    "timestamp": results["timestamp"],
                    "success": True,
                })
            else:
                # Re-add to temp queue if allocation failed
                temp_queue.append((priority, task_id, task))
                results["failed_count"] += 1
        
        # Re-queue failed allocations
        for item in temp_queue:
            heapq.heappush(self.pending_tasks, item)
        
        return results
    
    def _get_available_robots(self) -> List[Any]:
        """
        Get list of available robots.
        
        Returns:
            List of robots that are available for task assignment
        """
        return [robot for robot in self.robot_registry.values() if robot.is_available()]
    
    def _find_best_robot_for_task(
        self, task: Any, available_robots: List[Any]
    ) -> Optional[Any]:
        """
        Find the best robot to execute a task.
        
        Considers battery level and current position proximity to task location.
        
        Args:
            task: The task to assign
            available_robots: List of available robots
        
        Returns:
            The best RobotAgent, or None if no suitable robot found
        """
        if not available_robots:
            return None
        
        if len(available_robots) == 1:
            return available_robots[0]
        
        # Simple strategy: prefer robots with higher battery
        return max(available_robots, key=lambda r: r.battery_level)
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the status of a specific task.
        
        Args:
            task_id: The ID of the task to check
        
        Returns:
            Dictionary with task status, or None if task not found
        """
        if task_id in self.assigned_tasks:
            task = self.assigned_tasks[task_id]
            return {
                "task_id": task_id,
                "status": "completed" if task.completed else "pending",
                "assigned_robot": task.assigned_robot,
                "task_type": task.task_type,
                "location": task.location,
                "priority": task.priority,
            }
        return None
    
    def get_queue_status(self) -> Dict[str, Any]:
        """
        Get status of the task queue.
        
        Returns:
            Dictionary with queue information
        """
        return {
            "pending_tasks": len(self.pending_tasks),
            "assigned_tasks": len(self.assigned_tasks),
            "total_tasks": len(self.pending_tasks) + len(self.assigned_tasks),
            "registered_robots": len(self.robot_registry),
            "timestamp": datetime.now().isoformat(),
        }
    
    def get_robot_status(self, robot_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the status of a specific robot.
        
        Args:
            robot_id: The ID of the robot to check
        
        Returns:
            Dictionary with robot status, or None if robot not found
        """
        if robot_id in self.robot_registry:
            robot = self.robot_registry[robot_id]
            return robot.report_status()
        return None
    
    def get_all_robots_status(self) -> List[Dict[str, Any]]:
        """
        Get the status of all registered robots.
        
        Returns:
            List of dictionaries with robot statuses
        """
        return [robot.report_status() for robot in self.robot_registry.values()]
    
    def clear_completed_tasks(self) -> int:
        """
        Remove completed tasks from the assigned tasks dictionary.
        
        Returns:
            Number of tasks cleared
        """
        to_remove = [
            task_id for task_id, task in self.assigned_tasks.items()
            if task.completed
        ]
        
        for task_id in to_remove:
            del self.assigned_tasks[task_id]
        
        return len(to_remove)
    
    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        return (
            f"TaskAllocator(pending={len(self.pending_tasks)}, "
            f"assigned={len(self.assigned_tasks)}, "
            f"robots={len(self.robot_registry)})"
        )
