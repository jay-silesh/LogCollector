import unittest
from src.hello_world import HelloWorld
from ddt import ddt, data, unpack


@ddt
class TestHelloWorld(unittest.TestCase):
    @data(
        ("test", "Hello test"),
        ("test_2", "Hello test_2"),
    )
    @unpack
    def test_print_hello_word(self, given_data: str, expected_data: str):
        c = HelloWorld()
        self.assertEqual(c.print_hello_world(given_data), expected_data)


if __name__ == "__main__":
    unittest.main()
