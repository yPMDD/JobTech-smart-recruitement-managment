from django.urls import path
from . import views 



urlpatterns = [
    path('', views.homepage,name='home'),
    path('about/',views.about),
    path('notfound/',views.notfound),
    path('category/',views.category),
    path('contact/',views.contact),
    path('jobDetail/',views.jobDetail, name='jobDetail'),
    path('jobList/',views.jobList,name="jobList"),
    path('testimonial/',views.testimonial),
    path('jobForm/',views.jobForm),
    path('jobsPosted',views.jobsPosted,name="jobsPosted"),
    path('editJob/<int:id>/',views.editJob,name='editJob'),
    path('deleteJob/<int:id>/', views.deleteJob, name='deleteJob'),
    path('jobDetail/<int:id>/', views.jobDetails , name='jobDetails'),
    path('applyJob/<int:id>/', views.applyJob , name='applyJob'),
    path('appliedJobs/', views.appliedJobs, name='appliedJobs'),
    path('viewApplicants/<int:id>/', views.viewApplicants, name='viewApplicants'),
    path('changeAppStatus/<int:id>/<str:status>/', views.changeAppStatus, name='changeAppStatus'),
    path('changeJobStatus/<int:id>/<str:status>/', views.changeJobStatus, name='changeJobStatus'),
    path('deleteApplication/<int:id>/', views.deleteApplication, name='deleteApplication'),
    path('statusEmail/', views.emailPreview, name='changeStatusEmail'),
    path('applications/export/<int:id>', views.export_applications_to_excel, name='export_applications'),
    path('setInterviewDate/<int:id>',views.setInterviewDate, name='setInterviewDate'),
    path('viewInterviews/<int:id>',views.viewInterviews, name='viewInterviews'),
] 