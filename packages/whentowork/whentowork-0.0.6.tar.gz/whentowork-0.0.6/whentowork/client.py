import datetime
from logging import Logger
from typing import List, Tuple, Optional
from datetime import date
from .adapter import Adapter
from .models import Employee, Category, Position, Shift, TimeOff


class Client:
    def __init__(self, hostname: str, api_key: str, ssl_verify: bool = True, logger: Logger = None):
        self._adapter = Adapter(hostname, api_key, ssl_verify, logger)
        self.company_id: int = 0
        self.employees: List[Employee] = []
        self.positions: List[Position] = []
        self.categories: List[Category] = []
        self._init_company()

    def _init_company(self) -> None:
        self._init_employees()
        self.company_id = self.employees[0].company_id
        self._init_positions()
        self._init_categories()

    def _init_employees(self) -> None:
        self.employees = self._adapter.get_from_endpoint('EmployeeList')

    def _update_employees(self) -> bool:
        updated_employees = self._adapter.get_from_endpoint('EmployeeList')
        updated = False
        for employee in updated_employees:
            if employee not in self.employees:
                self.employees.append(employee)
                updated = True
        return updated

    def _init_positions(self) -> None:
        self.positions = self._adapter.get_from_endpoint('PositionList')

    def _update_positions(self) -> bool:
        updated_positions = self._adapter.get_from_endpoint('PositionList')
        updated = False
        for position in updated_positions:
            if position not in self.positions:
                self.positions.append(position)
                updated = True
        return updated

    def _init_categories(self) -> None:
        self.categories = self._adapter.get_from_endpoint('CategoryList')

    def _update_categories(self) -> bool:
        updated_categories = self._adapter.get_from_endpoint('CategoryList')
        updated = False
        for category in updated_categories:
            if category not in self.categories:
                self.categories.append(category)
                updated = True
        return updated

    def _add_emp_pos_cat_to_shift(self, shift: Shift) -> None:
        shift.employee = self.get_employee_by_id(shift.w2w_employee_id)
        shift.position = self.get_position_by_id(shift.position_id)
        shift.category = self.get_category_by_id(shift.category_id)

    def _add_emp_to_timeoff(self, timeoff: TimeOff) -> None:
        timeoff.employee = self.get_employee_by_id(timeoff.w2w_employee_id)

    def get_employee_by_id(self, w2w_employee_id: int) -> Optional[Employee]:
        if not isinstance(w2w_employee_id, int):
            raise TypeError("w2w_employee_id must be an integer")
        for employee in self.employees:
            if w2w_employee_id == employee.id:
                return employee

        updated = self._update_employees()
        if updated:
            for employee in self.employees:
                if w2w_employee_id == employee.id:
                    return employee
        return None

    def get_position_by_id(self, position_id: int) -> Optional[Position]:
        if not isinstance(position_id, int):
            raise TypeError("position_id must be an integer")
        for position in self.positions:
            if position_id == position.id:
                return position

        updated = self._update_positions()
        if updated:
            for position in self.positions:
                if position_id == position.id:
                    return position
        return None

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        if not isinstance(category_id, int):
            raise TypeError("category_id must be an integer")
        for category in self.categories:
            if category_id == category.id:
                return category

        updated = self._update_categories()
        if updated:
            for category in self.categories:
                if category_id == category.id:
                    return category
        return None

    def get_shifts_by_date(self, start_date: date, end_date: date) -> List[Shift]:
        self.validate_dates(start_date, end_date)
        shifts = []
        for date_partition in self.request_date_partitions(start_date, end_date):
            shifts.extend(self._adapter.get_from_endpoint('AssignedShiftList', date_partition[0], date_partition[1]))
        for shift in shifts:
            self._add_emp_pos_cat_to_shift(shift)
        return shifts

    def get_timeoff_by_date(self, start_date: date, end_date: date) -> List[TimeOff]:
        self.validate_dates(start_date, end_date)
        timeoff_requests = []
        for date_partition in self.request_date_partitions(start_date, end_date):
            timeoff_requests.extend(self._adapter.get_from_endpoint(
                'ApprovedTimeOff', date_partition[0], date_partition[1]))
        for request in timeoff_requests:
            self._add_emp_to_timeoff(request)
        return timeoff_requests

    @staticmethod
    def validate_dates(start_date: date, end_date: date) -> None:
        if not isinstance(start_date, date):
            raise TypeError("start_date must be of type datetime.date")
        if not isinstance(end_date, date):
            raise TypeError("end_date must be of type datetime.date")
        if start_date > end_date:
            raise ValueError("start_date before end_date")
        if end_date - start_date > datetime.timedelta(365*3):
            raise ValueError("Time difference between start_date and end_date cannot exceed 3 years")

    @staticmethod
    def request_date_partitions(start_date: date, end_date: date) -> List[Tuple]:
        moving_start_date = start_date
        date_partition = []
        while end_date - moving_start_date > datetime.timedelta(31):
            date_partition.append((moving_start_date, moving_start_date + datetime.timedelta(31)))
            moving_start_date += datetime.timedelta(32)
        date_partition.append((moving_start_date, end_date))
        return date_partition

