# Serializers convert complex Django model instances into JSON format
# that can be sent over the API, and also validate incoming JSON data
# before saving it to the database. Think of them as a bridge between
# your Django models and the outside world.

from rest_framework import serializers
from .models import Job, Application


class JobSerializer(serializers.ModelSerializer):
    """
    Serializer for the Job model.
    Converts Job objects to JSON and validates incoming job data.
    """

    # SerializerMethodField lets us add custom fields that don't
    # exist directly on the model but are computed dynamically.
    employer_name = serializers.SerializerMethodField()

    class Meta:
        # Tell the serializer which model it is working with
        model = Job

        # List every field we want to include in the API response.
        # 'employer' is the actual ForeignKey ID (a number).
        # 'employer_name' is our custom field showing the username.
        fields = [
            'id',
            'employer',
            'employer_name',
            'title',
            'company',
            'location',
            'job_type',
            'description',
            'requirements',
            'salary',
            'created_at',
            'is_active',
        ]

        # Read-only fields cannot be changed through the API.
        # 'employer' is set automatically from the logged-in user.
        # 'created_at' is set automatically by Django.
        read_only_fields = ['employer', 'created_at']

    def get_employer_name(self, obj):
        # This method is automatically called by SerializerMethodField.
        # 'obj' is the Job instance being serialized.
        # We return the employer's username instead of just their ID number,
        # making the API response more readable for frontend developers.
        return obj.employer.username


class ApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Application model.
    Handles converting application data to/from JSON.
    """

    # Custom field to show the job title instead of just the job ID number.
    # This makes the API response more informative.
    job_title = serializers.SerializerMethodField()

    # Custom field to show the applicant's username instead of their ID.
    applicant_name = serializers.SerializerMethodField()

    class Meta:
        # Tell the serializer which model it is working with
        model = Application

        fields = [
            'id',
            'job',
            'job_title',
            'applicant',
            'applicant_name',
            'cover_letter',
            'status',
            'applied_at',
        ]

        # These fields are set automatically and cannot be changed
        # directly through the API by the user.
        # 'applicant' is set from the logged-in user automatically.
        # 'applied_at' is set by Django when the application is created.
        # 'status' is controlled only by the employer, not the applicant.
        read_only_fields = ['applicant', 'applied_at', 'status']

    def get_job_title(self, obj):
        # 'obj' is the Application instance being serialized.
        # We access the related Job object through obj.job
        # and return its title for a more readable response.
        return obj.job.title

    def get_applicant_name(self, obj):
        # Returns the username of the person who submitted the application.
        # Much more readable than just showing a user ID number.
        return obj.applicant.username