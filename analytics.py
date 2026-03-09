"""
Analytics Module
System performance tracking and statistics.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field
import statistics


@dataclass
class TaskMetrics:
    """Metrics for task completion."""
    total_tasks: int = 0
    completed_tasks: int = 0
    pending_tasks: int = 0
    failed_tasks: int = 0
    average_completion_time: float = 0.0
    completion_times: List[float] = field(default_factory=list)
    average_priority: float = 0.0
    
    @property
    def completion_rate(self) -> float:
        """Get task completion rate as percentage."""
        if self.total_tasks == 0:
            return 0.0
        return (self.completed_tasks / self.total_tasks) * 100
    
    @property
    def success_rate(self) -> float:
        """Get task success rate (completed / completed + failed)."""
        total_finished = self.completed_tasks + self.failed_tasks
        if total_finished == 0:
            return 0.0
        return (self.completed_tasks / total_finished) * 100


@dataclass
class RobotMetrics:
    """Metrics for robot performance."""
    robot_id: str = ""
    tasks_completed: int = 0
    total_distance_traveled: float = 0.0
    average_battery_level: float = 100.0
    battery_levels: List[float] = field(default_factory=list)
    uptime_seconds: float = 0.0
    error_count: int = 0
    
    @property
    def efficiency(self) -> float:
        """Calculate robot efficiency (tasks per distance)."""
        if self.total_distance_traveled == 0:
            return 0.0
        return self.tasks_completed / self.total_distance_traveled if self.total_distance_traveled > 0 else 0


@dataclass
class SystemMetrics:
    """Overall system metrics."""
    start_time: datetime = field(default_factory=datetime.now)
    total_robots: int = 0
    robots: Dict[str, RobotMetrics] = field(default_factory=dict)
    tasks: TaskMetrics = field(default_factory=TaskMetrics)
    utilization_history: List[float] = field(default_factory=list)
    
    @property
    def uptime_seconds(self) -> float:
        """Get system uptime in seconds."""
        return (datetime.now() - self.start_time).total_seconds()
    
    @property
    def uptime_formatted(self) -> str:
        """Get formatted uptime string."""
        seconds = self.uptime_seconds
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    @property
    def average_robot_efficiency(self) -> float:
        """Get average efficiency across all robots."""
        if not self.robots:
            return 0.0
        total_efficiency = sum(r.efficiency for r in self.robots.values())
        return total_efficiency / len(self.robots)
    
    @property
    def robot_utilization(self) -> float:
        """Get current robot utilization rate (0-100)."""
        if self.total_robots == 0:
            return 0.0
        busy_robots = sum(
            1 for r in self.robots.values() if r.tasks_completed > 0
        )
        return (busy_robots / self.total_robots) * 100


class Analytics:
    """Tracks and analyzes system performance."""
    
    def __init__(self):
        """Initialize the analytics system."""
        self.metrics = SystemMetrics()
        self.snapshots: List[SystemMetrics] = []
        self.snapshot_interval_seconds: int = 60
    
    def register_robot(self, robot_id: str) -> None:
        """
        Register a robot for tracking.
        
        Args:
            robot_id: The robot ID to track
        """
        if robot_id not in self.metrics.robots:
            self.metrics.robots[robot_id] = RobotMetrics(robot_id=robot_id)
            self.metrics.total_robots += 1
    
    def update_robot_status(
        self,
        robot_id: str,
        tasks_completed: Optional[int] = None,
        distance_traveled: Optional[float] = None,
        battery_level: Optional[float] = None,
        error: bool = False
    ) -> None:
        """
        Update robot status metrics.
        
        Args:
            robot_id: The robot to update
            tasks_completed: Number of tasks completed
            distance_traveled: Distance traveled
            battery_level: Current battery level
            error: Whether an error occurred
        """
        if robot_id not in self.metrics.robots:
            self.register_robot(robot_id)
        
        robot = self.metrics.robots[robot_id]
        
        if tasks_completed is not None:
            robot.tasks_completed = tasks_completed
        
        if distance_traveled is not None:
            robot.total_distance_traveled = distance_traveled
        
        if battery_level is not None:
            robot.battery_levels.append(battery_level)
            robot.average_battery_level = statistics.mean(robot.battery_levels)
        
        if error:
            robot.error_count += 1
    
    def update_task_statistics(
        self,
        completed: int = 0,
        pending: int = 0,
        failed: int = 0,
        completion_time: Optional[float] = None,
        priority: Optional[int] = None
    ) -> None:
        """
        Update task statistics.
        
        Args:
            completed: Number of completed tasks
            pending: Number of pending tasks
            failed: Number of failed tasks
            completion_time: Completion time of a task
            priority: Priority of a task
        """
        self.metrics.tasks.completed_tasks += completed
        self.metrics.tasks.pending_tasks = pending
        self.metrics.tasks.failed_tasks += failed
        self.metrics.tasks.total_tasks = (
            self.metrics.tasks.completed_tasks +
            self.metrics.tasks.pending_tasks +
            self.metrics.tasks.failed_tasks
        )
        
        if completion_time is not None:
            self.metrics.tasks.completion_times.append(completion_time)
            self.metrics.tasks.average_completion_time = (
                statistics.mean(self.metrics.tasks.completion_times)
            )
        
        if priority is not None:
            all_priorities = [priority] + [
                p for p in (self.metrics.tasks.completion_times or [])
            ]
            if all_priorities:
                self.metrics.tasks.average_priority = (
                    statistics.mean(all_priorities)
                )
    
    def take_snapshot(self) -> SystemMetrics:
        """
        Take a snapshot of current metrics.
        
        Returns:
            A copy of current system metrics
        """
        snapshot = SystemMetrics(
            start_time=self.metrics.start_time,
            total_robots=self.metrics.total_robots,
            robots={k: RobotMetrics(**v.__dict__) for k, v in self.metrics.robots.items()},
            tasks=TaskMetrics(**self.metrics.tasks.__dict__),
            utilization_history=self.metrics.utilization_history.copy()
        )
        self.snapshots.append(snapshot)
        return snapshot
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a comprehensive summary of system metrics.
        
        Returns:
            Dictionary with all metrics and statistics
        """
        return {
            "system": {
                "uptime": self.metrics.uptime_formatted,
                "uptime_seconds": self.metrics.uptime_seconds,
                "total_robots": self.metrics.total_robots,
                "robot_utilization_percent": self.metrics.robot_utilization,
                "average_robot_efficiency": self.metrics.average_robot_efficiency,
            },
            "tasks": {
                "total": self.metrics.tasks.total_tasks,
                "completed": self.metrics.tasks.completed_tasks,
                "pending": self.metrics.tasks.pending_tasks,
                "failed": self.metrics.tasks.failed_tasks,
                "completion_rate_percent": self.metrics.tasks.completion_rate,
                "success_rate_percent": self.metrics.tasks.success_rate,
                "average_completion_time": self.metrics.tasks.average_completion_time,
            },
            "robots": [
                {
                    "robot_id": r.robot_id,
                    "tasks_completed": r.tasks_completed,
                    "distance_traveled": r.total_distance_traveled,
                    "average_battery_percent": r.average_battery_level,
                    "error_count": r.error_count,
                    "efficiency": r.efficiency,
                }
                for r in self.metrics.robots.values()
            ]
        }
    
    def __str__(self) -> str:
        """Return string representation."""
        return (
            f"Analytics(uptime={self.metrics.uptime_formatted}, "
            f"robots={self.metrics.total_robots}, "
            f"tasks_completed={self.metrics.tasks.completed_tasks})"
        )


# Global analytics instance
_analytics: Analytics = Analytics()


def get_analytics() -> Analytics:
    """Get the global analytics instance."""
    return _analytics
