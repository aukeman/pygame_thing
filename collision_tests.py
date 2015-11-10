from collision import distance_until_rectangles_intersect, rectangles_overlap, point_on_line
from line import Line
from point import Point
from pygame import Rect
import unittest

class CollisionTest(unittest.TestCase):
    
    def test_colocated_rectangles_overlap(self):
        r=[0, 0, 10, 10]
        self.assertEqual(rectangles_overlap(r, r), True)

    def test_colocated_inverted_rectangles_overlap(self):
        r1=[0, 0, 10, 10]
        r2=[10, 10, -10, -10]
        self.assertEqual(rectangles_overlap(r1, r2), True)

    def test_contained_rectangle_overlaps(self):
        r1=[0,0,10,10]
        r2=[3,3,4,4]
        self.assertEqual(rectangles_overlap(r1, r2), True)

    def test_adjacent_on_side_rectangles_overlap(self):
        r1=[0,0,10,10]
        r2=[10,3,4,4]
        self.assertEqual(rectangles_overlap(r1, r2), True)

    def test_adjacent_on_top_rectangles_overlap(self):
        r1=[0,0,10,10]
        r2=[3,10,4,4]
        self.assertEqual(rectangles_overlap(r1, r2), True)

    def test_overlap_side_rectangles_overlap(self):
        r1=[0,0,10,10]
        r2=[-3,3,6,4]
        self.assertEqual(rectangles_overlap(r1, r2), True)

    def test_overlap_top_rectangles_overlap(self):
        r1=[0,0,10,10]
        r2=[3,-3,4,6]
        self.assertEqual(rectangles_overlap(r1, r2), True)
        
    def test_disjoint_rectangles_do_not_overlap(self):
        r1=[0,0,10,10]
        r2=[20,0,4,6]
        self.assertEqual(rectangles_overlap(r1, r2), False)
        
    def test_endpoint1_on_line(self):
        p=Point(0,0)
        l=Line(0,0,10,10)
        self.assertEqual(point_on_line(p,l), True)


    def _test_stationary_rectangle_does_not_intersect(self):
        a=[0,0,10,10]
        v=[0,0]
        b=[20,0,10,10]
        self.assertEqual(distance_until_rectangles_intersect(a,v,b), None)


if __name__ == "__main__":
    unittest.main()
