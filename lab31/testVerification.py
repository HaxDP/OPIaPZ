import unittest

from lab31.verificationService import calculateDiscount, checkCodeStyle


class verificationTestCase(unittest.TestCase):
    def testCalculateDiscount(self):
        self.assertEqual(calculateDiscount(200, 25), 150)
        self.assertEqual(calculateDiscount(99.99, 10), 89.99)

    def testWrongPrice(self):
        with self.assertRaises(ValueError):
            calculateDiscount(-10, 5)

    def testWrongPercent(self):
        with self.assertRaises(ValueError):
            calculateDiscount(100, 130)

    def testStaticCheck(self):
        result = checkCodeStyle("print('hello')")
        self.assertTrue(all(item.success for item in result))

    def testStaticCheckFindsEval(self):
        result = checkCodeStyle("eval('2 + 2')")
        self.assertFalse(result[0].success)


if __name__ == "__main__":
    unittest.main()