from django import forms
from .models import Job

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'contact_email', 'MinSalary', 'MaxSalary', 'category',
                 'remote', 'location', 'description', 'responsibility', 'qualifications','skills']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'MinSalary': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'MaxSalary': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'remote': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'height: 150px'
            }),
            'responsibility': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'height: 150px'
            }),
            'qualifications': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'height: 150px'
            }),
            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'height: 100px',
                'placeholder': 'example: Python, Django, React'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['MinSalary'].required = False
        self.fields['MaxSalary'].required = False
        self.fields['responsibility'].required = False
        self.fields['qualifications'].required = False

    def clean(self):
        cleaned_data = super().clean()
        min_salary = cleaned_data.get('MinSalary')
        max_salary = cleaned_data.get('MaxSalary')

        # Convert empty strings to None
        if min_salary == '':
            cleaned_data['MinSalary'] = None
        if max_salary == '' or str(max_salary).lower() == 'none':
            cleaned_data['MaxSalary'] = None

        # Validate salary range if both exist
        if (min_salary is not None and 
            max_salary is not None and 
            min_salary > max_salary):
            self.add_error('MaxSalary', "Max salary must be greater than min salary")

        return cleaned_data