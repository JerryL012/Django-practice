from django.db import models
from django.utils import timezone

class TutorialCategory(models.Model):
    tutorial_category = models.CharField(max_length=200)
    category_summary = models.CharField(max_length=200)
    # for the URL
    category_slug = models.CharField(max_length=200)

    # see this name at the admin page
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.tutorial_category

# TutorialSeries has a foreignkey called category
class TutorialSeries(models.Model):
    tutorial_series = models.CharField(max_length=200)

    # point to category
    # if the Tutorial already exists, need to set default=1, for the migration(i.e. add a new column to an existing table, need defaullt)
    # on_delete=models.SET_DEFAULT. is in case you delete the category, wont delete all the series in that category
    tutorial_category = models.ForeignKey(TutorialCategory, default=1, verbose_name="Category", on_delete=models.SET_DEFAULT)
    series_summary = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Series"

    def __str__(self):
        return self.tutorial_series

# Basically, it is creating a table called 'Tutorial', columns......etc
class Tutorial(models.Model):
    tutorial_title = models.CharField(max_length=200)
    tutorial_published = models.DateTimeField("date published", default=timezone.now)  # timezone.now()

    # for the URL
    # Tutorial already exists
    tutorial_slug = models.CharField(max_length=200, default=1)
    # point to series
    # # on_delete is the behaviour to adopt when the referenced object is deleted.
    tutorial_series = models.ForeignKey(TutorialSeries, default=1, verbose_name="Series", on_delete=models.SET_DEFAULT)

    tutorial_contents = models.TextField()

    def __str__(self):
        return self.tutorial_title
