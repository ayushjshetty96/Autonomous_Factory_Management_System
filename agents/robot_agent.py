"""
Robot Agent Module
Handles autonomous robot behavior and task execution
"""

from typing import Optional, Tuple, Dict, Any
from datetime import datetime


class RobotAgent:
    """
    Agent representing a robot in the factory.
    
    Handles task acceptance, execution, movement, and status reporting.
    Each robot maintains its own state and can execute tasks autonomously.
    """
    
    VALID_STATUSES = {"idle", "moving", "executing", "charging", "error"}
    
    def __init__(self, robot_id: str, initial_position: Tuple[float, float] = (0, 0)) -> None:
        """
        Initialize a robot agent.
        
        Args:
            robot_id: Unique identifier for the robot
            initial_position: Starting (x, y) coordinates. Defaults to (0, 0)
        """
        self.robot_id: str = robot_id
        self.current_position: Tuple[float, float] = initial_position
        self.current_task: Optional[Any] = None
        self.status: str = "idle"
        self.battery_level: float = 100.0
        self.tasks_completed: int = 0
        self.total_distance_traveled: float = 0.0
        self.last_status_update: datetime = datetime.now()
    
    def accept_task(self, task: Any) -> bool:
        """
        Accept a new task from the task allocator.
        
        Args:
            task: The task object to accept
        
        Returns:
            bool: True if task was accepted, False otherwise
        """
        if self.current_task is not None:
            return False  # Already executing a task
        
        if self.battery_level < 10:
            return False  # Not enough battery
        
        self.current_task = task
        task.assign_robot(self.robot_id)
        self.status = "executing"
        return True
    
    def execute_task(self) -> bool:
        """
        Execute the current task.
        
        Returns:
            bool: True if task was completed, False if still executing
        """
        if self.current_task is None:
            return False
        
        # Simulate task execution
        self.battery_level = max(0, self.battery_level - 5)
        
        # Mark task as completed
        self.current_task.mark_completed()
        self.tasks_completed += 1
        
        # Clear current task
        self.current_task = None
        self.status = "idle"
        return True
    
    def move_to_position(self, position: Tuple[float, float]) -> bool:
        """
        Move to a specified position.
        
        Args:
            position: Target (x, y) coordinates
        
        Returns:
            bool: True if movement was successful, False otherwise
        """
        if self.battery_level < 5:
            self.status = "error"
            return False
        
        # Calculate distance traveled
        from utils.distance import euclidean_distance
        distance = euclidean_distance(self.current_position, position)
        
        # Update position and battery
        self.current_position = position
        self.total_distance_traveled += distance
        self.battery_level = max(0, self.battery_level - (distance * 0.5))
        
        self.status = "moving"
        return True
    
    def report_status(self) -> Dict[str, Any]:
        """
        Report current status of the robot.
        
        Returns:
            Dictionary containing robot status information
        """
        self.last_status_update = datetime.now()
        return {
            "robot_id": self.robot_id,
            "status": self.status,
            "current_position": self.current_position,
            "battery_level": self.battery_level,
            "current_task": self.current_task.task_id if self.current_task else None,
            "tasks_completed": self.tasks_completed,
            "total_distance_traveled": self.total_distance_traveled,
            "timestamp": self.last_status_update.isoformat(),
        }
    
    def charge_battery(self, amount: float = 100.0) -> None:
        """
        Charge the robot's battery.
        
        Args:
            amount: Amount to charge (0-100). Defaults to full charge.
        """
        self.battery_level = min(100.0, self.battery_level + amount)
        self.status = "charging"
    
    def is_available(self) -> bool:
        """Check if robot is available to accept a new task."""
        return self.current_task is None and self.status == "idle" and self.battery_level > 10
    
    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        return (
            f"RobotAgent({self.robot_id}, status={self.status}, "
            f"battery={self.battery_level:.1f}%, position={self.current_position})"
        )
    
    def __repr__(self) -> str:
        """Return a detailed string representation."""
        return self.__str__()
