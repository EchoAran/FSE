import unittest
import qheadache as q

class TestQheadache(unittest.TestCase):
    def test_parse_and_completion(self):
        walls, goals, boxes, player = q.parse_grid(q.PUZZLES[0]['grid'])
        self.assertEqual(player, (2, 1))
        self.assertIn((2, 2), boxes)
        self.assertIn((2, 3), goals)
        self.assertFalse(q.is_completed(boxes, goals))

    def test_legal_move_and_illegal_move(self):
        walls, goals, boxes, player = q.parse_grid(q.PUZZLES[0]['grid'])
        res = q.move_state(player, boxes, walls, goals, (0, 1))
        self.assertIsNotNone(res)
        p2, b2 = res
        self.assertEqual(p2, (2, 2))
        self.assertIn((2, 3), b2)
        self.assertIsNone(q.move_state(player, boxes, walls, goals, (0, -1)))

    def test_score(self):
        self.assertGreaterEqual(q.clamp_score(0, 0), q.clamp_score(1, 1))

if __name__ == '__main__':
    unittest.main()
