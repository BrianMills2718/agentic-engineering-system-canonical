from greeter import greet


def test_greets_the_name():
    assert greet("Ada") == "Hello, Ada!"
