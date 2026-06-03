import unittest

from lab32.productVariantService import calculateOrder, compareVariants, getDiscountPercent


class productVariantServiceTestCase(unittest.TestCase):
    def testBasicVariantWithoutDiscount(self):
        result = calculateOrder(100, 2, "basic")

        self.assertEqual(result.basePrice, 200)
        self.assertEqual(result.discount, 0)
        self.assertEqual(result.delivery, 80)
        self.assertEqual(result.total, 280)

    def testStandardVariantWithSmallOrderDiscount(self):
        result = calculateOrder(100, 2, "standard")

        self.assertEqual(result.discount, 10)
        self.assertEqual(result.delivery, 50)
        self.assertEqual(result.total, 240)

    def testPremiumVariantWithFreeDelivery(self):
        result = calculateOrder(100, 2, "premium")

        self.assertEqual(result.discount, 20)
        self.assertEqual(result.delivery, 0)
        self.assertEqual(result.total, 180)

    def testQuantityEdgeCaseForDiscount(self):
        self.assertEqual(getDiscountPercent("basic", 9), 0)
        self.assertEqual(getDiscountPercent("basic", 10), 5)
        self.assertEqual(getDiscountPercent("standard", 10), 10)
        self.assertEqual(getDiscountPercent("premium", 10), 15)

    def testWrongPrice(self):
        with self.assertRaises(ValueError):
            calculateOrder(0, 3, "basic")

    def testWrongQuantity(self):
        with self.assertRaises(ValueError):
            calculateOrder(100, 0, "basic")

    def testWrongVariant(self):
        with self.assertRaises(ValueError):
            calculateOrder(100, 1, "vip")

    def testCompareVariants(self):
        results = compareVariants(100, 2)

        self.assertEqual(results[0].variant, "premium")
        self.assertEqual(results[-1].variant, "basic")


if __name__ == "__main__":
    unittest.main()