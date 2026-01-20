# accounts/forms.py
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Candidate, Recruiter

User = get_user_model()

# --- SIGNUP FORM ---
class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('candidate', 'Candidate'),
        ('recruiter', 'Recruiter')
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5'
        })
    )

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'border block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:outline-green-600 sm:text-sm',
        'placeholder': 'First name'
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'border block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:outline-green-600 sm:text-sm',
        'placeholder': 'Last name'
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'border block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:outline-green-600 sm:text-sm',
        'placeholder': 'Email'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'border block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:outline-green-600 sm:text-sm',
        'placeholder': 'Password'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'border block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:outline-green-600 sm:text-sm',
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = User  
        fields = ['first_name', 'last_name', 'email', 'role', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = f"{self.cleaned_data['first_name']}  {self.cleaned_data['last_name']}".lower()
        
        if commit:
            user.save()
            # Create the appropriate profile based on role
            role = self.cleaned_data['role']
            if role == 'candidate':
                Candidate.objects.create(user=user)
            elif role == 'recruiter':
                Recruiter.objects.create(user=user)
            
            # If you're using Django's auth backend, you need this:
            if hasattr(self, 'save_m2m'):
                self.save_m2m()
                
        return user

# --- LOGIN FORM ---
class CustomLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'passwordInput'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            try:
                user = User.objects.get(email=email)
                self.user = authenticate(username=user.username, password=password)
                if self.user is None:
                    raise forms.ValidationError("Invalid email or password.")
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid email or password.")
        return cleaned_data

    def get_user(self):
        return self.user


# --- EDIT PROFILE FORM ---
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            
        }

class editCandidateDocuments(forms.ModelForm):

    class Meta:
        model = Candidate
        fields = ['resume', 'cover_letter']
        widgets = {
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'cover_letter': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class EditProfilePicture(forms.ModelForm):
    class Meta:
        model = User
        fields = ['picture']
        widgets = {
            'picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }