from django.db import models

class Scheduler(models.Model):
    dateFrom = models.DateField()
    dateTo = models.DateField()

    def __str__(self):
        return f'Urlop od {self.dateFrom} do {self.dateTo}'
