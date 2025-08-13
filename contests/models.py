# contests/models.py
from django.db import models
from django.conf import settings
from problems.models import Problem

class Contest(models.Model):
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    problems = models.ManyToManyField(Problem, related_name='contests')

    def has_started(self):
        from django.utils import timezone
        return timezone.now() >= self.start_time

    def has_ended(self):
        from django.utils import timezone
        return timezone.now() > self.end_time

class ContestSubmission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=20)
    verdict = models.CharField(max_length=20)  # AC, WA, TLE, etc.
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['submitted_at']
