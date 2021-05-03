'''
    This File creates Tables at admin side.
    Different Tables will be generated automatically by django.
    Authors : Nishit Popat, Meet Patel, Manil Patel, Jay Patel

'''

#Importing of Required Models
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

#Contest Model creates Contest Tables which will include name of Contest and Date and Time of creation Of Contest.
class Contest(models.Model):
    contest_name = models.CharField(max_length=200)
    contest_date = models.DateTimeField('date published')

    def __str__(self):
        return self.contest_name

#Problem Table will save contest reference, problem name, problem definition, marks, testfile and inputfile.
class Problem(models.Model):
    contest_reference = models.ForeignKey(Contest, on_delete=models.CASCADE)
    problem_name = models.CharField(max_length=200)
    problem_definition = models.TextField(max_length=700)
    marks = models.IntegerField(default=0)
    testfile = models.FileField(upload_to='testfile/')
    inputfile = models.FileField(upload_to='inputfile/')

    def __str__(self):
        return self.problem_name

#ProblemSolved table will save relationship of user and problem it will have user_ref, contest_ref and problem_ref
# as foreign key and it will also save points_get and time_submitted as well.
class ProblemSolved(models.Model):
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE)
    contest_ref = models.ForeignKey(Contest, on_delete=models.CASCADE)
    problem_ref = models.ForeignKey(Problem, on_delete=models.CASCADE)
    points_get = models.IntegerField(default=0)
    time_submitted = models.DateTimeField('date published')
    
    #Here Meta class identifies unique key in table which is combintion of user_ref and problem_ref which means one user can solve
    #one problem only once. If user submits it second time it will just override the row and it will not create extra row.
    class Meta:
        unique_together = ("user_ref", "problem_ref")
        

    def __str__(self):
        return self.user_ref.username + " solved " + self.problem_ref.problem_name + " and got " + str(self.points_get) + " marks " 

#Snippet model stores code by the users
class Snippet(models.Model):
    #Text field which will have code
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    #ordering will be done whoever creates first
    class Meta:
        ordering = ('-created_at', )
