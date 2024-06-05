# forms.py
from django import forms
from django.contrib.auth.models import User

COUNTRY_CHOICES = [
    ('US', 'United States'),
    ('CA', 'Canada'),
    ('GB', 'United Kingdom'),
    ('AU', 'Australia'),
    ('IN', 'India'),
    # Add more countries as needed
]

TOWN_CHOICES = [
    ('NY', 'New York'),
    ('LA', 'Los Angeles'),
    ('LN', 'London'),
    ('SY', 'Sydney'),
    ('MU', 'Mumbai'),
    # Add more towns as needed
]

class RegisterForm(forms.ModelForm):
    name = forms.CharField(max_length=30)
    surname = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'surname', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
