from src.test_publish.greet import say_hi


def test_greet():
    message = "hello"
    assert say_hi(message) == "hello"
