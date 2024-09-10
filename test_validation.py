

import unittest
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.exc import DataError


# Define validation functions
def validate_open_close_high_low(value):
    if not isinstance(value, float):
        raise TypeError("Value must be a float")
    if value < 0:
        raise ValueError("Value must be non-negative")


def validate_volume(value):
    if not isinstance(value, int):
        raise TypeError("Value must be an integer")
    if value < 0:
        raise ValueError("Volume must be non-negative")


def validate_instrument(value):
    if not isinstance(value, str):
        raise TypeError("Value must be a string")


def validate_datetime(value):
    if not isinstance(value, datetime):
        raise TypeError("Value must be a datetime object")


class TestDataValidation(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.valid_data = {
            'open': 10.5,
            'close': 11.5,
            'high': 12.0,
            'low': 9.5,
            'volume': 1000,
            'instrument': 'AAPL',
            'datetime': datetime.now()
        }

    def test_validate_open_close_high_low(self):
        try:
            validate_open_close_high_low(self.valid_data['open'])
            validate_open_close_high_low(self.valid_data['close'])
            validate_open_close_high_low(self.valid_data['high'])
            validate_open_close_high_low(self.valid_data['low'])
        except (TypeError, ValueError) as e:
            self.fail(f"Validation failed: {e}")

    def test_validate_volume(self):
        try:
            validate_volume(self.valid_data['volume'])
        except (TypeError, ValueError) as e:
            self.fail(f"Validation failed: {e}")

    def test_validate_instrument(self):
        try:
            validate_instrument(self.valid_data['instrument'])
        except TypeError as e:
            self.fail(f"Validation failed: {e}")

    def test_validate_datetime(self):
        try:
            validate_datetime(self.valid_data['datetime'])
        except TypeError as e:
            self.fail(f"Validation failed: {e}")


if __name__ == '__main__':
    unittest.main()
