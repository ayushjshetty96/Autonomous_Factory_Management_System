"""
Configuration Module
Centralized configuration management for the factory system.
"""

from typing import Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class RobotConfig:
    """Configuration for robot agents."""
    model_name: str = "AutonomousBot-v1"
    initial_battery: float = 100.0
    min_battery_threshold: float = 10.0
    battery_consumption_per_distance: float = 0.5
    battery_consumption_per_task: float = 5.0
    max_tasks_per_session: int = 10


@dataclass
class TaskConfig:
    """Configuration for task system."""
    priority_levels: int = 5
    default_priority: int = 1
    task_timeout_seconds: int = 3600
    max_pending_tasks: int = 1000


@dataclass
class SchedulerConfig:
    """Configuration for scheduler agent."""
    allocation_interval_seconds: int = 5
    optimization_interval_seconds: int = 10
    enable_priority_queue: bool = True
    enable_load_balancing: bool = True


@dataclass
class SystemConfig:
    """Master configuration for the entire system."""
    system_name: str = "Autonomous Factory Management System"
    version: str = "1.0.0"
    enable_logging: bool = True
    enable_monitoring: bool = True
    max_robots: int = 50
    factory_width: float = 100.0
    factory_height: float = 100.0
    
    robot_config: RobotConfig = None
    task_config: TaskConfig = None
    scheduler_config: SchedulerConfig = None
    
    def __post_init__(self):
        """Initialize nested configs if not provided."""
        if self.robot_config is None:
            self.robot_config = RobotConfig()
        if self.task_config is None:
            self.task_config = TaskConfig()
        if self.scheduler_config is None:
            self.scheduler_config = SchedulerConfig()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "system_name": self.system_name,
            "version": self.version,
            "enable_logging": self.enable_logging,
            "enable_monitoring": self.enable_monitoring,
            "max_robots": self.max_robots,
            "factory_width": self.factory_width,
            "factory_height": self.factory_height,
            "robot_config": asdict(self.robot_config),
            "task_config": asdict(self.task_config),
            "scheduler_config": asdict(self.scheduler_config),
        }
    
    def __str__(self) -> str:
        """Return string representation."""
        return f"{self.system_name} v{self.version}"


# Global config instance
_config: SystemConfig = SystemConfig()


def get_config() -> SystemConfig:
    """Get the global system configuration."""
    return _config


def set_config(config: SystemConfig) -> None:
    """Set the global system configuration."""
    global _config
    _config = config


def reset_config() -> None:
    """Reset configuration to defaults."""
    global _config
    _config = SystemConfig()
