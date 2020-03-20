from django.db import models


class University(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class Student(models.Model):
    name = models.CharField(max_length=100)
    university = models.ManyToManyField(University)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
