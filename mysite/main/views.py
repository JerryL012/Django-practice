from django.shortcuts import render, redirect  # render templates, when successfully login, redirect them to the other page
from django.http import HttpResponse
from .models import Tutorial, TutorialCategory, TutorialSeries
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# tutorial -> series -> category -> matching slug

def single_slug(request, single_slug):
    # click a URL, determine it is category or tutorial
    # it's a category URL
    categories = [c.category_slug for c in TutorialCategory.objects.all()]
    # if the URL is in the category_slug, then it's a category
    if single_slug in categories:
        matching_series = TutorialSeries.objects.filter(tutorial_category__category_slug=single_slug)
        series_urls = {}
        for m in matching_series.all():
            # earliest() is because of the datetime field in Tutorial
            part_one = Tutorial.objects.filter(tutorial_series__tutorial_series=m.tutorial_series).earliest("tutorial_published")
            # dict, key is object and the value is the URL
            series_urls[m] = part_one.tutorial_slug

        return render(request=request,
                      template_name="main/category.html",
                      context={"part_ones": series_urls})

    # it's a tutorial URL
    tutorials = [t.tutorial_slug for t in Tutorial.objects.all()]
    if single_slug in tutorials:
        this_tutorial = Tutorial.objects.get(tutorial_slug=single_slug)
        tutorials_from_series = Tutorial.objects.filter(tutorial_series__tutorial_series=this_tutorial.tutorial_series).order_by("tutorial_published") # sidebar need to be in order
        # need to know which one we are about to pop out(click on), so we need the index
        this_tutorial_idx = list(tutorials_from_series).index(this_tutorial)

        # pass 3 things to tutorial.html
        return render(request,
                      "main/tutorial.html",
                      {"tutorial": this_tutorial,
                       "sidebar": tutorials_from_series,
                       "this_tutorial_idx": this_tutorial_idx})

    # no match, django has own 404 response(later)
    return HttpResponse(f"{single_slug} is not matching anything of the URL now")

# Create your views here.
def homepage(request):
    # return HttpResponse("This is an <strong>awesome</strong> tutorial!!")
    return render(request=request,
                  template_name="main/categories.html",  # where the template is in the templates folder
                  context={"categories": TutorialCategory.objects.all})  # pass it to template by tutorial

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            # if the table is filled out, create a user and save it
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created: {username}")
            # login user
            login(request, user)
            messages.info(request, f"You successfully login as {username}")
            # successfully login, redirect user to the home page
            # go to the main app, homepage. find the app_name in urls.py.
            return redirect("main:homepage")
        else:
            # form.error_messages is a dictionary
            for msg in form.error_messages:
                messages.error(request, f"{msg}:{form.error_messages[msg]}")

    # use the django basic userform for now
    # request.method is default "GET". means the browser is requesting the form from server
    form = NewUserForm
    return render(request,
                  "main/register.html",
                  context={"form": form})   # pass the form to register.html


def logout_request(request):
    # logout the user
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")


def login_request(request):
    # use authenticate and AuthenticationForm here
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Successfully login as {username}!")
                return redirect("main:homepage")
            else:
                messages.error(request, "Invalid username or password!")
        else:
            messages.error(request, "Unexpected error!")

    form = AuthenticationForm()
    return render(request,
                  "main/login.html",
                  {"form": form})







