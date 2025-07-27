from django.db import models
from problems.models import Problem


class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='testcases')
    input_data = models.TextField()
    expected_output = models.TextField()

def __str__(self):
    return f"TestCase for Problem {self.problem.id}"
