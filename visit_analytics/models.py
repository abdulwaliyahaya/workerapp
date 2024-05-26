from django.db import models


class Worker(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    phone_number = models.CharField(max_length=255, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.name


class Visit(models.Model):
    time_stamp = models.DateTimeField(auto_now_add=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, blank=False, null=False)
    latitude = models.FloatField(blank=False, null=False)
    longitude = models.FloatField(blank=False, null=False)

    def __str__(self):
        visit_representation = '{} - {}'.format(self.unit.name, self.time_stamp)
        return visit_representation

