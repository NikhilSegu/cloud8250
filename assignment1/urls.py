from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('getHshdNum/', views.getHshdNum, name='getHshdNum'),
    path('about/', views.about, name="about"),
    path('aboutContent/', views.aboutContent, name="aboutContent"),
    path('education/', views.education, name="education"),
    path('workExp/', views.workExp, name="workExperience"),
    path('skills/', views.skills, name="skills"),
    path('achievements/', views.achievements, name="achievements"),
    path('register/', views.register, name="register"),
    path('login/', auth_view.LoginView.as_view(template_name='assignment1/login.html'), name="login"),
    path('logout/', auth_view.LogoutView.as_view(template_name='assignment1/home.html'), name="logout"),
    path('profile/', views.profile, name="profile"),
    path('download/', views.downloadF, name="download"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
