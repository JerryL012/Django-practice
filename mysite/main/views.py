from django.shortcuts import render  # render templates
from django.http import HttpResponse
from .models import Tutorial

# Create your views here.
def homepage(request):
    # return HttpResponse("This is an <strong>awesome</strong> tutorial!!")

    return render(request=request,
                  template_name="main/home.html",  # where the template is in the templates folder
                  context={"tutorials": Tutorial.objects.all})  # pass it to template

