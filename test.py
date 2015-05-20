from ctypes import *
rust_lib = cdll.LoadLibrary("target/release/librusty_python.dylib")

# Inspired by
# https://avacariu.me/articles/calling-rust-from-python.html


class Point(Structure):
    _fields_ = [("x", c_double), ("y", c_double)]

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "<Point x=%.4f, y=%.4f>" % (self.x, self.y)


class Slice(Structure):
    _fields_ = [("ptr", POINTER(Point)), ("len", c_uint64)]

    def __init__(self, a_list):
        self.ptr = byref(a_list)
        self.len = len(a_list)


if __name__ == '__main__':

    points = [Point(0, 0), Point(3, 3), Point(4, 4)]

    print "Initial points ", points

    # Setup types
    PointListType = Point * len(points)

    rust_lib.get_points.restype = Slice

    rust_lib.move_points.argtypes = (PointListType, c_size_t, c_double, c_double)
    rust_lib.move_points.restype = Slice

    rust_lib.move_points_inplace.argtypes = (PointListType, c_size_t, c_double, c_double)
    rust_lib.move_points_inplace.restype = None

    # Test returning of list
    v = rust_lib.get_points()

    points = [v.ptr[i] for i in range(v.len)]
    assert points[0].x == 1.0
    assert points[1].x == 2.0
    print "Returned points", points

    # Test passing of list and changing inplace
    c_points = PointListType(*points)
    rust_lib.move_points_inplace(c_points, len(points), 1.5, 2.5)

    points = [c_points[i] for i in range(len(points))]
    assert points[0].x == 1.5
    assert points[1].x == 1.5
    print "Moved points (A) ", points

    # Test passing and returning of list
    v = rust_lib.move_points(c_points, len(points), 5.5, 2.5)

    points = [v.ptr[i] for i in range(v.len)]
    assert points[0].x == 5.5
    assert points[1].x == 5.5
    print "Moved points (B) ", points
