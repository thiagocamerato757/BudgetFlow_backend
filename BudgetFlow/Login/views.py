from django.contrib.auth.models import User
from Login.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login as django_login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.request import Request
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
@method_decorator(csrf_exempt, name='dispatch')
class Loginview(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password')
            }
        ),
        responses={200: 'User authenticated and logged in successfully', 400: 'Invalid credentials'}
    )
    def put(self, request: Request) -> Response:
        """
        Handle PUT request to authenticate and log in the user.

        This method authenticates the user with the provided username and password,
        and logs in the user if the credentials are valid.

        :param request: The HTTP request object containing the username and password.
        :type request: Request
        :return: A response object containing a success message if the user is authenticated and logged in successfully,
                 or an error message with a 400 status code if the credentials are invalid.
        :rtype: Response
        """
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)
            return Response({"success": "User authenticated and logged in successfully"})
        return Response({"error": "Invalid credentials"}, status=HTTP_400_BAD_REQUEST)
@method_decorator(csrf_exempt, name='dispatch')    
class RegisterView(APIView):
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={201: 'User created successfully', 400: 'Bad Request'}
    )
    def post(self, request: Request) -> Response:
        """
        Handle POST request to create a new user.

        This method validates the incoming request data using the `UserSerializer`.
        If the data is valid, it creates a new user with the provided username and password,
        saves the user to the database, and returns a success response.
        If the data is not valid, it returns the serializer errors with a 400 status code.

        :param request: The HTTP request object containing the data to be validated and used for user creation.
        :type request: Request
        :return: A response object containing a success message if the user is created successfully,
                 or the serializer errors with a 400 status code if the data is invalid.
        :rtype: Response
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return Response({"success": "User created successfully"}, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username')
            }
        ),
        responses={200: 'User logged out successfully', 401: 'User not authenticated'}
    )
    def delete(self, request: Request) -> Response:
        """
        Handle DELETE request to log out the user.

        This method logs out the authenticated user.

        :param request: The HTTP request object.
        :type request: Request
        :return: A response object containing a success message if the user is logged out successfully,
                 or an error message with a 401 status code if the user is not authenticated.
        :rtype: Response
        """
        username = request.data.get('username')
        if not request.user.is_authenticated or request.user.username != username:
            return Response({"error": "User not authenticated"}, status=HTTP_401_UNAUTHORIZED)
        logout(request)
        return Response({"success": "User logged out successfully"})