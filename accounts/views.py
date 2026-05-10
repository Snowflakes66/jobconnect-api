# The accounts app handles everything related to user management —
# registering new users, logging in, and logging out.
# We use Django's built-in User model so we don't reinvent the wheel.

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class RegisterView(APIView):
    """
    POST /auth/register/  — Creates a new user account.

    Anyone can access this endpoint — even without being logged in.
    That's why permission_classes is set to AllowAny.
    """

    # AllowAny means no authentication is required to access this view.
    # This makes sense because new users don't have an account yet.
    permission_classes = [AllowAny]

    def post(self, request):
        # Extract the data sent by the client from the request body.
        # We expect: username, email, password
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Validate that all required fields are provided.
        # If any field is missing, return a 400 Bad Request response
        # with a clear message explaining what is missing.
        if not username or not password or not email:
            return Response(
                {'error': 'Username, email and password are all required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if a user with this username already exists.
        # Usernames must be unique — two users cannot share one.
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'A user with this username already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if a user with this email already exists.
        # We enforce unique emails for better account security.
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'A user with this email already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # create_user() is Django's built-in method for creating users.
        # It automatically hashes the password before saving it —
        # meaning the raw password is NEVER stored in the database.
        # This is a critical security feature.
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Create an authentication token for the new user.
        # This token is what the user will send with future requests
        # to prove they are logged in (instead of sending password each time).
        token = Token.objects.create(user=user)

        # Return a success response with the token and basic user info.
        # The client should store this token and send it in the
        # Authorization header of future requests.
        return Response(
            {
                'message': 'Account created successfully.',
                'token': token.key,
                'username': user.username,
                'email': user.email,
            },
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    """
    POST /auth/login/  — Logs in an existing user and returns their token.

    The client sends a username and password.
    If correct, we return the user's authentication token.
    """

    # Anyone can attempt to log in — no prior authentication needed.
    permission_classes = [AllowAny]

    def post(self, request):
        # Get the username and password from the request body
        username = request.data.get('username')
        password = request.data.get('password')

        # Make sure both fields were provided
        if not username or not password:
            return Response(
                {'error': 'Both username and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # authenticate() checks if the username and password are correct.
        # It returns the User object if valid, or None if invalid.
        # Django automatically compares the provided password against
        # the hashed password stored in the database.
        user = authenticate(username=username, password=password)

        if user is None:
            # The credentials were wrong — return a 401 Unauthorized response.
            # We intentionally keep the message vague for security —
            # we don't want to reveal whether the username or password
            # was the incorrect part.
            return Response(
                {'error': 'Invalid username or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # get_or_create() returns the existing token if one already exists,
        # or creates a new one if it doesn't.
        # This prevents a user from having multiple tokens at the same time.
        token, created = Token.objects.get_or_create(user=user)

        # Return the token along with basic user information.
        return Response(
            {
                'message': 'Login successful.',
                'token': token.key,
                'username': user.username,
                'email': user.email,
            },
            status=status.HTTP_200_OK
        )


class LogoutView(APIView):
    """
    POST /auth/logout/  — Logs out the currently logged-in user.

    We delete their token from the database, which immediately
    invalidates it. Any future requests using that token will be rejected.
    """

    # Only logged-in users (with a valid token) can log out.
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Delete the token associated with the current user.
        # request.user is automatically set by Django REST Framework
        # based on the token sent in the Authorization header.
        request.user.auth_token.delete()

        return Response(
            {'message': 'Logged out successfully.'},
            status=status.HTTP_200_OK
        )


class ProfileView(APIView):
    """
    GET /auth/profile/  — Returns the profile of the logged-in user.

    This is a simple endpoint to let the frontend know who is logged in.
    """

    # Must be logged in to view your own profile
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # request.user is the currently authenticated user.
        # We return their basic information as a JSON response.
        user = request.user
        return Response(
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                # date_joined is automatically set by Django
                # when the user account was first created.
                'date_joined': user.date_joined,
            },
            status=status.HTTP_200_OK
        )
