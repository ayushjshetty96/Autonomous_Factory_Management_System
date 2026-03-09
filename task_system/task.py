"""
Task Module
Defines the Task class for representing factory tasks
"""

from datetime import datetime
from typing import Optional


class Task:
    """
    Represents a task in the autonomous factory management system.
    
    A task is a unit of work that can be assigned to a robot and executed.
    Tasks have priorities and tracks their completion status and assignment.
    """
    
    def __init__(
        self,
        task_id: str,
        location: str,
        task_type: str,
        priority: int = 1
    ) -> None:
        """
        Initialize a new task.
        
        Args:
            task_id: Unique identifier for the task
            location: Physical location where the task should be executed
            task_type: Type of task (e.g., 'assembly', 'transport', 'inspection')
            priority: Priority level (1-5, where 1 is highest). Defaults to 1.
        
        Raises:
            ValueError: If priority is not between 1 and 5
        """
        if not (1 <= priority <= 5):
            raise ValueError(f"Priority must be between 1 and 5, got {priority}")
        
        self.task_id: str = task_id
        self.location: str = location
        self.task_type: str = task_type
        self.priority: int = priority
        self.assigned_robot: Optional[str] = None
        self.completed: bool = False
        self.created_at: datetime = datetime.now()
        self.completed_at: Optional[datetime] = None
    
    def assign_robot(self, robot_id: str) -> None:
        """
        Assign this task to a robot.
        
        Args:
            robot_id: The ID of the robot to assign this task to
        """
        self.assigned_robot = robot_id
    
    def mark_completed(self) -> None:
        """Mark this task as completed and record the completion time."""
        self.completed = True
        self.completed_at = datetime.now()
    
    def unassign(self) -> None:
        """Unassign this task from any robot."""
        self.assigned_robot = None
    
    def is_assigned(self) -> bool:
        """Check if this task is assigned to a robot."""
        return self.assigned_robot is not None
    
    def __str__(self) -> str:
        """Return a user-friendly string representation of the task."""
        status = "completed" if self.completed else "pending"
        assigned = self.assigned_robot or "unassigned"
        return (
            f"Task({self.task_id}, type={self.task_type}, "
            f"location={self.location}, priority={self.priority}, "
            f"status={status}, assigned_to={assigned})"
        )
    
    def __repr__(self) -> str:
        """Return a detailed string representation of the task."""
        return self.__str__()
    
    def to_dict(self) -> dict:
        """
        Convert the task to a dictionary representation.
        
        Returns:
            Dictionary containing all task attributes
        """
        return {
            "task_id": self.task_id,
            "location": self.location,
            "task_type": self.task_type,
            "priority": self.priority,
            "assigned_robot": self.assigned_robot,
            "completed": self.completed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }