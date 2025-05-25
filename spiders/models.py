from django.db import models

# Create your models here.
from django.db import models
#model for every job listing

class Job(models.Model):
    job_id = models.CharField(max_length=100, unique=True)
    Industry = models.CharField(max_length=100)
    Title = models.CharField(max_length=255)
    Company = models.CharField(max_length=255)
    Location = models.CharField(max_length=255)
    Type_of_Work = models.CharField(max_length=100, null=True, blank=True)
    Experience = models.CharField(max_length=100, null=True, blank=True)
    Employment_type = models.JSONField(default=list)  # List of types like ["b2b", "permanent"]
    Operating_mode = models.CharField(max_length=50, null=True, blank=True)
    Requirements = models.JSONField(default=list)  # List of skill strings
    Url = models.CharField(max_length=300)  # Contains just the slug, e.g. "company-role-slug"

    def __str__(self):
        return f"{self.Title} at {self.Company}"
