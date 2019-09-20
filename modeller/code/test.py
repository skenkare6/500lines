import unittest

import numpy
from mock import MagicMock
from viewer import Viewer
from node import Cube, Sphere


# https://stackoverflow.com/questions/5595425/what-is-the-best-way-to-compare-floats-for-almost-equality-in-python/33024979
def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.v = Viewer
        self.v.main_loop = MagicMock(name='main_loop')
        self.success = False
        self.key = ''
        self.node_type = None

    def node_interaction_test(self, obj):
        obj.interaction.handle_keystroke(self.key, 10, 10)
        start, direction = self.v.get_ray(obj, 10, 10)
        # place the node at the cursor in camera-space
        translation = (start + direction * obj.scene.PLACE_DEPTH)
        # convert the translation to world-space
        pre_tran = numpy.array([translation[0], translation[1], translation[2], 1])
        translation = obj.inverseModelView.dot(pre_tran)
        #why is array[1] inverse?
        for node in obj.scene.node_list:
            if isclose(translation[0], node.translation_matrix[0][3]) and \
                isclose(-translation[1], node.translation_matrix[1][3]) and \
                isclose(translation[2], node.translation_matrix[2][3]) and \
                isinstance(node, self.node_type):
                self.success = True
                break

    def test_create_object_sphere(self):
        # with 'S'
        self.key = 's'
        self.node_type = Sphere
        self.v.interaction_test = self.node_interaction_test
        self.v()
        self.assertTrue(self.success)
        # should check its a sphere and not just that it exists

    def test_create_object_cube(self):
        # with 'C'
        self.key = 'c'
        self.node_type = Cube
        self.v.interaction_test = self.node_interaction_test
        self.v()
        self.assertTrue(self.success)
        # should check its a cube and not just that it exists

    # def test_pick(self):
    #     self.key = 'd'
    #     self.v.interaction_test = self.node_interaction_test
    #     self.v()
    #     self.assertTrue(self.success)
    #
    # def test_rotate(self):
    #     # right click drag
    #     self.assertEqual(True, False)

    # def test_drag_object(self):
    #     # left click on object
    #     v = Viewer()
    #     modeller = subprocess.call(v.main_loop())
    #     m = PyMouse()
    #     x_dim, y_dim = m.screen_size()
    #     m.click(x_dim / 2, y_dim / 2, 1)
    #
    #     #find element, by id?
    #     #action chains drag and drop?
    #     self.assertEqual(True, False)

if __name__ == '__main__':
    unittest.main()
