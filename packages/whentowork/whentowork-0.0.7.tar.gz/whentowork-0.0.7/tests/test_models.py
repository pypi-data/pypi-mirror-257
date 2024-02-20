import unittest
from unittest.mock import MagicMock
from whentowork.client import Client
from whentowork.models import Employee
from settings import W2W_TOKEN, W2W_HOSTNAME


class TestEmployee(unittest.TestCase):

    def setUp(self):
        self.client = Client(hostname=W2W_HOSTNAME, api_key=W2W_TOKEN)
        self.employee = self.client.employees[0]
        self.employee2 = self.client.employees[1]

    def test_employee(self):
        pass
        # self.assertEqual(self.employee.address, 3)

    # TODO
