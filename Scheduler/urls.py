from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from SchedulerApp.forms import UserLoginForm
from django.contrib.auth import views as auth_views
from SchedulerApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/',
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=UserLoginForm
        ),
        name='login'
    ),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('SchedulerApp.urls')),
   
    path('announcements/', views.announcements, name='announcements'),
    path('announcements/add/', views.announcementAdd, name='announcementAdd'),
    path('announcements/edit/', views.announcementEdit, name='announcementEdit'),
    path('announcements/detail/<int:pk>/', views.announcementDetail, name='announcementDetail'),
    path('announcements/delete/<int:pk>/', views.announcementDelete, name='announcementDelete'),
]

handler404 = 'SchedulerApp.views.error_404'
handler500 = 'SchedulerApp.views.error_500'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
