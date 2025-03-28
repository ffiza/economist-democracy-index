import unittest
from src.colors import Colors


class TestColorClass(unittest.TestCase):
    def test_opaque_from_transparency_01(self):
        color = "#1f77b4"
        target_color = "#d2e3f0"
        new_color = Colors.get_opaque_hex_from_transparency(color, 0.2)
        self.assertEqual(new_color, target_color)

    def test_opaque_from_transparency_02(self):
        color = "#ff7f0e"
        target_color = "#ffe5ce"
        new_color = Colors.get_opaque_hex_from_transparency(color, 0.2)
        self.assertEqual(new_color, target_color)


if __name__ == '__main__':
    unittest.main()
