import tempfile
import unittest
from pathlib import Path

import qheadache as q


class QheadacheTests(unittest.TestCase):
    def test_legal_move_updates_board_and_counts_one_action(self):
        a = q.start_attempt("p", "1")
        ok, _ = a.move_piece("B", "right")
        self.assertTrue(ok)
        self.assertEqual(a.moves, 1)
        self.assertEqual(a.board[1][0], ".")
        self.assertEqual(a.board[2][0], ".")
        self.assertEqual(a.board[1][1], "B")
        self.assertEqual(a.board[2][1], "B")

    def test_illegal_move_rejected_and_not_counted(self):
        a = q.start_attempt("p", "1")
        ok, _ = a.move_piece("A", "left")
        self.assertFalse(ok)
        self.assertEqual(a.moves, 0)

    def test_undo_marks_flag_and_restores_state(self):
        a = q.start_attempt("p", "1")
        a.move_piece("B", "right")
        ok, _ = a.undo()
        self.assertTrue(ok)
        self.assertTrue(a.undo_used)
        self.assertEqual(a.moves, 0)
        self.assertEqual(a.board, q.PUZZLES["1"]["board"])

    def test_completion_detected_on_goal_state(self):
        a = q.start_attempt("p", "1")
        a.board = q.clone_board(q.PUZZLES["1"]["goal"])
        self.assertTrue(a.goal_reached())

    def test_profile_separation(self):
        with tempfile.TemporaryDirectory() as td:
            old_profiles = q.PROFILES_DIR
            q.PROFILES_DIR = Path(td)
            try:
                s1 = q.ProfileStore("alice")
                s2 = q.ProfileStore("bob")
                a = q.start_attempt("alice", "1")
                a.moves = 3
                s1.set_progress("1", a)
                self.assertTrue(s1.save())
                self.assertNotEqual(s1.path, s2.path)
                self.assertIsNone(s2.get_progress("1"))
            finally:
                q.PROFILES_DIR = old_profiles


if __name__ == "__main__":
    unittest.main()
