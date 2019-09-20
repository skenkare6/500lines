import unittest

import numpy
from OpenGL.GLUT import GLUT_LEFT_BUTTON, GLUT_DOWN, GLUT_MIDDLE_BUTTON, GLUT_RIGHT_BUTTON
from mock import MagicMock, patch
from viewer import Viewer
from node import Cube, Sphere, SnowFigure, Node
from trackball import Trackball


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

    def test_create_object_figure(self):
        self.key = 'f'
        self.node_type = SnowFigure
        self.v.interaction_test = self.node_interaction_test
        self.v()
        self.assertTrue(self.success)

    def mouse_interaction_test(self, obj):
        # 270, 217 is the default x,y of the sphere
        obj.interaction.handle_keystroke('s', 10, 10)
        obj.interaction.handle_mouse_button(self.key, GLUT_DOWN, 10, 10)
        if obj.scene.node_list[3].selected:
            self.success = True

    def test_pick_sphere(self):
        self.key = GLUT_LEFT_BUTTON
        self.node_type = Sphere
        self.v.interaction_test = self.mouse_interaction_test
        self.v()
        self.assertTrue(self.success)

    def pan_interaction_test(self, obj):
        # 270, 217 is the default x,y of the sphere
        obj.interaction.pressed = GLUT_MIDDLE_BUTTON
        obj.interaction.mouse_loc = [10,10,]
        with patch('interaction.Interaction.translate') as thing:
            obj.interaction.handle_mouse_move(10, 10)
            thing.assert_called()
            self.success = True

    def test_pan_scene(self):
        self.v.interaction_test = self.pan_interaction_test
        self.v()
        self.assertTrue(self.success)


    def test_rotate_scene(self):
        self.v.interaction_test = self.rotate_interaction_test
        self.v()
        self.assertTrue(self.success)

    def rotate_interaction_test(self, obj):
        # 270, 217 is the default x,y of the sphere
        obj.interaction.pressed = GLUT_RIGHT_BUTTON
        obj.interaction.mouse_loc = [10,10,]
        with patch('trackball.Trackball.drag_to') as thing:
            obj.interaction.handle_mouse_move(15, 15)
            thing.assert_called()
            self.success = True

if __name__ == '__main__':
    unittest.main()
