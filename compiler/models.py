from django.db import models

LANGUAGE_CHOICES = (
    ("cpp", "C++"),
    ("py", "Python"),
    ('java', 'Java'),
)

class CodeSubmission(models.Model):
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    code = models.TextField()
    input_data = models.TextField(blank=True, null=True)
    output_data = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.language} submission at {self.submitted_at}"
