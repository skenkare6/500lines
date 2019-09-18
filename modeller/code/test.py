import unittest
from mock import MagicMock

class MyTestCase(unittest.TestCase):
    def test_create_object_sphere(self):
        # with 'S'
        self.assertEqual(True, False)

    def test_create_object_cube(self):
        # with 'D'
        self.assertEqual(True, False)

    def test_pan(self):
        # middle click drag
        self.assertEqual(True, False)

    def test_rotate(self):
        # right click drag
        self.assertEqual(True, False)

    def test_drag_object(self):
        # left click on object
        self.assertEqual(True, False)

if __name__ == '__main__':
    unittest.main()
