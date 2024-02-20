from typing import List, Dict, Union, Optional
from datetime import datetime
from .types.employee import Employee as EmployeePayload
from .types.position import Position as PositionPayload
from .types.category import Category as CategoryPayload
from .types.shift import Shift as ShiftPayload
from .types.timeoff import TimeOff as TimeOffPayload

'''
EqualityComparable and Hashable are implemented here in a similar way to that in which they are
implemented in the discord.py module.
'''


class EqualityComparable:
    __slots__ = ()

    id: int

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return other.id == self.id
        return NotImplemented


class Hashable(EqualityComparable):
    __slots__ = ()

    def __hash__(self) -> int:
        return self.id >> 22


class Result:
    def __init__(self, status_code: int, message: str = '', data: List[Dict] = None):
        """
        Result returned from RestAdapter

        :param status_code: HTTP status code
        :param message:
        :param data:
        """
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else []


class Employee(Hashable):
    def __init__(self, data: EmployeePayload) -> None:
        self._update(data)

    def __str__(self):
        emp_str_info = [
            f'(id: {self.id})',
            f'(name: {self.first_name} {self.last_name})'
        ]
        return ', '.join(emp_str_info)

    def _update(self, data: EmployeePayload) -> None:
        self.company_id = int(data['COMPANY_ID'])
        self.id = int(data['W2W_EMPLOYEE_ID'])
        self.employee_number = int(data['EMPLOYEE_NUMBER']) if data['EMPLOYEE_NUMBER'] else 0
        self.first_name = data['FIRST_NAME']
        self.last_name = data['LAST_NAME']
        self.primary_phone = data['PHONE']
        self.secondary_phone = data['PHONE_2']
        self.mobile_phone = data['MOBILE_PHONE']
        if ',' not in data['EMAILS']:
            self.emails = [data['EMAILS']]
        else:
            self.emails = data['EMAILS'].split(',')
        self.last_sign_in = datetime.strptime(data['LAST_SIGN_IN'], '%m/%d/%Y %I:%M:%S %p') \
            if data['LAST_SIGN_IN'] else None
        self.sign_in_count = int(data['SIGN_IN_COUNT'])
        self.address = data['ADDRESS']
        self.address_second_line = data['ADDRESS_2']
        self.city = data['CITY']
        self.state = data['STATE']
        self.zip_code = data['ZIP']
        self.comments = data['COMMENTS']
        self.max_hours_day = int(data['MAX_HRS_DAY'])
        self.max_shifts_day = int(data['MAX_SHIFTS_DAY'])
        self.max_hours_week = int(data['MAX_HRS_WEEK'])
        self.max_days_week = int(data['MAX_DAYS_WEEK'])
        self.hire_date = datetime.strptime(data['HIRE_DATE'], '%m/%d/%Y').date() if data['HIRE_DATE'] else None
        self.status = int(data['STATUS']) if data['STATUS'] else 0
        self.priority_group = int(data['PRIORITY_GROUP'])
        self.custom_field_1 = data['CUSTOM_1']
        self.custom_field_2 = data['CUSTOM_2']
        self.biweekly_target_hours = int(data['BIWEEKLY_TARGET_HRS']) if data['BIWEEKLY_TARGET_HRS'] else None
        self.pay_rate = data.get('PAY_RATE', None)
        self.alert_date = datetime.strptime(data['ALERT_DATE'], '%m/%d/%Y').date() if data['ALERT_DATE'] else None
        self.next_alert = datetime.strptime(data['NEXT_ALERT'], '%m/%d/%Y').date() if data['NEXT_ALERT'] else None


class Position(Hashable):
    def __init__(self, data: PositionPayload) -> None:
        self._update(data)

    def __str__(self):
        pos_str_info = [
            f'(id: {self.id})',
            f'(name: {self.position_name})'
        ]
        return ', '.join(pos_str_info)

    def _update(self, data: PositionPayload) -> None:
        self.company_id = int(data['COMPANY_ID'])
        self.id = int(data['POSITION_ID'])
        self.position_name = data['POSITION_NAME']
        self.position_custom1 = data['POSITION_CUSTOM1']
        self.position_custom2 = data['POSITION_CUSTOM2']
        self.position_custom3 = data['POSITION_CUSTOM3']
        self.last_changed_ts = datetime.strptime(data['LAST_CHANGED_TS'], '%m/%d/%Y %I:%M:%S %p')


class Category(Hashable):
    def __init__(self, data: CategoryPayload) -> None:
        self._update(data)

    def __str__(self):
        cat_str_info = [
            f'(id: {self.id})',
            f'(name: {self.category_name} [{self.category_short}])',
        ]
        return ', '.join(cat_str_info)

    def _update(self, data: CategoryPayload) -> None:
        self.company_id = int(data['COMPANY_ID'])
        self.id = int(data['CATEGORY_ID'])
        self.category_name = data['CATEGORY_NAME']
        self.category_short = data['CATEGORY_SHORT']
        self.category_custom1 = data['CATEGORY_CUSTOM1']
        self.category_custom2 = data['CATEGORY_CUSTOM2']
        self.category_custom3 = data['CATEGORY_CUSTOM3']
        self.last_changed_ts = datetime.strptime(data['LAST_CHANGED_TS'], '%m/%d/%Y %I:%M:%S %p') \
            if data.get('LAST_CHANGED_TS') else None


class Shift(Hashable):
    def __init__(self, data: ShiftPayload) -> None:
        self.employee: Optional[Employee] = None
        self.position: Optional[Position] = None
        self.category: Optional[Category] = None
        self._update(data)

    def __str__(self):
        shift_str_info = [
            f'(id: {self.id})'
            f'(employee: {self.employee})',
            f'(time: {self.start_datetime.isoformat()}-{self.end_datetime.isoformat()})',
            f'(position: {self.position})',
            f'(category: {self.category})'
        ]
        return ','.join(shift_str_info)

    @staticmethod
    def _handle_w2w_api_time(w2w_time: str):
        return w2w_time if ':' in w2w_time else f'{w2w_time[:-2]}:00{w2w_time[-2:]}'

    def _update(self, data: ShiftPayload) -> None:
        self.company_id = int(data['COMPANY_ID'])
        self.id = int(data['SHIFT_ID'])
        self.published = True if data['PUBLISHED'] == 'Y' else False
        self.w2w_employee_id = int(data['W2W_EMPLOYEE_ID'])
        self.start_datetime = datetime.strptime(f"{data['START_DATE']} {self._handle_w2w_api_time(data['START_TIME'])}",
                                                '%m/%d/%Y %I:%M%p')
        self.end_datetime = datetime.strptime(f"{data['END_DATE']} {self._handle_w2w_api_time(data['END_TIME'])}",
                                              '%m/%d/%Y %I:%M%p')
        self.duration = float(data['DURATION'])
        self.description = data['DESCRIPTION']
        self.position_id = int(data['POSITION_ID'])
        self.category_id = int(data['CATEGORY_ID']) if data['CATEGORY_ID'] else 0
        self.color_id = int(data['COLOR_ID'])
        self.pay_rate = data.get('PAY_RATE', None)
        self.last_changed_ts = datetime.strptime(data['LAST_CHANGED_TS'], '%m/%d/%Y %I:%M:%S %p')
        self.last_changed_by = data.get('LAST_CHANGED_BY', None)


class TimeOff(Hashable):
    def __init__(self, data: TimeOffPayload) -> None:
        self.employee = None
        self._update(data)

    def __str__(self):
        timeoff_str_info = [
            f'(id: {self.id})',
            f'(employee: {self.employee})',
            f'(time: {self.start_datetime} to {self.end_datetime})'
        ]
        return ', '.join(timeoff_str_info)

    @staticmethod
    def _handle_w2w_api_time(w2w_time: str):
        return w2w_time if ':' in w2w_time else f'{w2w_time[:-2]}:00{w2w_time[-2:]}'

    def _update(self, data: TimeOffPayload) -> None:
        self.company_id = int(data['COMPANY_ID'])
        self.id = int(data['TIMEOFF_ID'])
        self.w2w_employee_id = int(data['W2W_EMPLOYEE_ID'])
        self.description = data['DESCRIPTION']
        self.partial_day = True if data['PARTIAL_DAY'] == 'Y' else False
        self.start_datetime = datetime.strptime(f"{data['START_DATE']} {self._handle_w2w_api_time(data['START_TIME'])}",
                                                '%m/%d/%Y %I:%M%p')
        self.end_datetime = datetime.strptime(f"{data['END_DATE']} {self._handle_w2w_api_time(data['END_TIME'])}",
                                              '%m/%d/%Y %I:%M%p')
        self.when_requested_ts = datetime.strptime(data['WHEN_REQUESTED_TS'], '%m/%d/%Y %I:%M:%S %p') \
            if data.get('LAST_CHANGED_TS', None) else None
        self.last_changed_ts = datetime.strptime(data['LAST_CHANGED_TS'], '%m/%d/%Y %I:%M:%S %p')
        self.last_changed_by = data['LAST_CHANGED_BY']
