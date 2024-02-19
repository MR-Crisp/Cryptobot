import unittest
import tools
import random
from datetime import datetime


class TestTools(unittest.TestCase):
    def test_MA(self):
        stocks = ['AAPL','TSLA','MCSFT','AMZN','AAT','AB','AIR','AMAT']
        startDate = f"{random.randint(2011, 2014)}-{random.randint(1,12)}-{random.randint(1,28)}"
        endDate = f"{random.randint(2015, 2022)}-{random.randint(1,12)}-{random.randint(1,28)}"
        ma = tools.averageCrossover(random.choice(stocks), startDate, endDate, 4, 20)
        ma.calc_MA()
        self.assertIsNotNone(ma.profit)


    def test_format_date(self):
        pivot = tools.PivotPoints("AAPL", "2017-10-15", "2022-10-13", 0, 0, 0, 0, 0)
        formatted_date = pivot.formatDate('2023-01-01')
        self.assertEqual(formatted_date, datetime(2023, 1, 1))

    def test_merge_list(self):
        # Provide valid arguments for symbol, start date, end date, and other parameters
        pivot = tools.PivotPoints("AAPL", "2017-10-15", "2022-10-13", 0, 0, 0, 0, 0)
        merged_list = pivot.merge_list([1.5, 2.0, 2.5, 3.5, 7.0], 0.5)
        self.assertEqual(merged_list, [1.5, 2.5,3.5, 7.0])



    def test_compare_pivots(self):
        pivot = tools.PivotPoints("AAPL", "2017-10-15", "2022-10-13", 0, 0, 0, 0, 0)
        init_price = 100
        current_price = 110
        pivot_list = [105, 108, 115]
        result = pivot.compare_pivots(init_price, current_price, pivot_list)
        self.assertTrue(result)

    def test_algo_buy_sell(self):
        stocks = ['AAPL', 'TSLA', 'MSFT', 'AMZN', 'AAT', 'AB', 'AIR', 'AMAT']
        startDate = str(random.randint(2011, 2014)) + '-' + str(random.randint(1, 12)) + '-' + str(
            random.randint(1, 30))
        endDate = str(random.randint(2015, 2022)) + '-' + str(random.randint(1, 12)) + '-' + str(
            random.randint(1, 30))
        ma = tools.averageCrossover(random.choice(stocks), startDate, endDate, 4, 20)
        ma.calc_MA()  # Calculate moving averages
        ma.algo(1000)  # Run the algorithm
        self.assertNotEqual(ma.profit, 0)

    def test_algo_no_buy(self):
        # Test the scenario where the algorithm does not execute any buy/sell operations
        symbol = 'AAPL'
        startDate = '2023-01-01'
        endDate = '2023-01-10'
        ma = tools.averageCrossover(symbol, startDate, endDate, 4, 20)
        ma.calc_MA()
        capital = 10000
        ma.algo(capital)
        self.assertEqual(ma.profit, 0)


if __name__ == '__main__':
    unittest.main()
