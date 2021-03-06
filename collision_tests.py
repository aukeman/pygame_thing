from collision import distance_until_rectangles_intersect, rectangles_overlap, point_on_line, line_intersects_line, line_intersects_rectangle
from line import Line
from point import Point
from rect import Rect
import unittest

class CollisionTest(unittest.TestCase):
    
    def test_colocated_rectangles_overlap(self):
        r=Rect(0, 0, 10, 10)
        self.assertEqual(rectangles_overlap(r, r), True)

    def test_colocated_inverted_rectangles_overlap(self):
        r1=Rect(0, 0, 10, 10)
        r2=Rect(10, 10, -10, -10)
        self.assertEqual(rectangles_overlap(r1, r2), True)

    def test_contained_rectangle_overlaps(self):
        r1=Rect(0,0,10,10)
        r2=Rect(3,3,4,4)
        self.assertEqual(rectangles_overlap(r1, r2), True)

    def test_adjacent_on_side_rectangles_overlap(self):
        r1=Rect(0,0,10,10)
        r2=Rect(10,3,4,4)
        self.assertEqual(rectangles_overlap(r1, r2), True)

    def test_adjacent_on_top_rectangles_overlap(self):
        r1=Rect(0,0,10,10)
        r2=Rect(3,10,4,4)
        self.assertEqual(rectangles_overlap(r1, r2), True)

    def test_overlap_side_rectangles_overlap(self):
        r1=Rect(0,0,10,10)
        r2=Rect(-3,3,6,4)
        self.assertEqual(rectangles_overlap(r1, r2), True)

    def test_overlap_top_rectangles_overlap(self):
        r1=Rect(0,0,10,10)
        r2=Rect(3,-3,4,6)
        self.assertEqual(rectangles_overlap(r1, r2), True)
        
    def test_disjoint_rectangles_do_not_overlap(self):
        r1=Rect(0,0,10,10)
        r2=Rect(20,0,4,6)
        self.assertEqual(rectangles_overlap(r1, r2), False)
        
    def test_endpoint1_on_line(self):
        p=Point(0,0)
        l=Line(0,0,10,10)
        self.assertEqual(point_on_line(p,l), True)

    def test_endpoint2_on_line(self):
        p=Point(10,10)
        l=Line(0,0,10,10)
        self.assertEqual(point_on_line(p,l), True)
        
    def test_midpoint_on_line(self):
        p=Point(5,5)
        l=Line(0,0,10,10)
        self.assertEqual(point_on_line(p,l), True)

    def test_midpoint_on_horizontal_line(self):
        p=Point(5,0)
        l=Line(0,0,10,0)
        self.assertEqual(point_on_line(p,l), True)

    def test_midpoint_on_vertical_line(self):
        p=Point(0,5)
        l=Line(0,0,0,10)
        self.assertEqual(point_on_line(p,l), True)

    def test_midpoint_on_reversed_line(self):
        p=Point(5,5)
        l=Line(10,10,0,0)
        self.assertEqual(point_on_line(p,l), True)

    def test_point_not_on_line(self):
        p=Point(0,5)
        l=Line(10,10,0,0)
        self.assertEqual(point_on_line(p,l), False)

    def test_orthoganal_perpendicular_lines_intersect(self):
        l1=Line(0,1,10,1)
        l2=Line(2,5,2,-5)
        p=Point(0,0)
        
        self.assertEquals(line_intersects_line(l1,l2,p),True)
        self.assertEquals(p.x, 2)
        self.assertEquals(p.y, 1)
        
    def test_arbitrary_lines_interserct(self):
        l1=Line(0,0,10,10)
        l2=Line(0,4,10,6)
        p=Point(0,0)

        self.assertEquals(line_intersects_line(l1,l2,p),True)
        self.assertEquals(p.x,5)
        self.assertEquals(p.y,5)

    def test_parallel_lines_intersect(self):
        l1=Line(7,10,0,0)
        l2=Line(3.5,5,0,0)
        p=Point(0,0)

        self.assertEquals(line_intersects_line(l1,l2,p),True)
        self.assertEquals(p.x,3.5)
        self.assertEquals(p.y,5)

    def test_perpendicular_lines_dont_intersect(self):
        l1=Line(0,0,10,10)
        l2=Line(0,10,3,7)
        p=Point(0,0)

        self.assertEquals(line_intersects_line(l1,l2,p),False)
        self.assertEquals(p.x,0)
        self.assertEquals(p.y,0)

    def test_parallel_lines_dont_intersect(self):
        l1=Line(1,1,5,6)
        l2=Line(1,2,5,7)
        p=Point(0,0)

        self.assertEquals(line_intersects_line(l1,l2,p),False)
        self.assertEquals(p.x,0)
        self.assertEquals(p.y,0)
        
    def test_colinear_parallel_lines_dont_intersect(self):
        l1=Line(1,1,4,4)
        l2=Line(10,10,8,8)
        p=Point(0,0)

        self.assertEquals(line_intersects_line(l1,l2,p),False)
        self.assertEquals(p.x,0)
        self.assertEquals(p.y,0)

    def test_line_intersects_rectangle_side(self):
        l=Line(0,1, 10,3)
        r=Rect(5,0, 5,5)
        p=Point(0,0)

        self.assertEquals(line_intersects_rectangle(l,r,p),True)
        self.assertEquals(p.x,5)
        self.assertEquals(p.y,2)

    def test_line_intersects_rectangle_top(self):
        l=Line(2,10, 2,3)
        r=Rect(0,0, 5,5)
        p=Point(0,0)

        self.assertEquals(line_intersects_rectangle(l,r,p),True)
        self.assertEquals(p.x,2)
        self.assertEquals(p.y,5)

    def test_line_intersects_rectangle_bottom(self):
        l=Line(2,-10, 3,10)
        r=Rect(0,0, 5,5)
        p=Point(0,0)

        self.assertEquals(line_intersects_rectangle(l,r,p),True)
        self.assertEquals(p.x,2.5)
        self.assertEquals(p.y,0)

    def test_line_doesnt_intersect_rectangle(self):
        l=Line(2,-10, 3,10)
        r=Rect(5,5, 5,5)

        self.assertEquals(line_intersects_rectangle(l,r),False)
        
    def test_line_starts_in_rectangle(self):
        l=Line(3,4, 10,3)
        r=Rect(0,0,5,5)
        p=Point(0,0)

        self.assertEquals(line_intersects_rectangle(l,r,p),True)
        self.assertEquals(p.x,3)
        self.assertEquals(p.y,4)

    def test_distance_until_rectangles_intersect(self):
        r1=Rect(0,0,10,10)
        r2=Rect(15,5,10,10)
        v=Point(10,0)

        self.assertEquals(distance_until_rectangles_intersect(r1,v,r2),5)

    def test_moving_rectangles_dont_intersect(self):
        r1=Rect(0,0,3,3)
        r2=Rect(15,5,10,10)
        v=Point(1,0)

        self.assertEquals(distance_until_rectangles_intersect(r1,v,r2),None)

        
if __name__ == "__main__":
    unittest.main()
