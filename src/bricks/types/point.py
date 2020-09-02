"""Representation of a point in two dimensional coordinate system"""


class Point:
    """
    Representation of a point in two dimensional coordinate system
    
    Attributes
    ----------
    x : float 
        x component of coordinate
    y : float 
        y component of coordinate
    """

    def __init__(self, x, y):
        """Stores x and y"""
        self.x = x
        self.y = y
