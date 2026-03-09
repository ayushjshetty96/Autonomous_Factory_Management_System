"""
Monitoring Module
System monitoring, logging, and event tracking.
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum
import json


class EventType(Enum):
    """Types of events in the system."""
    ROBOT_CREATED = "robot_created"
    ROBOT_ERROR = "robot_error"
    TASK_CREATED = "task_created"
    TASK_ALLOCATED = "task_allocated"
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"
    ROBOT_BATTERY_LOW = "robot_battery_low"
    ROBOT_MOVING = "robot_moving"
    ROBOT_EXECUTING = "robot_executing"
    ALLOCATION_CYCLE = "allocation_cycle"
    SYSTEM_START = "system_start"
    SYSTEM_SHUTDOWN = "system_shutdown"
    ERROR = "error"
    INFO = "info"
    WARNING = "warning"


class Event:
    """Represents a system event."""
    
    def __init__(
        self,
        event_type: EventType,
        source: str,
        message: str,
        data: Optional[Dict[str, Any]] = None,
        severity: str = "info"
    ):
        """
        Initialize an event.
        
        Args:
            event_type: Type of event
            source: Source component that triggered the event
            message: Human-readable message
            data: Additional event data
            severity: Event severity (info, warning, error)
        """
        self.event_type = event_type
        self.source = source
        self.message = message
        self.data = data or {}
        self.severity = severity
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary."""
        return {
            "event_type": self.event_type.value,
            "source": self.source,
            "message": self.message,
            "data": self.data,
            "severity": self.severity,
            "timestamp": self.timestamp.isoformat(),
        }
    
    def __str__(self) -> str:
        """Return string representation."""
        return (
            f"[{self.timestamp.strftime('%H:%M:%S')}] "
            f"{self.severity.upper()}: {self.source} - {self.message}"
        )


class EventLogger:
    """Logs and manages system events."""
    
    def __init__(self, max_events: int = 10000):
        """
        Initialize the event logger.
        
        Args:
            max_events: Maximum number of events to keep in memory
        """
        self.events: List[Event] = []
        self.max_events = max_events
        self.stats = {
            "total_events": 0,
            "by_type": {},
            "by_severity": {"info": 0, "warning": 0, "error": 0},
        }
    
    def log_event(self, event: Event) -> None:
        """
        Log an event.
        
        Args:
            event: The event to log
        """
        self.events.append(event)
        self.stats["total_events"] += 1
        
        # Update type count
        event_type_value = event.event_type.value
        if event_type_value not in self.stats["by_type"]:
            self.stats["by_type"][event_type_value] = 0
        self.stats["by_type"][event_type_value] += 1
        
        # Update severity count
        if event.severity in self.stats["by_severity"]:
            self.stats["by_severity"][event.severity] += 1
        
        # Trim events if over limit
        if len(self.events) > self.max_events:
            self.events = self.events[-self.max_events:]
        
        # Print event
        print(event)
    
    def get_events(
        self,
        event_type: Optional[EventType] = None,
        source: Optional[str] = None,
        severity: Optional[str] = None,
        limit: int = 100
    ) -> List[Event]:
        """
        Get filtered events.
        
        Args:
            event_type: Filter by event type
            source: Filter by source
            severity: Filter by severity
            limit: Maximum number of events to return
        
        Returns:
            List of matching events (most recent first)
        """
        filtered = self.events
        
        if event_type:
            filtered = [e for e in filtered if e.event_type == event_type]
        if source:
            filtered = [e for e in filtered if e.source == source]
        if severity:
            filtered = [e for e in filtered if e.severity == severity]
        
        # Return most recent first, limited by count
        return filtered[-limit:][::-1]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get event statistics."""
        return {
            **self.stats,
            "recent_events_count": len(self.events),
        }
    
    def clear(self) -> None:
        """Clear all events."""
        self.events = []
    
    def export_json(self, filepath: str) -> None:
        """
        Export events to JSON file.
        
        Args:
            filepath: Path to save the JSON file
        """
        with open(filepath, 'w') as f:
            json.dump(
                [event.to_dict() for event in self.events],
                f,
                indent=2
            )
    
    def __str__(self) -> str:
        """Return string representation."""
        return (
            f"EventLogger(events={len(self.events)}, "
            f"total_logged={self.stats['total_events']})"
        )


# Global logger instance
_logger: EventLogger = EventLogger()


def get_logger() -> EventLogger:
    """Get the global event logger."""
    return _logger


def log_event(
    event_type: EventType,
    source: str,
    message: str,
    data: Optional[Dict[str, Any]] = None,
    severity: str = "info"
) -> None:
    """
    Log an event using the global logger.
    
    Args:
        event_type: Type of event
        source: Source component
        message: Event message
        data: Additional data
        severity: Event severity
    """
    event = Event(event_type, source, message, data, severity)
    _logger.log_event(event)
