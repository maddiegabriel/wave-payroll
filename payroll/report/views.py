import csv, io, json
from report.models import TimeLog, JobGroup
from report.utils import build_employee_report, build_pay_period, build_report
from report.utils import get_job_group, get_file_path, get_report_id, format_date
from report.serializers import TimeLogSerializer
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection

@api_view(['GET'])
def timelog_list(request, format=None):
    """
    On GET request to /report, queries DB and builds payroll response object
    """
    if request.method == 'GET':
        # This query uses the job_group foreign key in each TimeLog
        #   to retrieve the correct wage ($ per hour) from JobGroup
        wage_query = "SELECT report_jobgroup.wage FROM report_jobgroup \
                        WHERE report_jobgroup.id=job_group_id"
        
        # This query uses the wage above to calculate the earnings for each TimeLog entry
        # It also sets an end_date field for this TimeLog based on the date_worked
        # I set end_date (rather than start_date) because it would be more complicated to calculate later
        #   and I found SQLite provides some nice functions to manipulate dates within a query easily
        # Finally, it uses GROUP BY to combine TimeLog entries with the same employee ID and end_date (same pay period)
        # The results are ordered by (numeric) employee_id and then by pay period (as spec suggested)
        query = "SELECT employee_id, printf('%.2f', ROUND(SUM(hours_worked * (" + wage_query + ")), 2)) AS earnings, \
                    CASE WHEN CAST(strftime('%d', date(date_worked)) AS integer) <= 15 \
                            THEN date(date(date_worked), 'start of month', '+14 days') \
                         ELSE date(date(date_worked), 'start of month', '+1 month', '-1 day') \
                    END AS end_date \
                FROM report_timelog \
                GROUP BY employee_id, end_date \
                ORDER BY CAST(employee_id AS integer), end_date;"

        # execute the query!
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        full_report = build_report(result)

    # Build and return the JSON report (as per spec)
    return JsonResponse(json.dumps(full_report), safe=False)

@api_view(['POST'])
def upload(request):
    """
    On POST request to /upload, parses CSV and creates new timelogs in database
    """
    if request.method == 'POST':
        # retrieve and validate filename
        file_path = get_file_path(request.FILES['file'])
        if file_path is None:
            return Response({'error': 'You already uploaded this file!'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        report_id = get_report_id(request.FILES['file'].name)

        # open and parse CSV file line by line
        with open(file_path) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader, None) # skip header
            for row in reader:
                # normally I would validate each field better!
                date = format_date(row[0])
                hours, employee_id, job_group_name = row[1], row[2], row[3]
                # find or create new JobGroup object for Foreign Key column
                job_group_object = get_job_group(job_group_name)
                # create new TimeLog for this row!
                TimeLog.objects.create(date_worked=date, hours_worked=hours, employee_id=employee_id, job_group=job_group_object, report_id=report_id)
    return Response(status=status.HTTP_200_OK)

def index(request):
    """
    Displays home page of site on /.
    """
    # Render the HTML template index.html
    return render(request, 'index.html', context={})
