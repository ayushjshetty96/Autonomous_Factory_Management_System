"""
Distance Utility Module
Provides distance calculation functions
"""

import math


def euclidean_distance(point1, point2):
    """
    Calculate Euclidean distance between two points
    
    Args:
        point1: Tuple (x, y) representing first point
        point2: Tuple (x, y) representing second point
    
    Returns:
        float: Distance between the two points
    """
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def manhattan_distance(point1, point2):
    """
    Calculate Manhattan distance between two points
    
    Args:
        point1: Tuple (x, y) representing first point
        point2: Tuple (x, y) representing second point
    
    Returns:
        float: Manhattan distance between the two points
    """
    x1, y1 = point1
    x2, y2 = point2
    return abs(x2 - x1) + abs(y2 - y1)


def chebyshev_distance(point1, point2):
    """
    Calculate Chebyshev distance between two points
    
    Args:
        point1: Tuple (x, y) representing first point
        point2: Tuple (x, y) representing second point
    
    Returns:
        float: Chebyshev distance between the two points
    """
    x1, y1 = point1
    x2, y2 = point2
    return max(abs(x2 - x1), abs(y2 - y1))
