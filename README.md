# Rusty Python

This is a test repo to try out different ways of interfacing Python and Rust.

I was heavily inspired by [this blogpost](https://avacariu.me/articles/calling-rust-from-python.html) and random googling around. At some point I thought it would be nice to put together everything I had learned.

## How to run

    cargo build --release
    python test.py

## What this shows

[Rust Inside Other Languages](http://doc.rust-lang.org/1.0.0/book/rust-inside-other-languages.html), the example being Python.

At the moment this is about using Rust code as a library inside Python, so this does the following:

- Calling a Rust function passing parameters, e.g. pointers to lists
  - Modifying the referenced objects inplace (i.e. Rust accessing the same memory)
  - Returning new objects in Rust, passing them back to Python