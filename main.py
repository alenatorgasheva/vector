import pygame
from random import random
from math import sqrt


class Vector:
    """Class of vectors"""
    def int_pair(self):
        """ """
        pass

    def _add(self, other):
        """Summary"""
        pass

    def sub(self, other):
        """Difference"""
        pass

    def mul_(self, other):
        """Multiplication by scalar and scalar multiplication"""
        pass

    def len(self):
        """Vector length"""
        pass


class Line:
    def add_point(self):
        """Adding points to the broken line with their speed"""
        pass

    def set_points(self):
        """Recalculation of point coordinates"""
        pass

    def draw_points(self):
        """Drawing a broken line"""
        pass


class Joint(Line):
    def draw_points(self):
        """Initiating call the get_joint function"""
        pass