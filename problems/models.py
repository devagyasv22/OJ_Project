from django.db import models

class Problem(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)  # for cleaner URLs
    statement = models.TextField()
    input_format = models.TextField()
    output_format = models.TextField()
    constraints = models.TextField()
    sample_input = models.TextField()
    sample_output = models.TextField()

    def __str__(self):
        return self.title

