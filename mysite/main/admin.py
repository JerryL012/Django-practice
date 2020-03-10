from django.contrib import admin
from .models import Tutorial    # register our model
from tinymce.widgets import TinyMCE
from django.db import models

# Register your models here.
class TutorialAdmin(admin.ModelAdmin):
    # customise, change order of the tutorial
    # fields = ["tutorial_title",
    #           "tutorial_published",
    #           "tutorial_contents"]

    # customise, separate them by fields
    fieldsets = [
        ("Title and date", {"fields" : ["tutorial_title", "tutorial_published"]}),
        ("content", {"fields" : ["tutorial_contents"]})
    ]

    # overwrite the textfield for us
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }


admin.site.register(Tutorial, TutorialAdmin)

