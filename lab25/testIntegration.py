import unittest
from lab25.integrationSystem import calculateStatusFunction, runIntegrationFunction

class IntegrationTestCase(unittest.TestCase):
    def testStatusFunction(self):
        data = [
            {"назва": "A", "стан": "готово"},
            {"назва": "B", "стан": "помилка"}
        ]
        result = calculateStatusFunction(data)
        self.assertEqual(result, {"всього": 2, "успіх": 1, "помилки": 1})

    def testRunFunction(self):
        text = runIntegrationFunction()
        self.assertIn("звіт інтеграції", text)
        self.assertIn("компонентів", text)

if __name__ == "__main__":
    unittest.main()