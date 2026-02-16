# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
# from JobTech.models import Skill  # Assuming Skill model is in JobTech app

class CustomUser(AbstractUser):
    
    ROLE_CHOICES = (
        ('recruiter', 'Recruiter'),
        ('candidate', 'Candidate')
    )
    email = models.EmailField(unique=True, max_length=191)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    picture = models.ImageField(default="unknown.jpg", upload_to='media/media/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    

    def __str__(self):
        return self.get_full_name()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the user first
        if hasattr(self, 'candidate'):
            self.candidate.username = self.username
            self.candidate.save()
        if hasattr(self, 'recruiter'):
            self.recruiter.username = self.username  # If recruiter had a username field
            self.recruiter.save()

class Candidate(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    cover_letter = models.FileField(upload_to='cover_letters/', blank=True, null=True)

    skills = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    skills = models.CharField(
        max_length=255,
        verbose_name="Skills",
        help_text="Comma-separated list of skills",
        blank=True,
        null=True,
    )

    def getSkills(self):
        return [skill.strip().lower() for skill in self.skills.split(',') if skill.strip()]

    def __str__(self):
        return f"Candidate Profile for {self.user.username}"
    def calculate_pertinence(self, job):
        
        candidate_skills = set(self.getSkills())
        required_skills = set(job.getRequiredSkills())
        
        if not required_skills:  # Avoid division by zero
            return 0
            
        matching_skills = candidate_skills & required_skills
        pertinence = (len(matching_skills) / len(required_skills)) * 100
        return round(pertinence, 2)
    

class Recruiter(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Recruiter Profile for {self.user.username}"