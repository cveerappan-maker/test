from io import StringIO
import sys


def test_hello_world():
    captured = StringIO()
    sys.stdout = captured
    exec(open("hello_world.py").read())
    sys.stdout = sys.__stdout__
    assert captured.getvalue().strip() == "Hello, World!"
