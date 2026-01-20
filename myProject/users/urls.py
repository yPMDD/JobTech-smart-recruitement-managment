from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
     path('login/',views.user_login,name='login'),
     path('signup/',views.signup,name='signup'),
     path('logout/',views.logout_view,name='logout'),
     path('profile/',views.profile,name='profile'),
     path('editProfile/<int:id>/',views.editProfile,name='editProfile'),
     path('deleteProfile/<int:id>/',views.deleteProfile,name='deleteProfile'),
     path('editProfilePicture/<int:id>/',views.editProfilePicture,name='editProfilePicture'),
     

]
