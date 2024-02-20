import datetime
from unittest import TestCase
from unittest.mock import MagicMock, Mock, create_autospec, patch
import requests

from whentowork.models import Shift
import whentowork.adapter
from whentowork.client import Client
from settings import W2W_TOKEN, W2W_HOSTNAME


class TestClient(TestCase):

    def setUp(self):
        self.client = Client(hostname=W2W_HOSTNAME, api_key=W2W_TOKEN)
        # self.client.request_date_partitions = MagicMock(return_value=3)
        self.mock_client = Mock()
        self.response = requests.Response()

    def test__update_categories(self):
        self.assertEqual(self.client._update_categories(), False)

    def test_test(self):
        start_date = datetime.date(2024, 2, 1)
        end_date = datetime.date(2024, 2, 16)
        timeoff = self.client.get_timeoff_by_date(start_date, end_date)
        print(timeoff)
        for to_request in timeoff:
            print(to_request)

    def test_get_shifts_by_date(self):
        start_date = datetime.date(2024, 2, 1)
        end_date = datetime.date(2024, 2, 16)
        shifts = self.client.get_shifts_by_date(start_date, end_date)

    def test_get_timeoff_by_date(self):
        with patch('whentowork.adapter.Adapter', autospec=True) as adapter:
            self.client._adapter = adapter
            start_date = datetime.date(2024, 2, 1)
            end_date = datetime.date(2024, 2, 16)
            timeoff = self.client.get_timeoff_by_date(start_date, end_date)
            adapter.get_from_endpoint.assert_called()

    # TODO

    def test__update_company(self):
        self.fail()

    def test__update_employees(self):
        self.fail()

    def test__update_positions(self):
        self.fail()

    def test__add_emp_pos_cat_to_shift(self):
        self.fail()

    def test__add_emp_to_timeoff(self):
        self.fail()

    def test_get_employee_by_id(self):
        self.fail()

    def test_get_position_by_id(self):
        self.fail()

    def test_get_category_by_id(self):
        self.fail()
