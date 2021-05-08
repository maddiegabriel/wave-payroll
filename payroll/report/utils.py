from datetime import datetime
import csv, io, os
from report.models import TimeLog, JobGroup

def build_report(result):
    """
    Builds report response object in desired format
    """
    report = {
        "payrollReport": {
            "employeeReports": []
        }
    }
    # Build employeeReports object as per spec
    for row in result:
        employee_id, earnings, end_date = row[0], row[1], row[2]
        employee_report = build_employee_report(employee_id, earnings, end_date)
        report["payrollReport"]["employeeReports"].append(employee_report)
    return report

def build_employee_report(employee_id, earnings, end_date):
    """
    Builds a single employee's report using given information
    """
    # build a new employee report object
    employee_report = {}
    employee_report["employeeId"] = employee_id
    employee_report["payPeriod"] = build_pay_period(end_date)
    employee_report["amountPaid"] = f'${earnings}'
    return employee_report

def build_pay_period(end_date):
    """
    Builds a pay period object using the given period's end date
    """
    # use end date to set the appropriate start date
    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')
    start_date = end_date_dt
    if end_date_dt.day == 15:
        start_date = start_date.replace(day = 1)
    else:
        start_date = start_date.replace(day = 16)
    # build pay period object as per spec
    pay_period = {
        "startDate": start_date.strftime('%Y-%m-%d'),
        "endDate": end_date
    }
    return pay_period

def get_job_group(name):
    """
    Retrieves the job group object with the given name
    """
    # if this job group already exists, return it
    job_group_object = JobGroup.objects.filter(name=name).first()
    if job_group_object: return job_group_object
    # if this job group doesn't exist, make a new one based on spec
    if name == 'A': wage = 20
    else: wage = 30
    return JobGroup.objects.create(name=name, wage=wage)

def format_date(date):
    date_object = datetime.strptime(date,'%d/%m/%Y')
    new_format = date_object.strftime('%Y-%m-%d')
    return new_format

def get_file_path(file):
    """
    Validates file and returns path to file
    """
    if not is_valid_report(file.name): return None
    # add file to uploads folder for parsing
    if not os.path.exists('uploads/'): os.mkdir('uploads/')
    path = 'uploads/' + file.name
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return path

def is_valid_report(file_name):
    """
    Verifies if this file has already been uploaded (based on report_id)
    """
    report_id = get_report_id(file_name)
    # if there is at least one TimeLog stored with this report ID,
    #   then this file must have already been uploaded!
    time_logs = TimeLog.objects.filter(report_id=report_id).first()
    return time_logs is None

def get_report_id(file_name):
    """
    Extracts report_id from the given filename
    """
    # extract report ID from filename 'time-report-X.csv'
    # normally I would validate this!
    return file_name.split('-')[2].split('.')[0]