import unittest

from lab33.programValidationService import calculateTicketPrice, validateProgramResults


class programValidationServiceTestCase(unittest.TestCase):
    def testAdultTicket(self):
        result = calculateTicketPrice(20, "adult")

        self.assertEqual(result.price, 50)

    def testChildTicket(self):
        result = calculateTicketPrice(20, "child")

        self.assertEqual(result.price, 25)

    def testStudentTicket(self):
        result = calculateTicketPrice(20, "student")

        self.assertEqual(result.price, 35)

    def testPensionerTicket(self):
        result = calculateTicketPrice(20, "pensioner")

        self.assertEqual(result.price, 30)

    def testMinimumPriceEdgeCase(self):
        result = calculateTicketPrice(3, "adult")

        self.assertEqual(result.price, 20)

    def testWrongDistance(self):
        with self.assertRaises(ValueError):
            calculateTicketPrice(0, "adult")

    def testWrongPassengerType(self):
        with self.assertRaises(ValueError):
            calculateTicketPrice(10, "worker")

    def testProgramValidation(self):
        testData = [
            (20, "adult", 50),
            (20, "child", 25),
            (20, "student", 35),
            (3, "adult", 20),
        ]

        self.assertTrue(validateProgramResults(testData))


if __name__ == "__main__":
    unittest.main()