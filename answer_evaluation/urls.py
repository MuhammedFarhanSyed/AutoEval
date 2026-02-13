"""answer_evaluation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from turtle import home
from django.contrib import admin
from django.urls import path
from adminapp  import views as adminapp_views
from userapp import views as userapp_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-index',adminapp_views.admin_index,name='admin_index'),
    path('admin-pending',adminapp_views.admin_pending,name='admin_pending'),
    path('admin-all',adminapp_views.admin_all,name='admin_all'),
    path('admin-add-subject',adminapp_views.admin_add_subject,name='admin_add_subject'),
    path('admin-add-question',adminapp_views.admin_add_question,name='admin_add_question'),
    path('admin-manage-question',adminapp_views.admin_manage_question,name='admin_manage_question'),
    
    path('admin-results',adminapp_views.admin_results,name='admin_results'),
    path('admin-analysis-graph',adminapp_views.admin_analysis_graph,name='admin_analysis_graph'),
    path('accept-user/<int:user_id>',adminapp_views.accept_user,name='accept_user'),
    path('decline-user/<int:user_id>',adminapp_views.decline_user,name='decline_user'),
    path('remove-questions/<int:question_id>',adminapp_views.remove_questions,name='remove_questions'),
    path('remove-subject/<int:subject_id>',adminapp_views.remove_subject,name='remove_subject'),

    

    #user urls
    path('',userapp_views.index,name='index'),
    path('admin-login',userapp_views.admin_login,name='admin_login'),
    path('user-login',userapp_views.user_login,name='user_login'),
    path('user-register',userapp_views.user_register,name='user_register'),
    path('user-contact',userapp_views.user_contact,name='user_contact'),
    path('user-dashboard',userapp_views.user_dashboard,name='user_dashboard'),
    path('user-questions/<str:subject>',userapp_views.user_questions,name='user_questions'),
    path('user-view-results/<int:answer_id>',userapp_views.user_view_results,name='user_view_results'),
    path('user-myprofile',userapp_views.user_myprofile,name='user_myprofile'),
    path('user-exam',userapp_views.user_exam,name='user_exam'),
    path('user-results',userapp_views.user_results,name='user_results'),

    
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

