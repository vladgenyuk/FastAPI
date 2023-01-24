from unittest import TestCase, main

class TEST(TestCase):
    def test(self):
        self.assertEqual(2+2, 4)
        self.assertEqual(2+2, 5)

    def test2(self):
        self.assertEqual(2+2, 4)
        self.assertEqual(2+2, 5)



if __name__ == "__main__":
    main()