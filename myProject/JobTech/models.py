from django.db import models
from users.models import CustomUser




class Job(models.Model):
    title = models.CharField(
        max_length=75,
        verbose_name="Job Title",
        null=True,
        blank=True,
    )
    poster = models.ForeignKey(CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    contact_email = models.EmailField(
        max_length=191,
        verbose_name="Contact Email",
        null=True,
        blank=True

    )
    description = models.TextField(
        verbose_name="Job Description",
        help_text="Detailed job description",
        null=True,
        blank=True,
    )
    responsibility = models.TextField(
        verbose_name="Job Responsibility ",
        help_text="Detailed job responsibilities",
        null=True,
        blank=True,
    )
    qualifications  = models.TextField(
        verbose_name="Job Qualifications ",
        help_text="Detailed job qualifications",
        null=True,
        blank=True,
    )
    MinSalary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Min Salary "
    )
    MaxSalary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Max Salary Amount"
    )
    CATEGORIES = [
        ('IT Services & Consulting', 'IT Services & Consulting'),
        ('Marketing', 'Marketing'),
        ('Customer Service', 'Customer Service'),
        ('Human Resource', 'Human Resource'),
        ('Project Management', 'Project Management'),
        ('Business Development', 'Business Development '),
        ('Sales & Communication', 'Sales & Communication'),
        ('Teaching & Education', 'Teaching & Education'),
        ('Design & Creative', 'Design & Creative'),
    ]
    category = models.CharField(
        max_length=75,
        choices=CATEGORIES,
        default='office',
        verbose_name="Category"

    )
    applications = models.BigIntegerField(
        default=0,
        verbose_name="Number of Applications"
    )
    REMOTE_CHOICES = [
        ('Remote', 'Remote'),
        ('Hybrid', ' Remote'),
        ('On Site', 'On Site'),
    ]
    remote = models.CharField(
        max_length=20,
        choices=REMOTE_CHOICES,
        default='office',
        verbose_name="Remote Work Option"
    )
    location = models.CharField(  
        max_length=191,
        verbose_name="Job Location",
        null=True,
        blank=True,
    )
    img = models.ImageField(
        default='fallback.png',
        blank=True,
        null=True,
        verbose_name="Company logo"
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Posting Date"
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'active'),
            ('closed', 'closed')
        ],
        default='active',
        verbose_name="Job Status"
    )
    skills = models.CharField(
        max_length=255,
        verbose_name="Required Skills",
        help_text="Comma-separated list of required skills",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title
    def getRequiredSkills(self):
        return [skill.strip().lower() for skill in self.skills.split(',') if skill.strip()]



class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cover_letter = models.TextField(
        verbose_name="Cover Letter",
        help_text="Detailed cover letter",
        null=True,
        blank=True,
    )
    resume = models.FileField(upload_to='resumes/')
    date_applied = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('new', 'new'),
            ('interviewing', 'interviewing'),
            ('accepted', 'accepted'),
            ('rejected', 'rejected')
        ],
        default='new'
    )
    pertinency = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        verbose_name="Pertinency Score",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.applicant} - {self.job.title}"
    
    

class interview(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    date = models.CharField(null=True,blank=True, max_length=191)
    status = models.CharField(max_length=20,blank=True, null=True , choices=[
            ('accepted', 'accepted'),
            ('scheduled', 'scheduled'),
            ('rejected', 'rejected')],default='scheduled')
    

    def __str__(self):
        return f"{self.applicant} - {self.job.title}"
    