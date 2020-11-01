from django.db import models

import pytz
import datetime
tz = pytz.timezone('Asia/Bangkok')
dateTime = datetime.datetime.now(tz)

class Statement(models.Model):
    statement_date = models.DateField(default=dateTime)
    statement_description = models.CharField(max_length=128)
    statement_income = models.DecimalField(decimal_places=2, max_digits=7)
    statement_expense = models.DecimalField(decimal_places=2, max_digits=7)

# Create your models here.
