from django.test import TestCase
from report.models import TimeLog, JobGroup
from django.urls import reverse
import json

class TimeLogListViewTest(TestCase):
    # see full diff
    maxDiff = None

    @classmethod
    def setUpTestData(cls):
        # Create some timelogs
        job_group_A_object = JobGroup.objects.create(name='A', wage=20)
        job_group_B_object = JobGroup.objects.create(name='B', wage=30)
        TimeLog.objects.create(date_worked='2020-01-04', hours_worked=10, employee_id='1', job_group=job_group_A_object, report_id=1)
        TimeLog.objects.create(date_worked='2020-01-14', hours_worked=5, employee_id='1', job_group=job_group_A_object, report_id=1)
        TimeLog.objects.create(date_worked='2020-01-20', hours_worked=3, employee_id='2', job_group=job_group_B_object, report_id=1)
        TimeLog.objects.create(date_worked='2020-01-20', hours_worked=4, employee_id='1', job_group=job_group_A_object, report_id=1)

    def test_response_is_correct(self):
        response = self.client.get('/report/')
        json_response = json.loads(response.content)
        expected = {
            "payrollReport": {
                "employeeReports": [
                    {
                        "employeeId": "1",
                        "payPeriod": {
                            "startDate": "2020-01-01",
                            "endDate": "2020-01-15"
                        },
                        "amountPaid": "$300.00"
                    },
                    {
                        "employeeId": "1",
                        "payPeriod": {
                            "startDate": "2020-01-16",
                            "endDate": "2020-01-31"
                        },
                        "amountPaid": "$80.00"
                    },
                    {
                        "employeeId": "2",
                        "payPeriod": {
                            "startDate": "2020-01-16",
                            "endDate": "2020-01-31"
                        },
                        "amountPaid": "$90.00"
                    }
                ]
            }
        }

        self.assertEqual(json_response, json.dumps(expected))
    
    def test_response_is_correct_new_employee(self):
        job_group_A_object = JobGroup.objects.create(name='A', wage=20)
        TimeLog.objects.create(date_worked='2021-07-06', hours_worked=1, employee_id='3', job_group=job_group_A_object, report_id=2)
        response = self.client.get('/report/')
        json_response = json.loads(response.content)
        expected = {
            "payrollReport": {
                "employeeReports": [
                    {
                        "employeeId": "1",
                        "payPeriod": {
                            "startDate": "2020-01-01",
                            "endDate": "2020-01-15"
                        },
                        "amountPaid": "$300.00"
                    },
                    {
                        "employeeId": "1",
                        "payPeriod": {
                            "startDate": "2020-01-16",
                            "endDate": "2020-01-31"
                        },
                        "amountPaid": "$80.00"
                    },
                    {
                        "employeeId": "2",
                        "payPeriod": {
                            "startDate": "2020-01-16",
                            "endDate": "2020-01-31"
                        },
                        "amountPaid": "$90.00"
                    },
                    {
                        "employeeId": "3",
                        "payPeriod": {
                            "startDate": "2021-07-01",
                            "endDate": "2021-07-15"
                        },
                        "amountPaid": "$20.00"
                    }
                ]
            }
        }

        self.assertEqual(json_response, json.dumps(expected))

    def test_response_is_correct_same_employee(self):
        job_group_A_object = JobGroup.objects.create(name='A', wage=20)
        TimeLog.objects.create(date_worked='2021-07-06', hours_worked=2, employee_id='2', job_group=job_group_A_object, report_id=3)
        response = self.client.get('/report/')
        json_response = json.loads(response.content)
        expected = {
            "payrollReport": {
                "employeeReports": [
                    {
                        "employeeId": "1",
                        "payPeriod": {
                            "startDate": "2020-01-01",
                            "endDate": "2020-01-15"
                        },
                        "amountPaid": "$300.00"
                    },
                    {
                        "employeeId": "1",
                        "payPeriod": {
                        "startDate": "2020-01-16",
                        "endDate": "2020-01-31"
                        },
                        "amountPaid": "$80.00"
                    },
                    {
                        "employeeId": "2",
                        "payPeriod": {
                            "startDate": "2020-01-16",
                            "endDate": "2020-01-31"
                        },
                        "amountPaid": "$90.00"
                    },
                    {
                        "employeeId": "2",
                        "payPeriod": {
                            "startDate": "2021-07-01",
                            "endDate": "2021-07-15"
                        },
                        "amountPaid": "$40.00"
                    }
                ]
            }
        }

        self.assertEqual(json_response, json.dumps(expected))
    
    def test_response_is_correct_middle_of_month(self):
        job_group_A_object = JobGroup.objects.create(name='A', wage=20)
        TimeLog.objects.create(date_worked='2020-01-15', hours_worked=1, employee_id='1', job_group=job_group_A_object, report_id=4)
        response = self.client.get('/report/')
        json_response = json.loads(response.content)
        expected = {
            "payrollReport": {
                "employeeReports": [
                    {
                        "employeeId": "1",
                        "payPeriod": {
                            "startDate": "2020-01-01",
                            "endDate": "2020-01-15"
                        },
                        "amountPaid": "$320.00"
                    },
                    {
                        "employeeId": "1",
                        "payPeriod": {
                            "startDate": "2020-01-16",
                            "endDate": "2020-01-31"
                        },
                        "amountPaid": "$80.00"
                    },
                    {
                        "employeeId": "2",
                        "payPeriod": {
                            "startDate": "2020-01-16",
                            "endDate": "2020-01-31"
                        },
                        "amountPaid": "$90.00"
                    }
                ]
            }
        }

        self.assertEqual(json_response, json.dumps(expected))

    def test_response_is_correct_end_of_month(self):
        job_group_A_object = JobGroup.objects.create(name='A', wage=20)
        TimeLog.objects.create(date_worked='2020-01-31', hours_worked=1, employee_id='1', job_group=job_group_A_object, report_id=5)
        response = self.client.get('/report/')
        json_response = json.loads(response.content)
        expected = {
            "payrollReport": {
                "employeeReports": [
                    {
                        "employeeId": "1",
                        "payPeriod": {
                            "startDate": "2020-01-01",
                            "endDate": "2020-01-15"
                        },
                        "amountPaid": "$300.00"
                    },
                    {
                        "employeeId": "1",
                        "payPeriod": {
                            "startDate": "2020-01-16",
                            "endDate": "2020-01-31"
                        },
                        "amountPaid": "$100.00"
                    },
                    {
                        "employeeId": "2",
                        "payPeriod": {
                            "startDate": "2020-01-16",
                            "endDate": "2020-01-31"
                        },
                        "amountPaid": "$90.00"
                    }
                ]
            }
        }

        self.assertEqual(json_response, json.dumps(expected))
    
    def test_response_is_correct_start_of_month(self):
        job_group_A_object = JobGroup.objects.create(name='A', wage=20)
        TimeLog.objects.create(date_worked='2020-01-01', hours_worked=1, employee_id='1', job_group=job_group_A_object, report_id=6)
        response = self.client.get('/report/')
        json_response = json.loads(response.content)
        expected = {
            "payrollReport": {
                "employeeReports": [
                    {
                        "employeeId": "1",
                        "payPeriod": {
                            "startDate": "2020-01-01",
                            "endDate": "2020-01-15"
                        },
                        "amountPaid": "$320.00"
                    },
                    {
                        "employeeId": "1",
                        "payPeriod": {
                            "startDate": "2020-01-16",
                            "endDate": "2020-01-31"
                        },
                        "amountPaid": "$80.00"
                    },
                    {
                        "employeeId": "2",
                        "payPeriod": {
                            "startDate": "2020-01-16",
                            "endDate": "2020-01-31"
                        },
                        "amountPaid": "$90.00"
                    }
                ]
            }
        }

        self.assertEqual(json_response, json.dumps(expected))
