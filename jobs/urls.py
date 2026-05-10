# urls.py maps URL patterns to their corresponding views.
# When a request comes in, Django checks this file to find
# which view should handle that specific URL.

from django.urls import path
from . import views

# 'app_name' sets a namespace for these URLs.
# This prevents conflicts if other apps have URLs with the same name.
app_name = 'jobs'

urlpatterns = [
    # GET  /jobs/       — List all active jobs
    # POST /jobs/       — Create a new job posting
    path('jobs/', views.JobListCreateView.as_view(), name='job-list-create'),

    # GET    /jobs/<id>/ — View a single job's details
    # PUT    /jobs/<id>/ — Update a job posting
    # DELETE /jobs/<id>/ — Delete a job posting
    path('jobs/<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),

    # POST /jobs/<id>/apply/ — Submit an application for a job
    path('jobs/<int:pk>/apply/', views.ApplyJobView.as_view(), name='job-apply'),

    # GET /applications/ — View all your submitted applications
    path('applications/', views.MyApplicationsView.as_view(), name='my-applications'),

    # GET /my-jobs/ — View all jobs you have posted as an employer
    path('my-jobs/', views.MyJobsView.as_view(), name='my-jobs'),
]