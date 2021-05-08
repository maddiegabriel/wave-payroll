from django.test import TestCase
from report.models import TimeLog, JobGroup
from datetime import datetime

class TimeLogModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        job_group_object = JobGroup.objects.create(name='A', wage=22)
        TimeLog.objects.create(date_worked='2021-05-07', hours_worked=8, employee_id=1, job_group=job_group_object, report_id=1)

    def test_employee_id_label(self):
        timelog = TimeLog.objects.get(id=1)
        field_label = timelog._meta.get_field('employee_id').verbose_name
        self.assertEqual(field_label, 'employee id')

    def test_report_id_label(self):
        timelog = TimeLog.objects.get(id=1)
        field_label = timelog._meta.get_field('report_id').verbose_name
        self.assertEqual(field_label, 'report id')

    def test_date_worked_label(self):
        timelog = TimeLog.objects.get(id=1)
        field_label = timelog._meta.get_field('date_worked').verbose_name
        self.assertEqual(field_label, 'date worked')

    def test_hours_worked_label(self):
        timelog = TimeLog.objects.get(id=1)
        field_label = timelog._meta.get_field('hours_worked').verbose_name
        self.assertEqual(field_label, 'hours worked')

    def test_job_group_label(self):
        timelog = TimeLog.objects.get(id=1)
        field_label = timelog._meta.get_field('job_group').verbose_name
        self.assertEqual(field_label, 'job group')

    def test_date_worked_format(self):
        timelog = TimeLog.objects.get(id=1)
        date_str = str(timelog.date_worked)
        date_object = datetime.strptime(date_str,'%Y-%m-%d')
        self.assertNotEqual(date_object, None)
    
    def test__str__(self):
        timelog = TimeLog.objects.get(id=1)
        expected_string = f'Employee #{timelog.employee_id} ({timelog.job_group.name}, ${timelog.job_group.wage}) worked {timelog.hours_worked} hours on {timelog.date_worked}.'
        self.assertEqual(expected_string, timelog.__str__())


class JobGroupModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        JobGroup.objects.create(name='B', wage=12)

    def test_name_label(self):
        job_group = JobGroup.objects.get(id=1)
        field_label = job_group._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_wage_label(self):
        job_group = JobGroup.objects.get(id=1)
        field_label = job_group._meta.get_field('wage').verbose_name
        self.assertEqual(field_label, 'wage')

    def test_wage_is_positive(self):
        job_group = JobGroup.objects.get(id=1)
        wage = float(job_group.wage)
        self.assertGreater(wage, 0.0)

    def test__str__(self):
        job_group = JobGroup.objects.get(id=1)
        expected_string = f'{job_group.name} (${job_group.wage})'
        self.assertEqual(expected_string, job_group.__str__())
