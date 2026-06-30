from greet import greet


def test_greets_a_provided_name():
    assert greet("Ada") == "Hello, Ada!"
