from django.shortcuts import render, get_object_or_404,redirect
from .models import Job , Application , interview
from django.contrib.auth.decorators import login_required
from .forms import JobPostingForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import HttpResponse
import pandas as pd
from .models import Application
from django.utils import timezone
from django.utils.html import strip_tags
from premailer import transform
from django.core.mail import EmailMessage


def homepage(req):
    Jobs  = Job.objects.all().order_by('-date')
    # messages.error(req,'error')
    # messages.success(req,'sucess')
    # messages.warning(req,'warning')
    return render(req,'index.html',{'jobs': Jobs})

def about(req):
    return render(req,'about.html')

def notfound(req):
    return render(req,'404.html')
def contact(req):
    return render(req,'contact.html')

def category(req):
    return render(req,'category.html')

@login_required(login_url='/users/login')
def jobList(req):
    Jobs  = Job.objects.all().order_by('-date')
    return render(req,'job-list.html',{'jobs': Jobs})

def jobDetail(req):
    return render(req,'job-detail.html')

def testimonial(req):
    return render(req,'testimonial.html')


@login_required(login_url='/users/login')
def jobDetails(req, id):
    job = get_object_or_404(Job, id=id)
    return render(req, 'job-detail.html', {'job': job})

@login_required(login_url='/users/login')
def jobForm(req):
    if req.method == 'POST':
        form = JobPostingForm(req.POST)
        print(form.errors)  # Before is_valid()
        if form.is_valid():
                
                # Create Job instance manually
                job = Job(
                    title=form.cleaned_data['title'],
                    contact_email=form.cleaned_data['contact_email'],
                    MinSalary=form.cleaned_data['MinSalary'],
                    MaxSalary=form.cleaned_data['MaxSalary'],
                    category=form.cleaned_data['category'],
                    remote=form.cleaned_data['remote'],
                    location=form.cleaned_data['location'],
                    description=form.cleaned_data['description'],
                    responsibility=form.cleaned_data['responsibility'],
                    qualifications=form.cleaned_data['qualifications'],
                    skills=form.cleaned_data['skills'],
                    poster=req.user
                )
                job.save()
                messages.success(req,'Job Posted Successfully !')
                return redirect('home')  
    else:
        
        form = JobPostingForm()

    return render(req, 'jobForm.html', {'form': form})

@login_required(login_url='/users/login')
def jobsPosted(req):
    Jobs  = Job.objects.all().order_by('-date')
    return render(req,'jobsPosted.html',{'jobs':Jobs})


@login_required(login_url='/users/login')
def editJob(request, id):
    job = get_object_or_404(Job, id=id, poster=request.user)
    
    if request.method == 'POST':
        form = JobPostingForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully")
            return redirect('jobsPosted')
        else:
            messages.error(request, "Please correct the errors below")
            print("Form errors:", form.errors)  # Debugging
    else:
        form = JobPostingForm(instance=job)
    
    return render(request, 'editJob.html', {
        'form': form,
        'job': job
    })

def deleteJob(req,id):
    job = get_object_or_404(Job, id=id, poster=req.user)  # Ensure only owner can delete
    job.delete()
    messages.success(req, "Job deleted successfully")
    return redirect('jobsPosted')  # Redirect to jobs list page




@login_required(login_url='/users/login')
def applyJob(request, id):
    job = get_object_or_404(Job, id=id)
    candidate = request.user.candidate
    if request.method == 'POST':
        # Check if the user has already applied for this job
        if Application.objects.filter(job=job, applicant=request.user).exists():
            messages.error(request, "You have already applied for this job.")
            return redirect('home')
        if request.user.role != 'candidate':
            messages.error(request, "You must be a candidate to apply for jobs.")
            return redirect('home')
        if request.user.candidate.resume is None or request.user.candidate.resume == '':
            messages.error(request, "Please upload your resume before applying.")
            return redirect('users:profile')
        else:
            job.applications = job.applications + 1
            job.save()


        
        
        app = Application(
            job=job,
            applicant=request.user,
            cover_letter=request.user.candidate.cover_letter,
            resume=request.user.candidate.resume,
            pertinency = candidate.calculate_pertinence(job)
            
        )
        
        app.save()
        # Handle the application logic here
        messages.success(request, f"You have successfully applied for the {job.title} job!")
        return redirect('home')
    
    return render(request, 'appliedJobs.html', {
        'user': User,
        'job': job
    })


@login_required
def appliedJobs(request):
    applications = Application.objects.filter(applicant=request.user)
    if request.user.role != 'candidate':
        messages.error(request, "You must be a candidate to view your applications.")
        return redirect('home')
    return render(request, 'appliedJobs.html', {
        'applications': applications
    })
@login_required
def viewApplicants(request, id):
    job = get_object_or_404(Job, id=id)
    applications = Application.objects.filter(job=job)
    return render(request, 'viewApplicants.html', {
        'applications': applications,
        'job': job
    })

@login_required
def changeAppStatus(request, id, status):
    application = get_object_or_404(Application, id=id)
    
    if request.method == 'POST':
        application.status = status
        application.save()
        Interview = get_object_or_404(interview,application_id=application.id)
        if Interview:
            Interview.status=status
            Interview.save()
            
        # Optionally, send an email notification to the applicant
        email_body = render_to_string('emails/changeStatus.html', {'application': application})
        email_html_inlined = transform(email_body)
        # email_plain = strip_tags(email_html_inlined)
        email = EmailMessage(
            'Application Status Update',
            email_html_inlined,
            'JobTech <saad989011@gmail.com>',
            [application.applicant.email]
            )
        email.content_subtype = 'html'  # Set content type to HTML
        email.send()
        messages.success(request, f"Application status updated to {status} and email sent to applicant.")
        
        return redirect('viewApplicants', id=application.job.id)
    
    return render(request, 'viewApplicants.html', {
        'application': application,
        'status': status
    })

def setInterviewDate(request, id):
    application = get_object_or_404(Application, id=id)
    
    if request.method == 'POST':
         
        interviewDate = request.POST.get('date')
        Interview = interview(
            job = application.job,
            applicant = application.applicant,
            date = interviewDate,
            application = application
         )
        
        Interview.save()

        application.status = "interviewing"
        application.save()
        # Optionally, send an email notification to the applicant
        email_body = render_to_string('emails/changeStatus.html', 
                                      {'application': application , 
                                       'date':interviewDate})
        email_html_inlined = transform(email_body)
        # email_plain = strip_tags(email_html_inlined)
        email = EmailMessage(
            'Application Status Update',
            email_html_inlined,
            'JobTech <saad989011@gmail.com>',
            [application.applicant.email]
            )
        email.content_subtype = 'html'  # Set content type to HTML
        email.send()
        messages.success(request, f"Application status updated to interviewing and email sent to applicant.")
        return redirect('viewApplicants', id=application.job.id)
    
    return render(request, 'viewApplicants.html', {
        'application': application,
        'status': 'interviewing'
    })



@login_required
def changeJobStatus(request, id, status):
    job = get_object_or_404(Job, id=id)
    
    if request.method == 'POST':
        job.status = status
        job.save()
        messages.success(request, f"Job status updated to {status}")
        return redirect('jobsPosted')
    
    return render(request, 'jobsPosted.html', {
        'job': job,
        'status': status
    })




@login_required
def deleteApplication(request, id):
    application = get_object_or_404(Application, id=id)
    job = get_object_or_404(Job, id=application.job.id)
    if request.method == 'POST':
        job.applications = job.applications - 1
        job.save()
        application.delete()
        messages.success(request, "Application deleted successfully")
        return redirect('appliedJobs')
    
    return render(request, 'appliedJobs.html', {
        'application': application
    })

@login_required
def emailPreview(request):
    application = get_object_or_404(Application, id=16)
    return render(request, 'emails/changeStatus.html', {
        'application': application,
        'date':"19-06-2025 at 9:00"
    })
    

@login_required
def export_applications_to_excel(request,id):
    # Get all applications with related data
    queryset = Application.objects.filter(job_id=id).select_related('job', 'applicant')
    
    # Prepare data for export
    data = []
    for app in queryset:
        data.append({
            'Candidate': f"{app.applicant.first_name} {app.applicant.last_name}",
            'Email': app.applicant.email,
            'Status': app.get_status_display(),
            'Applied': app.date_applied.strftime('%d-%m-%y'),
            'Resume': 'No resume uploaded' if not app.resume else app.resume.url,
            'Cover Letter': 'No cover letter uploaded' if not app.cover_letter else 'Cover letter provided',
            'Pertinency': app.pertinency,  # Replace with your actual calculation
            'Job Title': app.job.title,
        })
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Reorder columns to match your table
    df = df[['Candidate', 'Email', 'Status', 'Applied', 'Resume', 
             'Cover Letter', 'Pertinency', 'Job Title']]
    
    # Create HTTP response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename="applications_export.xlsx"'
    
    # Write DataFrame to Excel
    df.to_excel(response, index=False, sheet_name='Applications')
    
    return response


def viewInterviews(request, id):
    job = get_object_or_404(Job, id=id)
    interviews = interview.objects.filter(job=job)
    return render(request, 'viewInterviews.html', {
        'interviews': interviews,
        'job': job
    })
