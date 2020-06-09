from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class NewUserForm(UserCreationForm):
    # the form will not be submitted until user gives the email
    email = forms.EmailField(required=True)

    # inject one more field email to be required
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    # if the form gets saved itself
    def save(self, commit=True):
        # save it for this point, not yet to submit the form
        user = super(NewUserForm, self).save(commit=False)
        # modify the email we just added, input the email to the database
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

