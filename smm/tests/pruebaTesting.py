# -*- coding: utf-8 -*-
import unittest

from tools.GestorAlumnos import GestorAlumnos

class AllUniqueTests(unittest.TestCase):

  def test_all_unique(self):

    self.assertTrue (all_unique(""))
    self.assertTrue (all_unique("a"))




if __name__ == "__main__":
    unittest.main()
