from django.db import models


class Contest(models.Model):
    contest_name = models.CharField(max_length=200)
    contest_date = models.DateTimeField('date published')

    def __str__(self):
        return self.contest_name


class Problem(models.Model):
    contest_reference = models.ForeignKey(Contest, on_delete=models.CASCADE)
    problem_name = models.CharField(max_length=200)
    problem_definition = models.CharField(max_length=700)
    marks = models.IntegerField(default=0)

    def __str__(self):
        return self.problem_name


