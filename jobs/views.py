# Views handle the logic of what happens when an API endpoint is called.
# They receive a request, process it, interact with the database,
# and return a response. Think of views as the "brain" of each endpoint.

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

# Import our models and serializers
from .models import Job, Application
from .serializers import JobSerializer, ApplicationSerializer


class JobListCreateView(generics.ListCreateAPIView):
    """
    GET  /jobs/  — Returns a list of all active job postings.
    POST /jobs/  — Creates a new job posting (employers only).
    
    generics.ListCreateAPIView is a Django REST Framework shortcut
    that automatically handles both listing and creating objects.
    We don't need to write separate get() and post() methods.
    """

    # queryset defines which objects this view works with.
    # We only show active jobs (is_active=True) to job seekers.
    queryset = Job.objects.filter(is_active=True).order_by('-created_at')

    # The serializer converts Job objects to/from JSON
    serializer_class = JobSerializer

    # IsAuthenticatedOrReadOnly means:
    # - Anyone (even without an account) can READ (GET) the job list
    # - Only logged-in users can CREATE (POST) a new job
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # This method is called automatically when a new job is created.
        # We automatically set the employer to the currently logged-in user
        # so the user cannot fake being a different employer.
        serializer.save(employer=self.request.user)


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /jobs/<id>/  — Returns details of a single job.
    PUT    /jobs/<id>/  — Updates a job (employer only).
    DELETE /jobs/<id>/  — Deletes a job (employer only).

    RetrieveUpdateDestroyAPIView handles all three operations automatically.
    """

    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def update(self, request, *args, **kwargs):
        # Before allowing an update, we check that the person making
        # the request is actually the employer who posted the job.
        # This prevents one employer from editing another's job posting.
        job = self.get_object()
        if job.employer != request.user:
            return Response(
                # Return a clear error message explaining why it was denied
                {'error': 'You can only edit your own job postings.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Same check for deletion — only the employer who created
        # the job can delete it.
        job = self.get_object()
        if job.employer != request.user:
            return Response(
                {'error': 'You can only delete your own job postings.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class ApplyJobView(APIView):
    """
    POST /jobs/<id>/apply/  — Submit an application for a specific job.
    
    We use APIView here instead of generics because we need more
    custom logic — checking if the user already applied, checking
    if the job is still active, etc.
    """

    # Only logged-in users can apply for jobs
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # 'pk' is the job ID passed in the URL e.g. /jobs/5/apply/
        # We try to find the job with that ID in the database.
        try:
            job = Job.objects.get(pk=pk, is_active=True)
        except Job.DoesNotExist:
            # If the job doesn't exist or is no longer active,
            # return a 404 Not Found response
            return Response(
                {'error': 'Job not found or no longer active.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Prevent employers from applying to their own job postings.
        # This is a business logic check — it wouldn't make sense.
        if job.employer == request.user:
            return Response(
                {'error': 'You cannot apply to your own job posting.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if this user has already applied for this specific job.
        # We don't want duplicate applications from the same person.
        if Application.objects.filter(job=job, applicant=request.user).exists():
            return Response(
                {'error': 'You have already applied for this job.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Pass the incoming request data to the serializer for validation.
        # The serializer checks that all required fields are present
        # and that the data is in the correct format.
        serializer = ApplicationSerializer(data=request.data)

        if serializer.is_valid():
            # Save the application and automatically set the applicant
            # to the currently logged-in user and the job to this job.
            serializer.save(applicant=request.user, job=job)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        # If the data is invalid, return the validation errors
        # so the client knows exactly what went wrong.
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class MyApplicationsView(generics.ListAPIView):
    """
    GET /applications/  — Returns all applications submitted by
    the currently logged-in user.

    ListAPIView automatically handles returning a list of objects.
    """

    serializer_class = ApplicationSerializer

    # Only logged-in users can see their applications
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Instead of returning ALL applications from the database,
        # we filter to only return applications belonging to the
        # currently logged-in user. This keeps data private —
        # users can only see their own applications, not others'.
        return Application.objects.filter(
            applicant=self.request.user
        ).order_by('-applied_at')


class MyJobsView(generics.ListAPIView):
    """
    GET /my-jobs/  — Returns all job postings created by
    the currently logged-in employer.
    """

    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter jobs to only show those posted by the current user.
        # An employer can see both active and inactive jobs they posted.
        return Job.objects.filter(
            employer=self.request.user
        ).order_by('-created_at')