from django.db import models
from datetime import datetime

# Create your models here.
# Basically, it is creating a table called 'Tutorial', columns......etc
class Tutorial(models.Model):
    tutorial_title = models.CharField(max_length=200)
    tutorial_contents = models.TextField()
    tutorial_published = models.DateTimeField("date published", default=datetime.now()) # timezone.now()

    def __str__(self):
        return self.tutorial_title