from django import forms 
from django.forms import ModelForm
from .models import Comment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class RegistrationForm(forms.Form):

    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'inputUsername',
            'placeholder': 'Username',
        }),
    )

    password = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'inputPassword',
            'placeholder': 'Password',
        }),
    )

    repeat_password = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'inputRepeatPassword',
            'placeholder': 'Repeat password',
        }),
    )

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['repeat_password']

        if password != confirm_password:
            raise forms.ValidationError(
                'Password mismatch'
            )
        
    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        user.save()
        auth = authenticate(**self.cleaned_data)
        return auth
    

class SignInForm(forms.Form):

    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'inputLogin',
            'placeholder': 'Username',
        })
    )

    password = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'inputPasswordSignIn',
            'placeholder': 'Password',
        })
    )


class FeedbackForm(forms.Form):

    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'inputName',
            'placeholder': 'Name',
        })
    )

    email = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'inputEmail',
            'placeholder': 'Email',
        })
    )

    subject = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'inputSubject',
            'placeholder': 'Subject',
        })
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'id': 'inputMessage',
            'rows': 2,
            'placeholder': 'Your message',
        })
    )


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
        }