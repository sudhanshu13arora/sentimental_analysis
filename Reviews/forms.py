from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models.fields import TextField
from django.forms import ModelForm, PasswordInput, DateField, DateInput, CharField, widgets, NumberInput, ValidationError

from .models import Reviews, Student

class ReviewsForm(ModelForm):
    class Meta:
        model = Reviews
        fields = ['meal','review','rating']


class UserForm(ModelForm):
    confirm_password = CharField(widget=PasswordInput, help_text="Enter the same password as before, for verification.",label="Password Confirmation")
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['password'].widget.attrs['minlength'] = 8

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password','confirm_password']
        widgets = {
           'password':PasswordInput()
        }
        # help_texts = {
        #     'username' : '*required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        #     'first_name': "*required",
        #     'last_name': "*required"
        # }

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError(
                "Passwords don't match"
            )



class StudentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['regno'].widget.attrs['minlength'] = 7

    def clean_price(self):
        reg = self.cleaned_data['regno']
        if len(reg) < 7:
            raise ValidationError("Registration Number is of alteast 7 digits")
        return reg

    class Meta:
        model = Student
        fields = ['dob', 'regno']
        widgets = {
            'dob' : DateInput(format=('%Y-%m-%d') ),
        }
        labels = {
            'dob' : 'Date of Birth',
            'regno' : 'Registration Number'
        }
        help_texts = {
            'dob' : "Enter your date of birth in the format YYYY-MM-DD",
            'regno' : "Enter your college registration number"
        }
