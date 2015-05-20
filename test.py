from ctypes import *
rust_lib = cdll.LoadLibrary("target/release/librusty_python.dylib")


class Point(Structure):
    _fields_ = [("x", c_double), ("y", c_double)]

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return "<Point x=%.4f, y=%.4f>" % (self.x, self.y)


class Slice(Structure):
    _fields_ = [("ptr", POINTER(Point)), ("len", c_uint64)]

    def __init__(self, a_list):
        self.ptr = byref(a_list)
        self.len = len(a_list)


if __name__ == '__main__':
    # Setup types
    rust_lib.get_points.restype = Slice

    # Test returning of list
    v = rust_lib.get_points()

    points = [v.ptr[i] for i in range(v.len)]
    print "Returned points: ", points
    assert points[0] == Point(1.0, 1.0)
    assert points[1] == Point(2.0, 2.0)
    assert points[2] == Point(3.0, 3.0)

    # Setup types
    PointListType = Point * len(points)
    rust_lib.move_points.argtypes = (PointListType, c_size_t, c_double, c_double)
    rust_lib.move_points.restype = Slice

    rust_lib.move_points_inplace.argtypes = (PointListType, c_size_t, c_double, c_double)
    rust_lib.move_points_inplace.restype = None

    # Test passing of list and changing inplace
    c_points = PointListType(*points)  # Make a pointer to a copy of the list
    rust_lib.move_points_inplace(c_points, len(points), 1.0, 2.0)

    points = [c_points[i] for i in range(len(points))]  # Map pointer back to list
    print "Moved points (A):", points
    assert points[0] == Point(2.0, 3.0)
    assert points[1] == Point(3.0, 4.0)
    assert points[2] == Point(4.0, 5.0)

    # Test passing and returning of list
    v = rust_lib.move_points(c_points, len(points), 5.5, 2.5)

    points = [v.ptr[i] for i in range(v.len)]  # Map pointer back to list
    print "Moved points (B):", points
    assert points[0] == Point(7.5, 5.5)
    assert points[1] == Point(8.5, 6.5)
    assert points[2] == Point(9.5, 7.5)

    print "All tests passed."
