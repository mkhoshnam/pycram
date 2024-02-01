from bullet_world_testcase import BulletWorldTestCase
from pycram.pose import Pose
from geometry_msgs.msg import Point


class TestObject(BulletWorldTestCase):

    def test_set_position_as_point(self):
        self.milk.set_position(Point(1, 2, 3))
        self.assertEqual(self.milk.get_position_as_list(), [1, 2, 3])

    def test_set_position_as_pose(self):
        self.milk.set_position(Pose([1, 2, 3]))
        self.assertEqual(self.milk.get_position_as_list(), [1, 2, 3])

    def test_set_position_as_list(self):
        self.milk.set_position([1, 2, 3])
        self.assertEqual(self.milk.get_position_as_list(), [1, 2, 3])

    def test_save_state(self):
        self.robot.attach(self.milk)
        self.robot.save_state(1)
        self.assertEqual(self.robot.saved_states[1].attachments, self.robot.attachments)
        self.assertTrue(self.milk in self.robot.saved_states[1].attachments)
        for link in self.robot.links.values():
            self.assertEqual(link.get_current_state(), link.saved_states[1])

    def test_restore_state(self):
        self.robot.attach(self.milk)
        self.robot.save_state(1)
        self.milk.save_state(1)
        self.assertTrue(self.milk in self.robot.attachments)
        self.robot.detach(self.milk)
        self.assertTrue(self.milk not in self.robot.attachments)
        self.robot.restore_state(1)
        self.milk.restore_state(1)
        self.assertTrue(self.milk in self.robot.attachments)
        for link in self.robot.links.values():
            curr_state = link.get_current_state()
            saved_state = link.saved_states[1]
            self.assertEqual(curr_state, saved_state)
            self.assertEqual(curr_state.constraint_ids, saved_state.constraint_ids)