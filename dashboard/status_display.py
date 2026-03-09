"""
Dashboard Module
Status display and system overview for the factory management system.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import asdict


class ConsoleDashboard:
    """Simple console-based dashboard for system status."""
    
    def __init__(self):
        """Initialize the dashboard."""
        self.refresh_rate = 1.0  # seconds
        self.last_refresh = datetime.now()
    
    def display_robot_status(self, robots: List[Any]) -> None:
        """
        Display status of all robots.
        
        Args:
            robots: List of RobotAgent objects
        """
        print("\n" + "="*80)
        print("ROBOT STATUS".center(80))
        print("="*80)
        
        if not robots:
            print("No robots registered")
            return
        
        # Header
        print(f"{'Robot ID':<15} {'Status':<12} {'Battery':<10} {'Position':<20} {'Current Task':<15}")
        print("-" * 80)
        
        # Robot rows
        for robot in robots:
            status_report = robot.report_status()
            task_id = status_report.get('current_task') or 'None'
            
            print(
                f"{status_report['robot_id']:<15} "
                f"{status_report['status']:<12} "
                f"{status_report['battery_level']:<10.1f}% "
                f"{str(status_report['current_position']):<20} "
                f"{task_id:<15}"
            )
        
        print()
    
    def display_task_status(self, allocator: Any) -> None:
        """
        Display task queue and allocation status.
        
        Args:
            allocator: TaskAllocator object
        """
        queue_status = allocator.get_queue_status()
        
        print("="*80)
        print("TASK QUEUE STATUS".center(80))
        print("="*80)
        print(f"Pending Tasks:     {queue_status['pending_tasks']}")
        print(f"Assigned Tasks:    {queue_status['assigned_tasks']}")
        print(f"Total Tasks:       {queue_status['total_tasks']}")
        print(f"Registered Robots: {queue_status['registered_robots']}")
        print()
    
    def display_system_stats(self, analytics: Any) -> None:
        """
        Display overall system statistics.
        
        Args:
            analytics: Analytics object
        """
        summary = analytics.get_summary()
        
        print("="*80)
        print("SYSTEM STATISTICS".center(80))
        print("="*80)
        
        # System info
        system = summary['system']
        print(f"Uptime:                {system['uptime']}")
        print(f"Total Robots:          {system['total_robots']}")
        print(f"Robot Utilization:     {system['robot_utilization_percent']:.1f}%")
        print(f"Average Efficiency:    {system['average_robot_efficiency']:.2f}")
        
        # Task info
        tasks = summary['tasks']
        print(f"\nCompleted Tasks:       {tasks['completed']}/{tasks['total']}")
        print(f"Completion Rate:       {tasks['completion_rate_percent']:.1f}%")
        print(f"Success Rate:          {tasks['success_rate_percent']:.1f}%")
        print(f"Avg Completion Time:   {tasks['average_completion_time']:.2f}s")
        print()
    
    def display_robot_details(self, robots: List[Any]) -> None:
        """
        Display detailed information for each robot.
        
        Args:
            robots: List of RobotAgent objects
        """
        print("="*80)
        print("ROBOT DETAILS".center(80))
        print("="*80)
        
        for robot in robots:
            status = robot.report_status()
            print(f"\n{robot.robot_id}:")
            print(f"  Status:              {status['status']}")
            print(f"  Position:            {status['current_position']}")
            print(f"  Battery:             {status['battery_level']:.1f}%")
            print(f"  Tasks Completed:     {status['tasks_completed']}")
            print(f"  Distance Traveled:   {status['total_distance_traveled']:.2f}")
        
        print()
    
    def display_factory_layout(self, factory: Any) -> None:
        """
        Display factory layout and zone status.
        
        Args:
            factory: FactoryLayout object
        """
        status = factory.get_factory_status()
        
        print("\n" + "="*80)
        print("FACTORY LAYOUT".center(80))
        print("="*80)
        print(f"Factory Dimensions: {status['dimensions']['width']}x{status['dimensions']['height']}")
        print(f"Total Zones:        {status['total_zones']}")
        print(f"Total Capacity:     {status['total_capacity']}")
        print(f"Current Occupancy:  {status['total_occupancy']}/{status['total_capacity']}")
        
        print(f"\n{'Zone ID':<20} {'Type':<15} {'Occupancy':<20}")
        print("-" * 55)
        
        for zone in status['zones']:
            occupancy_str = f"{zone['occupancy']}/{zone['capacity']} ({zone['occupancy_percent']:.1f}%)"
            print(
                f"{zone['zone_id']:<20} "
                f"{zone['type']:<15} "
                f"{occupancy_str:<20}"
            )
        
        print()
    
    def display_full_status(
        self,
        robots: List[Any],
        allocator: Any,
        analytics: Any,
        factory: Optional[Any] = None
    ) -> None:
        """
        Display complete system status.
        
        Args:
            robots: List of RobotAgent objects
            allocator: TaskAllocator object
            analytics: Analytics object
            factory: Optional FactoryLayout object
        """
        self.display_robot_status(robots)
        self.display_task_status(allocator)
        self.display_system_stats(analytics)
        
        if factory:
            self.display_factory_layout(factory)
        
        print("="*80)
        print(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)


class HTMLDashboard:
    """HTML-based dashboard for web display."""
    
    @staticmethod
    def generate_html(
        robots: List[Any],
        allocator: Any,
        analytics: Any,
        factory: Optional[Any] = None
    ) -> str:
        """
        Generate HTML dashboard content.
        
        Args:
            robots: List of RobotAgent objects
            allocator: TaskAllocator object
            analytics: Analytics object
            factory: Optional FactoryLayout object
        
        Returns:
            HTML string
        """
        summary = analytics.get_summary()
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Factory Management Dashboard</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; }
                .card { background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .header { color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }
                table { width: 100%; border-collapse: collapse; }
                th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background: #007bff; color: white; }
                .status-active { color: green; font-weight: bold; }
                .status-idle { color: blue; }
                .metric { display: inline-block; margin: 10px 20px 10px 0; }
                .metric-value { font-size: 24px; font-weight: bold; color: #007bff; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Autonomous Factory Management System</h1>
                
                <div class="card">
                    <h2 class="header">System Statistics</h2>
        """
        
        system = summary['system']
        html += f"""
                    <div class="metric">
                        <div>Uptime</div>
                        <div class="metric-value">{system['uptime']}</div>
                    </div>
                    <div class="metric">
                        <div>Total Robots</div>
                        <div class="metric-value">{system['total_robots']}</div>
                    </div>
                    <div class="metric">
                        <div>Utilization</div>
                        <div class="metric-value">{system['robot_utilization_percent']:.1f}%</div>
                    </div>
        """
        
        html += """
                </div>
                
                <div class="card">
                    <h2 class="header">Tasks</h2>
                    <table>
                        <tr>
                            <th>Metric</th>
                            <th>Value</th>
                        </tr>
        """
        
        tasks = summary['tasks']
        html += f"""
                        <tr>
                            <td>Total Tasks</td>
                            <td>{tasks['total']}</td>
                        </tr>
                        <tr>
                            <td>Completed</td>
                            <td>{tasks['completed']}</td>
                        </tr>
                        <tr>
                            <td>Completion Rate</td>
                            <td>{tasks['completion_rate_percent']:.1f}%</td>
                        </tr>
        """
        
        html += """
                    </table>
                </div>
                
                <div class="card">
                    <h2 class="header">Robot Status</h2>
                    <table>
                        <tr>
                            <th>Robot ID</th>
                            <th>Tasks Completed</th>
                            <th>Distance Traveled</th>
                            <th>Battery (%)</th>
                            <th>Efficiency</th>
                        </tr>
        """
        
        for robot in summary['robots']:
            html += f"""
                        <tr>
                            <td>{robot['robot_id']}</td>
                            <td>{robot['tasks_completed']}</td>
                            <td>{robot['distance_traveled']:.2f}</td>
                            <td>{robot['average_battery_percent']:.1f}%</td>
                            <td>{robot['efficiency']:.2f}</td>
                        </tr>
            """
        
        html += """
                    </table>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
