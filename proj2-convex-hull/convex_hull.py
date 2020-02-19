from PyQt5.QtCore import QLineF, QPointF, QThread, pyqtSignal

import time

import math
from functools import partial


def less_than(self, other):
    return self.x() < other.x()


QPointF.__lt__ = less_than


class ConvexHullSolverThread(QThread):
    def __init__(self, unsorted_points, demo):
        self.points = unsorted_points
        self.pause = demo
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    show_hull = pyqtSignal(list, tuple)
    display_text = pyqtSignal(str)

    # Some additional thread signals you can implement and use for debugging,
    # if you like
    show_tangent = pyqtSignal(list, tuple)
    erase_hull = pyqtSignal(list)
    erase_tangent = pyqtSignal(list)

    def set_points(self, unsorted_points, demo):
        self.points = unsorted_points
        self.demo = demo

    """
    Divide and conquer is T(n) = 2T(n/2) + O(n)
    Master Theorem: O(nlogn)
    Space complexity: log(n) because the stack size is divided into two each time
    """

    def divide_and_conquer(self, points):
        if len(points) == 1:
            return points

        left_half = self.divide_and_conquer(points[0: len(points) // 2])
        right_half = self.divide_and_conquer(points[len(points) // 2:])

        # this step is O(n) time and O(n) space
        return self.merge(left_half, right_half)

    """
    get_slope is is O(1) since it just two subtractions and a divide
    Space complexity is O(1)
    """

    @staticmethod
    def get_slope(left_point, right_point):
        return (right_point.y() - left_point.y()) / (right_point.x() - left_point.x())

    """
    Time complexity: O(n)
    Space complexity O(n)
    """

    def merge(self, left_half, right_half):
        if len(left_half) + len(right_half) < 4:
            center_x, center_y = get_center(left_half + right_half)
            full = sorted(left_half + right_half, key=partial(clockwise_angle_and_distance, center_x=center_x, center_y=center_y))
            return full

        # O(2n)
        left_start = get_closest_x(left_half, "left")
        right_start = get_closest_x(right_half, "right")

        # O(2n) time worst case
        left_upper_tangent, right_upper_tangent = self.get_upper_tangent(left_start, left_half, right_start, right_half)
        right_lower_tangent, left_lower_tangent = self.get_upper_tangent(right_start, right_half, left_start, left_half)
        full_list = []
        full_list.append(left_half[left_upper_tangent])
        index = right_upper_tangent

        while right_half[index % len(right_half)] != right_half[right_lower_tangent]:
            full_list.append(right_half[index % len(right_half)])
            index += 1
        full_list.append(right_half[right_lower_tangent])
        index = left_lower_tangent

        while left_half[index % len(left_half)] != left_half[left_upper_tangent]:
            full_list.append(left_half[index % len(left_half)])
            index += 1

        return full_list

    """
    Time complexity: O(n)
    Space complexity: O(1)
    """

    def get_upper_tangent(self, left_start, left_half, right_start, right_half):
        left_index = left_start
        right_index = right_start
        previous_tangent = tuple([left_index, right_index])
        while True:
            slope = self.get_slope(left_half[left_index], right_half[right_index])
            left_slope_decreasing = True
            while left_slope_decreasing:
                next_iteration_slope = self.get_slope(left_half[(left_index - 1) % len(left_half)],
                                                      right_half[right_index])
                if next_iteration_slope < slope:
                    slope = next_iteration_slope
                    left_index -= 1
                    if left_index < 0:
                        left_index = len(left_half) - 1
                    left_slope_decreasing = True
                else:
                    left_slope_decreasing = False

            right_slope_increasing = True
            while right_slope_increasing:
                next_iteration_slope = self.get_slope(left_half[left_index],
                                                      right_half[(right_index + 1) % len(right_half)])
                if next_iteration_slope > slope:
                    slope = next_iteration_slope
                    right_index += 1
                    if right_index >= len(right_half):
                        right_index %= len(right_half)
                    right_slope_increasing = True
                else:
                    right_slope_increasing = False

            current_tangent = tuple([left_index, right_index])
            if previous_tangent == current_tangent:
                break
            previous_tangent = current_tangent

        return left_index, right_index

    def run(self):
        assert (type(self.points) == list and type(self.points[0]) == QPointF)

        n = len(self.points)
        print('Computing Hull for set of {} points'.format(n))

        t1 = time.time()
        points = sorted(self.points)
        t2 = time.time()
        print('Time Elapsed (Sorting): {:3.3f} sec'.format(t2 - t1))
        t3 = time.time()

        points = self.divide_and_conquer(points)
        polygon = [QLineF(points[i], points[(i + 1) % len(points)]) for i in range(len(points))]
        t4 = time.time()
        self.show_hull.emit(polygon, (0, 255, 0))

        self.display_text.emit('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4 - t3))
        print('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4 - t3))


"""
time complexity: O(n)
space complexity: O(1)
"""


def calc_upper_tangent(left_start, left_half, right_start, right_half):
    left_index = left_start
    right_index = right_start
    previous_tangent = tuple([left_index, right_index])
    while True:
        slope = get_slope(left_half[left_index], right_half[right_index])
        left_slope_decreasing = True
        while left_slope_decreasing:
            next_iteration_slope = get_slope(left_half[(left_index - 1) % len(left_half)],
                                             right_half[right_index])
            if next_iteration_slope < slope:
                slope = next_iteration_slope
                left_index -= 1
                if left_index < 0:
                    left_index = len(left_half) - 1
                left_slope_decreasing = True
            else:
                left_slope_decreasing = False

        right_slope_increasing = True
        while right_slope_increasing:
            next_iteration_slope = get_slope(left_half[left_index],
                                             right_half[(right_index + 1) % len(right_half)])
            if next_iteration_slope > slope:
                slope = next_iteration_slope
                right_index += 1
                if right_index >= len(right_half):
                    right_index %= len(right_half)
                right_slope_increasing = True
            else:
                right_slope_increasing = False

        current_tangent = tuple([left_index, right_index])
        if previous_tangent == current_tangent:
            break
        previous_tangent = current_tangent
    return left_index, right_index


"""
Time complexity: O(n)
Space complexity: O(1)
"""

def get_closest_x(points, side_to_find="left"):
    closest_index = 0
    if side_to_find == "left":
        for index, point in enumerate(points):
            if point > points[closest_index]:
                closest_index = index
    else:
        for index, point in enumerate(points):
            if point < points[closest_index]:
                closest_index = index
    return closest_index


"""
Time complexity: O(1)
Space complexity: O(1)
"""

def clockwise_angle_and_distance(point, center_x, center_y, anchor="ne"):
    return math.atan2(point.x() - center_x, point.y() - center_y)


"""
Time complexity: O(1)
Space complexity: O(1)
"""
def get_slope(point1, point2):
    return (point1.y() + point2.y()) / (point1.x() + point2.x())


"""
Time complexity: O(n)
Space complexity: O(n)
"""
def get_center(points_list):
    x = [p.x() for p in points_list]
    y = [p.y() for p in points_list]
    return sum(x) / len(points_list), sum(y) / len(points_list)
