"""
System Verification Script
Verifies all components of the autonomous factory system are working correctly.
"""

import sys
from datetime import datetime


def test_imports():
    """Test that all modules can be imported."""
    print("\n" + "="*60)
    print("TESTING IMPORTS".center(60))
    print("="*60)
    
    modules = [
        ("agents.robot_agent", "RobotAgent"),
        ("agents.scheduler_agent", "SchedulerAgent"),
        ("task_system.task", "Task"),
        ("task_system.task_allocator", "TaskAllocator"),
        ("simulation.factory_layout.layout", "FactoryLayout"),
        ("dashboard.status_display", "ConsoleDashboard"),
        ("config", "get_config"),
        ("monitoring", "get_logger"),
        ("analytics", "get_analytics"),
        ("utils.distance", "euclidean_distance"),
    ]
    
    passed = 0
    failed = 0
    
    for module_name, class_name in modules:
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
            print(f"✓ {module_name}.{class_name}")
            passed += 1
        except Exception as e:
            print(f"✗ {module_name}.{class_name}: {e}")
            failed += 1
    
    print(f"\nImports: {passed} passed, {failed} failed")
    return failed == 0


def test_task_creation():
    """Test Task creation and methods."""
    print("\n" + "="*60)
    print("TESTING TASK MODULE".center(60))
    print("="*60)
    
    try:
        from task_system.task import Task
        
        # Create task
        task = Task("task_1", "zone_A", "assembly", priority=1)
        print(f"✓ Created task: {task}")
        
        # Test methods
        assert task.task_id == "task_1"
        print("✓ Task ID correct")
        
        assert task.priority == 1
        print("✓ Task priority correct")
        
        assert not task.completed
        print("✓ Task initially not completed")
        
        # Test assignment
        task.assign_robot("robot_0")
        assert task.is_assigned()
        print("✓ Robot assignment works")
        
        # Test completion
        task.mark_completed()
        assert task.completed
        print("✓ Task completion works")
        
        # Test serialization
        task_dict = task.to_dict()
        assert "task_id" in task_dict
        print("✓ Task serialization works")
        
        return True
    except Exception as e:
        print(f"✗ Task test failed: {e}")
        return False


def test_robot_creation():
    """Test RobotAgent creation and methods."""
    print("\n" + "="*60)
    print("TESTING ROBOT MODULE".center(60))
    print("="*60)
    
    try:
        from agents.robot_agent import RobotAgent
        from task_system.task import Task
        
        # Create robot
        robot = RobotAgent("robot_0", (0, 0))
        print(f"✓ Created robot: {robot}")
        
        # Test status
        assert robot.robot_id == "robot_0"
        print("✓ Robot ID correct")
        
        assert robot.battery_level == 100.0
        print("✓ Robot battery initialized")
        
        # Test task acceptance
        task = Task("task_1", "zone_A", "assembly", priority=1)
        accepted = robot.accept_task(task)
        assert accepted
        print("✓ Robot accepts tasks")
        
        # Test execution
        robot.execute_task()
        assert robot.current_task is None
        assert robot.tasks_completed == 1
        print("✓ Robot executes tasks")
        
        # Test movement
        robot.move_to_position((10, 10))
        assert robot.current_position == (10, 10)
        print("✓ Robot movement works")
        
        # Test status report
        status = robot.report_status()
        assert "robot_id" in status
        print("✓ Robot status reporting works")
        
        return True
    except Exception as e:
        print(f"✗ Robot test failed: {e}")
        return False


def test_task_allocator():
    """Test TaskAllocator functionality."""
    print("\n" + "="*60)
    print("TESTING TASK ALLOCATOR".center(60))
    print("="*60)
    
    try:
        from task_system.task_allocator import TaskAllocator
        from task_system.task import Task
        from agents.robot_agent import RobotAgent
        
        # Create allocator
        allocator = TaskAllocator()
        print("✓ Created allocator")
        
        # Register robots
        robots = [RobotAgent(f"robot_{i}") for i in range(3)]
        for robot in robots:
            allocator.register_robot(robot)
        print(f"✓ Registered {len(robots)} robots")
        
        # Create tasks
        tasks = [
            Task("task_1", "zone_A", "assembly", priority=1),
            Task("task_2", "zone_B", "transport", priority=2),
            Task("task_3", "zone_C", "inspection", priority=1),
        ]
        for task in tasks:
            allocator.add_task_to_queue(task)
        print(f"✓ Added {len(tasks)} tasks")
        
        # Allocate
        result = allocator.allocate_available_tasks()
        assert result["allocated_count"] > 0
        print(f"✓ Allocated {result['allocated_count']} tasks")
        
        # Check status
        status = allocator.get_queue_status()
        assert status["registered_robots"] == 3
        print("✓ Queue status correct")
        
        return True
    except Exception as e:
        print(f"✗ Task allocator test failed: {e}")
        return False


def test_analytics():
    """Test Analytics functionality."""
    print("\n" + "="*60)
    print("TESTING ANALYTICS MODULE".center(60))
    print("="*60)
    
    try:
        from analytics import Analytics
        
        # Create analytics
        analytics = Analytics()
        print("✓ Created analytics instance")
        
        # Register robot
        analytics.register_robot("robot_0")
        assert "robot_0" in analytics.metrics.robots
        print("✓ Robot registration works")
        
        # Update stats
        analytics.update_robot_status(
            "robot_0",
            tasks_completed=5,
            distance_traveled=50.5,
            battery_level=85.0
        )
        print("✓ Robot status update works")
        
        # Update tasks
        analytics.update_task_statistics(
            completed=5,
            pending=2,
            failed=0,
            completion_time=10.5
        )
        print("✓ Task statistics update works")
        
        # Get summary
        summary = analytics.get_summary()
        assert "system" in summary
        assert "tasks" in summary
        assert "robots" in summary
        print("✓ Summary generation works")
        
        # Snapshot
        snapshot = analytics.take_snapshot()
        assert snapshot.total_robots == 1
        print("✓ Snapshot creation works")
        
        return True
    except Exception as e:
        print(f"✗ Analytics test failed: {e}")
        return False


def test_event_logger():
    """Test EventLogger functionality."""
    print("\n" + "="*60)
    print("TESTING EVENT LOGGER MODULE".center(60))
    print("="*60)
    
    try:
        from monitoring import EventLogger, Event, EventType
        
        # Create logger
        logger = EventLogger()
        print("✓ Created event logger")
        
        # Log events
        event1 = Event(
            EventType.ROBOT_CREATED,
            "test",
            "Test robot created",
            {"robot_id": "robot_0"},
            "info"
        )
        logger.log_event(event1)
        
        event2 = Event(
            EventType.TASK_ALLOCATED,
            "test",
            "Test task allocated",
            {"task_id": "task_1"},
            "info"
        )
        logger.log_event(event2)
        print("✓ Event logging works")
        
        # Check stats
        stats = logger.get_stats()
        assert stats["total_events"] == 2
        print("✓ Event statistics correct")
        
        # Filter events
        events = logger.get_events(event_type=EventType.ROBOT_CREATED)
        assert len(events) == 1
        print("✓ Event filtering works")
        
        return True
    except Exception as e:
        print(f"✗ Event logger test failed: {e}")
        return False


def test_factory_layout():
    """Test Factory Layout functionality."""
    print("\n" + "="*60)
    print("TESTING FACTORY LAYOUT MODULE".center(60))
    print("="*60)
    
    try:
        from simulation.factory_layout.layout import create_default_factory, ZoneType
        
        # Create factory
        factory = create_default_factory()
        print("✓ Created default factory")
        
        # Check zones
        assert len(factory.zones) > 0
        print(f"✓ Factory has {len(factory.zones)} zones")
        
        # Get zone by type
        assembly_zones = factory.get_zones_by_type(ZoneType.ASSEMBLY)
        assert len(assembly_zones) > 0
        print(f"✓ Found {len(assembly_zones)} assembly zones")
        
        # Find nearest zone
        nearest = factory.find_nearest_zone((0, 0))
        assert nearest is not None
        print("✓ Nearest zone finding works")
        
        # Get status
        status = factory.get_factory_status()
        assert "total_zones" in status
        assert "total_capacity" in status
        print("✓ Factory status works")
        
        return True
    except Exception as e:
        print(f"✗ Factory layout test failed: {e}")
        return False


def test_dashboard():
    """Test Dashboard functionality."""
    print("\n" + "="*60)
    print("TESTING DASHBOARD MODULE".center(60))
    print("="*60)
    
    try:
        from dashboard.status_display import ConsoleDashboard, HTMLDashboard
        from agents.robot_agent import RobotAgent
        from task_system.task_allocator import TaskAllocator
        from analytics import Analytics
        
        # Create dashboard
        dashboard = ConsoleDashboard()
        print("✓ Created console dashboard")
        
        # Create test data
        robots = [RobotAgent("robot_0")]
        allocator = TaskAllocator()
        analytics = Analytics()
        
        # Register robot
        allocator.register_robot(robots[0])
        analytics.register_robot("robot_0")
        
        # Test HTML generation
        html = HTMLDashboard.generate_html(robots, allocator, analytics)
        assert "<!DOCTYPE html>" in html
        assert "Factory Management Dashboard" in html
        print("✓ HTML generation works")
        
        return True
    except Exception as e:
        print(f"✗ Dashboard test failed: {e}")
        return False


def test_config():
    """Test Configuration functionality."""
    print("\n" + "="*60)
    print("TESTING CONFIGURATION MODULE".center(60))
    print("="*60)
    
    try:
        from config import get_config, SystemConfig, RobotConfig
        
        # Get default config
        config = get_config()
        print("✓ Retrieved default config")
        
        # Check values
        assert config.system_name == "Autonomous Factory Management System"
        print("✓ System name correct")
        
        assert config.max_robots > 0
        print("✓ Max robots set")
        
        # Check nested configs
        assert config.robot_config is not None
        assert config.task_config is not None
        assert config.scheduler_config is not None
        print("✓ All nested configs present")
        
        # Test serialization
        config_dict = config.to_dict()
        assert "robot_config" in config_dict
        print("✓ Config serialization works")
        
        return True
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        return False


def test_distance_utils():
    """Test distance utility functions."""
    print("\n" + "="*60)
    print("TESTING DISTANCE UTILITIES".center(60))
    print("="*60)
    
    try:
        from utils.distance import (
            euclidean_distance,
            manhattan_distance,
            chebyshev_distance,
            minkowski_distance
        )
        
        # Test Euclidean
        dist = euclidean_distance((0, 0), (3, 4))
        assert abs(dist - 5.0) < 0.01
        print("✓ Euclidean distance correct")
        
        # Test Manhattan
        dist = manhattan_distance((0, 0), (3, 4))
        assert dist == 7
        print("✓ Manhattan distance correct")
        
        # Test Chebyshev
        dist = chebyshev_distance((0, 0), (3, 4))
        assert dist == 4
        print("✓ Chebyshev distance correct")
        
        # Test Minkowski
        dist = minkowski_distance((0, 0), (3, 4), p=2)
        assert abs(dist - 5.0) < 0.01
        print("✓ Minkowski distance correct")
        
        return True
    except Exception as e:
        print(f"✗ Distance utilities test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "█"*60)
    print("AUTONOMOUS FACTORY SYSTEM - VERIFICATION".center(60))
    print("█"*60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Imports", test_imports),
        ("Task Module", test_task_creation),
        ("Robot Module", test_robot_creation),
        ("Task Allocator", test_task_allocator),
        ("Analytics", test_analytics),
        ("Event Logger", test_event_logger),
        ("Factory Layout", test_factory_layout),
        ("Dashboard", test_dashboard),
        ("Configuration", test_config),
        ("Distance Utilities", test_distance_utils),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY".center(60))
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "-"*60)
    print(f"Results: {passed}/{total} tests passed")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
