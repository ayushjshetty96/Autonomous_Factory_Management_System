"""
Distance Utility Module
Provides distance calculation functions for coordinate-based operations.

Supports multiple distance metrics: Euclidean, Manhattan, and Chebyshev.
All functions expect 2D coordinates as tuples (x, y).
"""

import math
from typing import Tuple, Union


PointType = Tuple[Union[int, float], Union[int, float]]


def euclidean_distance(point1: PointType, point2: PointType) -> float:
    """
    Calculate Euclidean distance between two points.
    
    The standard distance metric in 2D space. Represents the straight-line
    distance between two points.
    
    Args:
        point1: Tuple (x, y) representing first point
        point2: Tuple (x, y) representing second point
    
    Returns:
        float: Distance between the two points
    
    Raises:
        ValueError: If points don't have exactly 2 coordinates
        TypeError: If coordinates are not numeric
    """
    if len(point1) != 2 or len(point2) != 2:
        raise ValueError("Points must have exactly 2 coordinates (x, y)")
    
    try:
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    except TypeError as e:
        raise TypeError(f"Coordinates must be numeric: {e}")


def manhattan_distance(point1: PointType, point2: PointType) -> float:
    """
    Calculate Manhattan distance between two points.
    
    Also known as L1 distance or taxicab distance. Represents the distance
    traveled when moving only horizontally and vertically (like on a grid).
    
    Args:
        point1: Tuple (x, y) representing first point
        point2: Tuple (x, y) representing second point
    
    Returns:
        float: Manhattan distance between the two points
    
    Raises:
        ValueError: If points don't have exactly 2 coordinates
        TypeError: If coordinates are not numeric
    """
    if len(point1) != 2 or len(point2) != 2:
        raise ValueError("Points must have exactly 2 coordinates (x, y)")
    
    try:
        x1, y1 = point1
        x2, y2 = point2
        return abs(x2 - x1) + abs(y2 - y1)
    except TypeError as e:
        raise TypeError(f"Coordinates must be numeric: {e}")


def chebyshev_distance(point1: PointType, point2: PointType) -> float:
    """
    Calculate Chebyshev distance between two points.
    
    Also known as L∞ distance or chessboard distance. Represents the minimum
    number of moves a chess king would need to move from one point to another.
    
    Args:
        point1: Tuple (x, y) representing first point
        point2: Tuple (x, y) representing second point
    
    Returns:
        float: Chebyshev distance between the two points
    
    Raises:
        ValueError: If points don't have exactly 2 coordinates
        TypeError: If coordinates are not numeric
    """
    if len(point1) != 2 or len(point2) != 2:
        raise ValueError("Points must have exactly 2 coordinates (x, y)")
    
    try:
        x1, y1 = point1
        x2, y2 = point2
        return max(abs(x2 - x1), abs(y2 - y1))
    except TypeError as e:
        raise TypeError(f"Coordinates must be numeric: {e}")


def minkowski_distance(
    point1: PointType, point2: PointType, p: float = 2.0
) -> float:
    """
    Calculate Minkowski distance between two points.
    
    Generalized distance metric where p=1 gives Manhattan and p=2 gives Euclidean.
    
    Args:
        point1: Tuple (x, y) representing first point
        point2: Tuple (x, y) representing second point
        p: The order of the norm. Defaults to 2 (Euclidean)
    
    Returns:
        float: Minkowski distance between the two points
    
    Raises:
        ValueError: If points are invalid or p <= 0
        TypeError: If coordinates are not numeric
    """
    if len(point1) != 2 or len(point2) != 2:
        raise ValueError("Points must have exactly 2 coordinates (x, y)")
    
    if p <= 0:
        raise ValueError(f"p must be > 0, got {p}")
    
    try:
        x1, y1 = point1
        x2, y2 = point2
        
        if p == float('inf'):
            return max(abs(x2 - x1), abs(y2 - y1))
        
        return (abs(x2 - x1)**p + abs(y2 - y1)**p)**(1/p)
    except TypeError as e:
        raise TypeError(f"Coordinates must be numeric: {e}")
