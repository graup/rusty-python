extern crate libc;

use libc::{size_t,uint32_t};
use std::mem;
use std::slice;

#[derive(Clone)]
pub struct Point {
    x: f64,
    y: f64
}

#[repr(C)]
pub struct Slice<T> {
    ptr: *mut T,
    len: usize,
}

/// Wraps a vector in our own slice to be on the safe side
/// Necessary as a native slice might be outlived
fn vec_to_slice(mut v: Vec<Point>) -> Slice<Point> {
    let p = v.as_mut_ptr();
    let len = v.len();

    // so that no destructor is run on our vector
    mem::forget(v);

    Slice { ptr: p, len: len }
}


/// Change a list of passed points inplace
#[no_mangle]
pub extern fn move_points_inplace(points: *const uint32_t, length: size_t, move_x: f64, move_y: f64) {
    // Map pointer to slice
    let points = unsafe { slice::from_raw_parts_mut(points as *mut Point, length as usize) };

    // Iterate over slice
    if points.len() > 0 {
        for p in points {
            p.x += move_x;
            p.y += move_y;
        }
    }
}

/// Change a list of passed points (working on a copy) and return result
#[no_mangle]
pub extern fn move_points(points: *const uint32_t, length: size_t, move_x: f64, move_y: f64) -> Slice<Point> {
    // Map pointer to slice
    let points = unsafe { slice::from_raw_parts(points as *mut Point, length as usize) };
    
    // Create a copy
    let mut points_copy: Vec<Point> = Vec::new();

    // Iterate over slice
    if points.len() > 0 {
        for p in points {
            let mut p_copy = p.clone();
            p_copy.x += move_x;
            p_copy.y += move_y; 
            points_copy.push(p_copy);
        }
    }

    vec_to_slice(points_copy)
}

/// Return a list of points
#[no_mangle]
pub extern fn get_points() -> Slice<Point> {
    // Map pointer to slice
    let points = vec![Point {x: 1.0, y: 1.0},
                      Point {x: 2.0, y: 2.0},
                      Point {x: 3.0, y: 3.0}];

    vec_to_slice(points)
}