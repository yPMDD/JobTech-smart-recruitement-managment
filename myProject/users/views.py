from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404,redirect
from .forms import CustomUserCreationForm, CustomLoginForm ,EditProfileForm,EditProfilePicture,editCandidateDocuments
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser ,Candidate, Recruiter 
from .resume_parser import extract_text_from_file, extract_resume_sections
from django.conf import settings
import os


# Create your views here.
def user_login(req):
    next_url = req.GET.get('next', '')
    if next_url:  
        messages.warning(req, "Please log in first")
    if req.method == 'POST':
        form = CustomLoginForm(req.POST)
        if form.is_valid():
            user = form.get_user() 
            login(req, user)        
            messages.success(req, f'Welcome back , {user.username} !')
            return redirect('home') 
    else:
        form = CustomLoginForm()
    return render(req, 'login.html', {'form': form})


def signup(req):
    if req.method == 'POST':
        form = CustomUserCreationForm(req.POST, req.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()  # Save the base user first
            
            # Create role-specific profile
            if user.role == 'candidate':
                Candidate.objects.create(user=user)
            elif user.role == 'recruiter':
                Recruiter.objects.create(user=user)
            # Add HR services if needed
            
            login(req, user)
            messages.success(req, f'Welcome {user.username}! Please complete your profile.')
            return redirect('home')  
    else:
        form = CustomUserCreationForm()
    return render(req, 'signup.html', {'form': form})


def logout_view(req):
     if req.method == "POST": 
        logout(req) 
        messages.success(req,'You have been logged out !')
        return redirect("home")
     
def profile(req):
    return render(req,'profile.html')



@login_required(login_url='/users/login')
def editProfile(request, id):
    # Ensure the user can only edit their own profile
    
    
    user = get_object_or_404(CustomUser, id=id)
    is_candidate = (user.role == 'candidate' )
    
    if request.method == 'POST':
        
        user_form = EditProfileForm(request.POST, request.FILES, instance=user)
        candidate_form = None
        
        if is_candidate:
            candidate_form = editCandidateDocuments(request.POST, request.FILES, instance=user.candidate)
        
        if user_form.is_valid() and (not is_candidate or candidate_form.is_valid()):
            # Save user data
            user = user_form.save()
            
            # Save candidate-specific data (if applicable)
            if is_candidate:
                
                candidate = candidate_form.save(commit=False)
                
                # Handle file uploads explicitly (optional, if not handled by the form)
                if 'resume' in request.FILES:
                    
                    candidate.resume = request.FILES['resume']
                    candidate.save()
                if 'cover_letter' in request.FILES:
                    
                    candidate.cover_letter = request.FILES['cover_letter']
                    candidate.save()
                    
                file_path = os.path.join(settings.MEDIA_ROOT, str(candidate.resume))
                resume_text = extract_text_from_file(file_path)
                
                # Extract information from resume
                extracted_data = extract_resume_sections(resume_text)
                
                # Update candidate profile with extracted data
                candidate.skills = ', '.join(extracted_data['skills'])
                candidate.education = '\n'.join(extracted_data['education'])
                candidate.experience = '\n'.join(extracted_data['experience'])
                candidate.save()
            
            messages.success(request, "Profile updated successfully!")
            return redirect('users:profile')
        else:
            # Combine form errors for debugging
            errors = user_form.errors
            if is_candidate:
                errors.update(candidate_form.errors)
            messages.error(request, "Please correct the errors below.")
            print("Form errors:", errors)
    else:
        user_form = EditProfileForm(instance=user)
        candidate_form = None
        if is_candidate:
            candidate_form = editCandidateDocuments(instance=user.candidate)
    
    context = {
        'user_form': user_form,
        'candidate_form': candidate_form,
        'user': user,
        'is_candidate': is_candidate,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='/users/login')
def editProfilePicture(request, id):
    user = get_object_or_404(CustomUser, id=id)

    if request.method == 'POST':
        form = EditProfilePicture(request.POST, request.FILES, instance=user)
        if 'email' in form.fields:
            form.fields['email'].required = False
        if form.is_valid():
            form.save()
            messages.success(request, "Profile picture updated successfully")
            return redirect('users:profile')  # make sure this URL name exists
        else:
            messages.error(request, "Please correct the errors below")
            print("Form errors:", form.errors)
    else:
        form = EditProfilePicture(instance=user)
        if 'email' in form.fields:
            form.fields['email'].required = False

    return render(request, 'profile.html', {
        'form': form,
        'User': user
    })

@login_required(login_url='/users/login')
def deleteProfile(request, id):
    User = get_object_or_404(CustomUser, id=id)
    
    if request.method == 'POST':
        User.delete()
        
        messages.success(request, "Profile deleted successfully")
        return redirect('home')
    
    return render(request, 'profile.html', {
        'User': User
    })

