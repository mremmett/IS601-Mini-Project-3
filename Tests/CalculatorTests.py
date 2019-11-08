import unittest
from Calculator.Calculator import Calculator
from CsvReader.CsvReader import CSVReader


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.calculator = Calculator()

    def test_instantiate_calculator(self):
        self.assertIsInstance(self.calculator, Calculator)

    def test_addition(self):
        test_data = CSVReader('CalcData/Unit_Test_Addition.csv').float_data
        for row in test_data:
            result = (row['Result'])
            self.assertEqual(self.calculator.add(row['Value 1'], row['Value 2']), result)
            self.assertEqual(self.calculator.result, row['Result'])

    def test_subtraction(self):
        test_data = CSVReader('CalcData/Unit_Test_Subtraction.csv').float_data
        for row in test_data:
            result = row['Result']
            self.assertEqual(self.calculator.subtract(row['Value 1'], row['Value 2']), result)
            self.assertEqual(self.calculator.result, row['Result'])

    def test_multiplication(self):
        test_data = CSVReader('CalcData/Unit_Test_Multiplication.csv').float_data
        for row in test_data:
            result = row['Result']
            self.assertEqual(self.calculator.multiply(row['Value 1'], row['Value 2']), result)
            self.assertEqual(self.calculator.result, row['Result'])

    def test_division(self):
        test_data = CSVReader('CalcData/Unit_Test_Division.csv').float_data
        for row in test_data:
            result = row['Result']
            self.assertEqual(self.calculator.divide(row['Value 1'], row['Value 2']), result)
            self.assertEqual(self.calculator.result, row['Result'])

    def test_square(self):
        test_data = CSVReader('CalcData/Unit_Test_Square.csv').float_data
        for row in test_data:
            result = row['Result']
            self.assertEqual(self.calculator.sqaure(row['Value 1'], result))
            self.assertEqual(self.calculator.result, row['Result'])

    def test_results_property(self):
        self.assertEqual(self.calculator.result, 0)


if __name__ == '__main__':
    unittest.main()