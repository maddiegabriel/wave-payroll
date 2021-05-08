from django.db import models
# Used to generate URLs by reversing the URL patterns
from django.core.validators import MinValueValidator
import datetime

class JobGroup(models.Model):
    """Model representing a job group."""
    name = models.CharField(max_length=200, default='A')
    wage = models.DecimalField(decimal_places=2, max_digits=200, validators=[MinValueValidator(0)],default=0.00)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name} (${self.wage})'

class TimeLog(models.Model):
    """Model representing a single Time Log."""
    employee_id = models.CharField(max_length=200, default='0')
    report_id = models.IntegerField(default=0)
    date_worked = models.DateField(default=datetime.date.today)
    hours_worked = models.DecimalField(default=0.0,decimal_places=2, max_digits=200, validators=[MinValueValidator(0)])
    # ForeignKey used because each Time Log can have only one Job Group, but Job Groups can appear in many Time Logs.
    # JobGroup class has already been defined so we can specify the object above.
    job_group = models.ForeignKey('JobGroup', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'Employee #{self.employee_id} ({self.job_group.name}, ${self.job_group.wage}) worked {self.hours_worked} hours on {self.date_worked}.'

    # Defines desired ordering of records returned when I query this model type
    class Meta:
        ordering = ['employee_id', 'date_worked']