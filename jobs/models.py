from django.db import models
# We import 'User' from Django's built-in auth system.
# This means we don't need to create our own user model from scratch.
# Django's User model already has fields like username, email, and password.
from django.contrib.auth.models import User


class Job(models.Model):
    """
    This model represents a job posting created by an employer.
    Each job belongs to a specific employer (a User) and contains
    all the details a job seeker needs to know before applying.
    """

    # --- JOB TYPE CONSTANTS ---
    # Instead of hardcoding strings like 'full_time' everywhere in our code,
    # we define them as class-level constants. This prevents typos and makes
    # the code easier to maintain. If we ever want to change a value,
    # we only change it in one place.
    FULL_TIME = 'full_time'
    PART_TIME = 'part_time'
    CONTRACT = 'contract'
    REMOTE = 'remote'

    # --- JOB TYPE CHOICES ---
    # Django uses this list of tuples to:
    # 1. Validate that only these values are saved to the database
    # 2. Display human-readable labels in the admin panel
    # Each tuple is: (value_stored_in_db, human_readable_label)
    JOB_TYPE_CHOICES = [
        (FULL_TIME, 'Full Time'),
        (PART_TIME, 'Part Time'),
        (CONTRACT, 'Contract'),
        (REMOTE, 'Remote'),
    ]

    # --- FIELDS ---

    # ForeignKey creates a many-to-one relationship.
    # Many jobs can belong to one employer (User).
    # on_delete=CASCADE means: if the employer's account is deleted,
    # all their job postings are automatically deleted too.
    # related_name='jobs' lets us do: user.jobs.all()
    # to get all jobs posted by a specific user.
    employer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='jobs'
    )

    # The job title e.g. "Backend Developer", "UI Designer"
    # max_length=255 is a safe standard length for titles
    title = models.CharField(max_length=255)

    # The name of the company posting the job
    company = models.CharField(max_length=255)

    # Where the job is located e.g. "Lagos, Nigeria" or "Remote"
    location = models.CharField(max_length=255)

    # The type of job — must be one of the JOB_TYPE_CHOICES above.
    # default=FULL_TIME means if no job type is provided, it saves 'full_time'
    job_type = models.CharField(
        max_length=20, choices=JOB_TYPE_CHOICES, default=FULL_TIME
    )

    # A detailed description of the job role and responsibilities.
    # TextField has no character limit, unlike CharField.
    description = models.TextField()

    # What skills or qualifications the applicant must have.
    requirements = models.TextField()

    # The salary is optional (null=True allows NULL in the database,
    # blank=True allows the field to be empty in forms/API).
    # DecimalField is used for money to avoid floating point errors.
    # max_digits=10 means up to 10 digits total e.g. 99,999,999.99
    # decimal_places=2 means two digits after the decimal point
    salary = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    # auto_now_add=True automatically sets this field to the
    # current date and time when the job is first created.
    # It cannot be changed afterwards.
    created_at = models.DateTimeField(auto_now_add=True)

    # This lets employers deactivate a job without deleting it.
    # default=True means all new jobs are active by default.
    is_active = models.BooleanField(default=True)

    def __str__(self):
        # This controls how a Job object is displayed as a string.
        # e.g. in the Django admin panel or when printed in the terminal.
        # Output example: "Backend Developer at Google"
        return f"{self.title} at {self.company}"


class Application(models.Model):
    """
    This model represents a job application submitted by a job seeker.
    Each application links a specific User (applicant) to a specific Job.
    An employer can then update the status to accepted or rejected.
    """

    # --- APPLICATION STATUS CONSTANTS ---
    # Same pattern as Job types above — constants prevent typos
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    # The list of valid status values with human-readable labels
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]

    # --- FIELDS ---

    # Links this application to a specific job posting.
    # If the job is deleted, all its applications are deleted too (CASCADE).
    # related_name='applications' lets us do: job.applications.all()
    # to get every application submitted for a specific job.
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name='applications'
    )

    # Links this application to the user who applied.
    # related_name='applications' lets us do: user.applications.all()
    # to see all jobs a specific user has applied for.
    applicant = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='applications'
    )

    # The applicant's cover letter — why they want the job.
    # This is required (no null=True or blank=True).
    cover_letter = models.TextField()

    # Tracks where the application stands.
    # Starts as 'pending' by default when first submitted.
    # The employer can later change it to 'accepted' or 'rejected'.
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=PENDING
    )

    # Automatically records exactly when the application was submitted.
    # Cannot be modified after creation.
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Displays a clear summary of who applied for what.
        # Output example: "james → Backend Developer"
        # The → arrow makes it read like "james applied to Backend Developer"
        return f"{self.applicant.username} → {self.job.title}"