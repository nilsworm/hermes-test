from greet import greet


def test_greets_a_provided_name():
    assert greet("Ada") == "Hello, Ada!"


def test_trims_surrounding_whitespace():
    assert greet("  Ada  ") == "Hello, Ada!"


def test_falls_back_to_there_for_empty_string():
    assert greet("") == "Hello, there!"


def test_falls_back_to_there_for_whitespace_only():
    assert greet("   ") == "Hello, there!"


def test_falls_back_to_there_when_called_with_no_arguments():
    assert greet() == "Hello, there!"
