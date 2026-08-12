"""
==============================================================================
URL ROUTING CONFIGURATION
==============================================================================
This module routes incoming HTTP requests to their corresponding view handler
functions in adminapp and userapp.
==============================================================================
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from adminapp import views as adminapp_views
from userapp import views as userapp_views

urlpatterns = [
    # --------------------------------------------------------------------------
    # ADMIN ROUTES (Faculty / Admin Operations)
    # --------------------------------------------------------------------------
    path('admin/', admin.site.urls),                                               # Django built-in admin panel
    path('admin-index', adminapp_views.admin_index, name='admin_index'),          # Admin main dashboard overview
    path('admin-pending', adminapp_views.admin_pending, name='admin_pending'),      # Pending user registration requests
    path('admin-all', adminapp_views.admin_all, name='admin_all'),                  # All registered user list
    path('admin-add-subject', adminapp_views.admin_add_subject, name='admin_add_subject'),  # Add new exam subject
    path('admin-add-question', adminapp_views.admin_add_question, name='admin_add_question'),# Add question & model answer
    path('admin-manage-question', adminapp_views.admin_manage_question, name='admin_manage_question'), # Edit/delete questions
    path('admin-results', adminapp_views.admin_results, name='admin_results'),      # View all student results
    path('admin-analysis-graph', adminapp_views.admin_analysis_graph, name='admin_analysis_graph'), # Grade analytics charts
    path('accept-user/<int:user_id>', adminapp_views.accept_user, name='accept_user'), # Approve user registration
    path('decline-user/<int:user_id>', adminapp_views.decline_user, name='decline_user'), # Reject user registration
    path('remove-questions/<int:question_id>', adminapp_views.remove_questions, name='remove_questions'), # Delete question
    path('remove-subject/<int:subject_id>', adminapp_views.remove_subject, name='remove_subject'),   # Delete subject

    # --------------------------------------------------------------------------
    # USER ROUTES (Student Operations & Authentication)
    # --------------------------------------------------------------------------
    path('', userapp_views.index, name='index'),                                   # Website Home/Landing page
    path('admin-login', userapp_views.admin_login, name='admin_login'),           # Admin login form
    path('user-login', userapp_views.user_login, name='user_login'),               # Student login form
    path('user-register', userapp_views.user_register, name='user_register'),     # Student signup form
    path('user-contact', userapp_views.user_contact, name='user_contact'),         # Contact us page
    path('user-dashboard', userapp_views.user_dashboard, name='user_dashboard'),   # Logged-in student dashboard
    path('user-questions/<str:subject>', userapp_views.user_questions, name='user_questions'), # Take exam & NLP evaluation
    path('user-view-results/<int:answer_id>', userapp_views.user_view_results, name='user_view_results'), # Question mark breakdown
    path('user-myprofile', userapp_views.user_myprofile, name='user_myprofile'),   # View/edit student profile
    path('user-exam', userapp_views.user_exam, name='user_exam'),                 # Available subject list
    path('user-results', userapp_views.user_results, name='user_results'),         # Student's past exam history
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve uploaded media files in development


